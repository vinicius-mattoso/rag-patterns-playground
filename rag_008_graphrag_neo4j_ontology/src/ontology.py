"""Ontology loading and lookup helpers."""

from __future__ import annotations

from pathlib import Path

import yaml

from src.schemas import EntityTypeSpec, Ontology, RelationshipTypeSpec


def _normalize_key(raw_value: str) -> str:
    return "".join(character.lower() for character in raw_value if character.isalnum())


def load_ontology(path: Path) -> Ontology:
    """Load the ontology YAML used to constrain graph extraction."""
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))

    entity_types = tuple(
        EntityTypeSpec(
            name=item["name"],
            aliases=tuple(item.get("aliases", [])),
            id_patterns=tuple(item.get("id_patterns", [])),
            required_properties=tuple(item.get("required_properties", [])),
            description=item.get("description", ""),
        )
        for item in payload.get("entity_types", [])
    )
    relationship_types = tuple(
        RelationshipTypeSpec(
            name=item["name"],
            aliases=tuple(item.get("aliases", [])),
            source_types=tuple(item.get("source_types", [])),
            target_types=tuple(item.get("target_types", [])),
            description=item.get("description", ""),
        )
        for item in payload.get("relationship_types", [])
    )

    entity_lookup = {}
    for spec in entity_types:
        entity_lookup[_normalize_key(spec.name)] = spec.name
        for alias in spec.aliases:
            entity_lookup[_normalize_key(alias)] = spec.name

    relationship_lookup = {}
    for spec in relationship_types:
        relationship_lookup[_normalize_key(spec.name)] = spec.name
        for alias in spec.aliases:
            relationship_lookup[_normalize_key(alias)] = spec.name

    return Ontology(
        entity_types=entity_types,
        relationship_types=relationship_types,
        entity_lookup=entity_lookup,
        relationship_lookup=relationship_lookup,
    )
