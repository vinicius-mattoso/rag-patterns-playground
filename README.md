# RAG Patterns Playground

Este repositório foi construído como uma trilha prática de evolução de arquiteturas de RAG, saindo de um baseline simples e chegando a padrões mais robustos, governáveis e próximos de um cenário real de produção.

A proposta não é apenas “ter vários exemplos”. A proposta é mostrar uma jornada de engenharia:

- como um RAG nasce de forma simples
- onde os problemas começam a aparecer
- quais abstrações ajudam
- quando um banco vetorial local basta
- quando um grafo passa a fazer sentido
- quando uma ontologia deixa de ser opcional e passa a ser requisito

Em outras palavras: este repositório foi pensado para ajudar a transformar conhecimento isolado sobre RAG em capacidade real de projetar sistemas que possam ser colocados em produção com mais segurança.

## Visão do Projeto

Os módulos foram organizados como degraus de maturidade. Cada pasta representa um padrão, uma decisão arquitetural e um trade-off diferente.

O ganho disso é que a comparação fica concreta. Em vez de discutir RAG de forma abstrata, você consegue ver:

- o que muda no código
- o que muda na estrutura do projeto
- o que muda na persistência
- o que muda na forma de consultar
- o que muda no controle sobre os dados e sobre o comportamento do sistema

## O Que Existe Hoje

### `rag_001_naive_prompt`

O ponto de partida. Um RAG mais direto, com recuperação simples e montagem manual de prompt.

Esse estágio é importante porque ensina o essencial:

- chunking
- embeddings
- recuperação
- contexto
- montagem de prompt

Sem dominar essa base, qualquer framework vira caixa-preta.

### `rag_002_llamaindex_basic`

Primeira evolução com framework especializado em RAG. O objetivo aqui é mostrar como LlamaIndex organiza ingestão, indexação e consulta sem exigir tanta montagem manual.

Esse módulo ajuda a entender:

- abstrações de indexação
- query engines
- organização de pipeline com menos código artesanal

### `rag_003_langchain_basic`

O mesmo problema resolvido com LangChain, de forma comparável ao `rag_002`.

Esse módulo é valioso porque mostra uma diferença importante de mercado: LangChain tende a oferecer mais flexibilidade composicional e um ecossistema muito amplo, enquanto exige mais disciplina arquitetural.

### `rag_004_tabular_rag`

Uma transição importante: sair de documentos livres e começar a pensar em dados estruturados. Esse módulo abre o espaço para raciocínio tabular e serve como ponte conceitual para modelos mais relacionais.

Mesmo quando a solução final não é “tabular RAG puro”, esse tipo de conhecimento é importante porque muitos problemas reais envolvem:

- CSVs
- planilhas
- eventos operacionais
- dados relacionáveis entre si

### `rag_005_text_langchain_local`

Primeira entrada forte em GraphRAG sobre texto usando LangChain e `LLMGraphTransformer`.

Aqui o aprendizado muda de nível. A pergunta deixa de ser apenas “quais chunks recuperar?” e passa a ser:

- quais entidades existem?
- quais relações são relevantes?
- como preservar estrutura sem depender só de similaridade vetorial?

### `rag_006_text_langchain_prompt_graph`

Versão alternativa do GraphRAG textual, com extração guiada por prompt em vez de `LLMGraphTransformer`.

Esse contraste é importante porque mostra um ponto real de engenharia:

- nem toda equipe vai querer depender de um transformer especializado
- às vezes mais controle via prompt vale o custo
- às vezes a robustez operacional do framework compensa

### `rag_007_graphrag_neo4j`

Aqui o projeto deixa de ser apenas “grafo em memória” ou “grafo local” e passa a ter uma base persistida em Neo4j.

Esse é um salto importante de maturidade, porque começam a entrar preocupações típicas de produção:

- persistência durável
- schema observável
- consultas via Cypher
- inspeção do grafo
- rastreabilidade entre texto, entidades e relações

### `rag_008_graphrag_neo4j_ontology`

Este é o estágio em que o sistema começa a se aproximar de um GraphRAG realmente governável.

Em produção, um problema recorrente é o drift estrutural:

- labels variam
- relacionamentos mudam de nome
- ids ficam inconsistentes
- a query deixa de bater no grafo que foi salvo

Por isso a ontologia passa a ser central. Ela funciona como contrato do domínio:

- quais entidades são válidas
- quais relacionamentos são válidos
- quais aliases podem existir
- quais combinações fazem sentido

Esse padrão é especialmente relevante quando o objetivo é construir sistemas confiáveis e auditáveis, e não apenas demos inteligentes.

## O Padrão de Construção do Repositório

Um dos pontos mais importantes deste projeto é que os módulos seguem um padrão relativamente consistente de construção.

Esse padrão não foi mantido por estética. Ele foi mantido para facilitar:

- comparação entre abordagens
- refatoração incremental
- troca de componentes
- evolução arquitetural sem recomeçar do zero

De forma geral, os módulos seguem esta linha:

- `app_direct.py` como ponto de execução simples e explícito
- `src/` com separação de responsabilidades
- `config.py` para centralizar ambiente e parâmetros
- `loaders.py` para ingestão
- componentes específicos para indexação, consulta, grafo ou ontologia
- `docs/` para arquitetura e decisões
- `tests/` quando faz sentido para validar partes críticas

Esse tipo de organização é extremamente útil em times e projetos reais. Ele reduz acoplamento, melhora legibilidade e torna a evolução da solução mais sustentável.

## Por Que Esse Conhecimento É Relevante Para Produção

Colocar RAG em produção não é só conectar um LLM a um conjunto de documentos.

O que normalmente separa um protótipo de uma solução utilizável de verdade são fatores como:

- qualidade da recuperação
- consistência do contexto enviado ao modelo
- governança do dado indexado
- persistência local ou remota
- possibilidade de auditar a resposta
- capacidade de explicar por que o sistema respondeu daquela forma
- previsibilidade do comportamento ao longo do tempo

Este repositório foi desenhado justamente para desenvolver essa maturidade.

Ao percorrer os módulos, você passa por competências que são fundamentais para um RAG de produção:

- modelagem de chunking
- estratégia de embeddings
- recuperação vetorial
- montagem de prompts grounded
- persistência local
- desacoplamento entre provider e lógica de negócio
- consulta sobre dados estruturados
- construção e consulta de grafos
- uso de Neo4j como runtime de conhecimento
- normalização guiada por ontologia

Isso significa que, ao final dessa trilha, você não fica apenas sabendo “usar um framework”. Você fica preparado para decidir qual padrão faz sentido para cada tipo de problema.

## Quando Cada Padrão Faz Mais Sentido

Nem todo caso precisa de GraphRAG. Nem todo caso precisa de ontologia. Nem todo caso precisa de Neo4j.

Uma leitura prática seria:

- `rag_001` a `rag_003`: bons para RAG textual clássico
- `rag_004`: útil quando o dado é tabular e estruturado
- `rag_005` e `rag_006`: úteis quando relações entre entidades passam a importar
- `rag_007`: útil quando o grafo precisa ser persistido, consultado e observado
- `rag_008`: útil quando o grafo precisa ser governado por regras do domínio

Esse tipo de discernimento é exatamente o que faz diferença na prática.

## O Que Significa “Estar Pronto Para Produção”

Este repositório não pretende dizer que basta rodar um módulo e pronto, o sistema já está em produção.

O que ele entrega é algo mais valioso: uma base arquitetural e conceitual para chegar lá com muito menos improviso.

Depois dessa trilha, a evolução natural para um cenário produtivo inclui:

- observabilidade e tracing
- avaliação automatizada de respostas
- políticas de fallback
- autenticação e segregação de acesso
- versionamento de ontologia
- pipelines de reindexação
- tratamento de custos e latência
- testes de regressão semântica
- governança sobre schema e qualidade do grafo

Ou seja: a parte difícil deixa de ser “como eu começo?” e passa a ser “como eu endureço isso para o meu contexto?”.

Esse é um ótimo lugar para estar.

## Como Navegar no Repositório

Se a ideia for aprender a progressão:

1. comece pelo `rag_001_naive_prompt`
2. compare com `rag_002_llamaindex_basic`
3. compare com `rag_003_langchain_basic`
4. observe a transição para estrutura em `rag_004_tabular_rag`
5. entre em GraphRAG com `rag_005` e `rag_006`
6. veja a persistência real com `rag_007_graphrag_neo4j`
7. finalize com governança em `rag_008_graphrag_neo4j_ontology`

Se a ideia for usar como referência de projeto:

- procure o módulo cujo padrão mais se aproxima do seu caso
- entenda o trade-off daquela abordagem
- e então adapte a estrutura, não apenas o código

## Fechamento

O objetivo deste repositório é mostrar que RAG não é uma receita única. É uma família de padrões.

Saber construir um sistema desse tipo para produção exige mais do que saber chamar API, gerar embedding ou fazer similarity search. Exige saber escolher arquitetura, definir contratos, controlar drift, explicar respostas e manter o sistema previsível.

Esse playground foi montado exatamente para desenvolver esse repertório.
