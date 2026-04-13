"""Graph query engine built on LangChain and Neo4j."""

from __future__ import annotations

import json
import re

from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import PromptTemplate

from src.chain_compat import GraphCypherQAChain
from src.config import AppConfig
from src.neo4j_compat import Neo4jGraph
from src.schemas import GraphQueryResult, GraphSupportRecord


CYPHER_GENERATION_TEMPLATE = """You are a Neo4j Cypher expert.
Task: Generate a read-only Cypher query for the user's question.

Rules:
- Use only the relationship types and properties present in the schema.
- Never write, update, delete, merge, create, drop, call dbms procedures, or call APOC mutation procedures.
- Prefer exact identifiers such as shipment ids when the question provides them.
- Return only the Cypher query, with no markdown fences or commentary.
- Keep the query concise and deterministic.

Schema:
{schema}

Question:
{question}
"""

QA_TEMPLATE = """You are answering questions from Neo4j graph query results.
Use only the provided context rows.
If the answer is not in the context, say "I don't know."
Answer in a short grounded paragraph.

Question: {question}
Context:
{context}
"""


def build_query_chain(config: AppConfig, llm: BaseLanguageModel, graph: Neo4jGraph) -> GraphCypherQAChain:
    """Create a Neo4j Cypher QA chain tuned for ontology-guided GraphRAG."""
    cypher_prompt = PromptTemplate(input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE)
    qa_prompt = PromptTemplate(input_variables=["question", "context"], template=QA_TEMPLATE)
    return GraphCypherQAChain.from_llm(
        graph=graph,
        llm=llm,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt,
        top_k=config.query_top_k,
        validate_cypher=True,
        return_intermediate_steps=True,
        allow_dangerous_requests=True,
    )


def _stringify_record(payload: object) -> str:
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, ensure_ascii=False, default=str)


def _extract_generated_cypher(result: dict) -> str:
    for step in result.get("intermediate_steps", []):
        if isinstance(step, dict) and "query" in step:
            return str(step["query"])
    return ""


def _extract_context_records(result: dict, context_limit: int) -> tuple[GraphSupportRecord, ...]:
    for step in result.get("intermediate_steps", []):
        if isinstance(step, dict) and "context" in step:
            context = list(step["context"])
            return tuple(
                GraphSupportRecord(row_number=index, payload=_stringify_record(payload))
                for index, payload in enumerate(context[:context_limit], start=1)
            )
    return ()


def _extract_source_documents(
    graph: Neo4jGraph,
    context_records: tuple[GraphSupportRecord, ...],
    limit: int,
) -> tuple[str, ...]:
    entity_ids = sorted({match for record in context_records for match in re.findall(r"[A-Z]{2,}-\d+", record.payload)})
    if not entity_ids:
        return ()
    rows = graph.query(
        """
        MATCH (d:Document)-[:MENTIONS]->(e)
        WHERE e.id IN $entity_ids
        RETURN DISTINCT coalesce(d.source_name, d.id, d.source_path) AS source_name
        LIMIT $limit
        """,
        params={"entity_ids": entity_ids, "limit": limit},
    )
    return tuple(str(row["source_name"]) for row in rows if row.get("source_name"))


def run_query(chain: GraphCypherQAChain, graph: Neo4jGraph, question: str, context_limit: int) -> GraphQueryResult:
    """Execute a graph question and normalize the result."""
    print("[rag_008] generating Cypher and querying Neo4j")
    raw_result = chain.invoke({"query": question})
    generated_cypher = _extract_generated_cypher(raw_result)
    if generated_cypher:
        print(f"[rag_008] generated Cypher: {generated_cypher}")
    context_records = _extract_context_records(raw_result, context_limit=context_limit)
    print(f"[rag_008] retrieved {len(context_records)} context rows")
    source_documents = _extract_source_documents(graph, context_records=context_records, limit=context_limit)
    print(f"[rag_008] resolved {len(source_documents)} source documents")
    return GraphQueryResult(
        answer=str(raw_result.get("result", "I don't know.")),
        generated_cypher=generated_cypher,
        context_records=context_records,
        source_documents=source_documents,
    )
