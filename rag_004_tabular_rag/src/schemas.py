"""Schema definitions for Graph RAG over tabular data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph
import networkx as nx


@dataclass(frozen=True)
class LoadedTable:
    """A loaded CSV table."""

    name: str
    path: Path
    dataframe: pd.DataFrame


@dataclass(frozen=True)
class EntitySpec:
    """Ontology directive for creating graph nodes from a CSV table."""

    table: str
    entity_type: str
    id_column: str
    label_template: str
    description_template: str
    attribute_columns: tuple[str, ...]
    color: str


@dataclass(frozen=True)
class RelationshipSpec:
    """Ontology directive for creating graph edges between entities."""

    name: str
    source_table: str
    source_entity: str
    source_key_column: str
    target_table: str
    target_entity: str
    target_key_column: str
    relation_template: str


@dataclass(frozen=True)
class Ontology:
    """Ontology metadata used to map CSV rows into graph structure."""

    entities: tuple[EntitySpec, ...]
    relationships: tuple[RelationshipSpec, ...]


@dataclass(frozen=True)
class KnowledgeTripleView:
    """Readable view of a graph edge for evidence display."""

    subject: str
    relation: str
    object_: str
    source_table: str


@dataclass(frozen=True)
class GraphAssets:
    """All graph artifacts required by the pipeline."""

    graph: nx.MultiDiGraph
    entity_graph: NetworkxEntityGraph
    triple_views: tuple[KnowledgeTripleView, ...]
    node_text_index: dict[str, str]


@dataclass(frozen=True)
class GraphQueryResult:
    """Structured answer returned by the graph query pipeline."""

    answer: str
    entities: list[str]
    supporting_triples: list[KnowledgeTripleView]
