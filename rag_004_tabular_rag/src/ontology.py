"""Ontology loading and parsing for CSV-to-graph conversion."""

from __future__ import annotations

from pathlib import Path

import yaml

from src.schemas import EntitySpec, Ontology, RelationshipSpec


def load_ontology(path: Path) -> Ontology:
    """Load ontology directives from a YAML file."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    entities = tuple(
        EntitySpec(
            table=item["table"],
            entity_type=item["entity_type"],
            id_column=item["id_column"],
            label_template=item["label_template"],
            description_template=item["description_template"],
            attribute_columns=tuple(item.get("attribute_columns", [])),
            color=item.get("color", "#4f46e5"),
        )
        for item in raw.get("entities", [])
    )
    relationships = tuple(
        RelationshipSpec(
            name=item["name"],
            source_table=item["source_table"],
            source_entity=item["source_entity"],
            source_key_column=item["source_key_column"],
            target_table=item["target_table"],
            target_entity=item["target_entity"],
            target_key_column=item["target_key_column"],
            relation_template=item["relation_template"],
        )
        for item in raw.get("relationships", [])
    )
    return Ontology(entities=entities, relationships=relationships)
