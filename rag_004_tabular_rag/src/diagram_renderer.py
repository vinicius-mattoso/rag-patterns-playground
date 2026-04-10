"""Render project diagrams as PNG assets."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from src.graph_builder import build_knowledge_graph
from src.loaders import load_csv_tables
from src.ontology import load_ontology


BG = "#08111f"
PANEL = "#0f1b2d"
TEXT = "#e5eefc"
MUTED = "#9fb4d0"
EDGE = "#5b708f"
ACCENT = "#69d2e7"


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_card(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    title: str,
    subtitle: str,
    color: str,
) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=22, fill=PANEL, outline=color, width=3)
    draw.text((x1 + 18, y1 + 14), title, font=_font(28, bold=True), fill=TEXT)
    draw.multiline_text((x1 + 18, y1 + 58), subtitle, font=_font(18), fill=MUTED, spacing=6)


def _draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    label: str,
    color: str = EDGE,
) -> None:
    draw.line([start, end], fill=color, width=4)
    ex, ey = end
    draw.polygon([(ex, ey), (ex - 16, ey - 8), (ex - 16, ey + 8)], fill=color)
    mx = (start[0] + end[0]) // 2
    my = (start[1] + end[1]) // 2
    draw.rounded_rectangle((mx - 110, my - 20, mx + 110, my + 18), radius=14, fill="#10243d")
    draw.text((mx - 98, my - 12), label, font=_font(16, bold=True), fill=ACCENT)


def render_ontology_diagram(output_path: Path) -> Path:
    """Render a Neo4j-style ontology overview image."""
    image = Image.new("RGB", (1800, 1100), BG)
    draw = ImageDraw.Draw(image)

    draw.text((70, 46), "Graph RAG Ontology", font=_font(42, bold=True), fill=TEXT)
    draw.text(
        (70, 102),
        "CSV tables become typed nodes and directed relationships used for Graph RAG and HTML visualization.",
        font=_font(22),
        fill=MUTED,
    )

    cards = {
        "Shipment": (130, 260, 470, 420, "#2563eb", "shipments.csv\nid: shipment_id\nattrs: status, priority, weight"),
        "Route": (690, 120, 1090, 280, "#0f766e", "routes.csv\nid: route_id\nattrs: origin, destination, distance"),
        "Carrier": (1330, 260, 1680, 420, "#7c3aed", "carriers.csv\nid: carrier_id\nattrs: service, on-time, fleet"),
        "Warehouse": (670, 720, 1110, 900, "#b45309", "warehouses.csv\nid: warehouse_id\nattrs: city, region, capacity"),
        "DeliveryEvent": (120, 720, 520, 900, "#dc2626", "delivery_events.csv\nid: event_id\nattrs: shipment_id, timestamp, type"),
    }

    for title, (x1, y1, x2, y2, color, subtitle) in cards.items():
        _draw_card(draw, (x1, y1, x2, y2), title, subtitle, color)

    _draw_arrow(draw, (470, 340), (690, 200), "uses route")
    _draw_arrow(draw, (1090, 200), (1330, 340), "handled by carrier", color="#8b5cf6")
    _draw_arrow(draw, (300, 720), (300, 420), "belongs to shipment", color="#ef4444")
    _draw_arrow(draw, (470, 400), (670, 760), "origin / destination", color="#d97706")
    _draw_arrow(draw, (470, 380), (1330, 380), "carrier relationship", color="#7c3aed")

    draw.rounded_rectangle((1180, 720, 1700, 920), radius=26, fill="#0b1627", outline="#2dd4bf", width=2)
    draw.text((1210, 748), "How to read this", font=_font(26, bold=True), fill=TEXT)
    draw.multiline_text(
        (1210, 796),
        "1. Each CSV row becomes a node.\n"
        "2. Foreign-key style columns create edges.\n"
        "3. ontology.yaml defines labels, colors,\n"
        "   and relation phrasing.\n"
        "4. The same graph feeds QA and HTML export.",
        font=_font(20),
        fill=MUTED,
        spacing=8,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return output_path


def render_answer_infographic(output_path: Path) -> Path:
    """Render a NotebookLM-style infographic for the SHP-004 answer flow."""
    image = Image.new("RGB", (1800, 1220), "#f5f1e8")
    draw = ImageDraw.Draw(image)

    dark = "#16202b"
    accent = "#2f6fed"
    red = "#d9485f"
    gold = "#b7791f"
    teal = "#127475"

    draw.rounded_rectangle((50, 40, 1750, 1180), radius=36, fill="#fcfaf5", outline="#d7d0c3", width=3)
    draw.text((90, 70), "How the graph answered: Who handles shipment SHP-004?", font=_font(40, bold=True), fill=dark)
    draw.text(
        (90, 126),
        "An infographic view of the retrieval path from question to grounded answer.",
        font=_font(22),
        fill="#556170",
    )

    steps = [
        ((100, 220, 430, 390), accent, "1. Question", "User asks:\nWhich carrier is responsible\nfor shipment SHP-004?"),
        ((520, 220, 880, 390), teal, "2. Entity Match", "Matched locally:\nSHP-004\nShipment SHP-004"),
        ((970, 220, 1350, 390), gold, "3. Triple Retrieval", "Six relevant triples are pulled\nfrom the graph neighborhood."),
        ((1420, 220, 1700, 390), red, "4. Grounded Answer", "Carrier Cargo Pulse is\nresponsible for SHP-004."),
    ]

    for rect, color, title, body in steps:
        _draw_card(draw, rect, title, body, color)

    _draw_arrow(draw, (430, 305), (520, 305), "find entity", accent)
    _draw_arrow(draw, (880, 305), (970, 305), "expand graph", teal)
    _draw_arrow(draw, (1350, 305), (1420, 305), "synthesize", gold)

    draw.text((100, 470), "Supporting graph evidence", font=_font(30, bold=True), fill=dark)

    evidence_cards = [
        ((100, 530, 820, 660), "#eaf2ff", accent, "Shipment SHP-004 -> Carrier Cargo Pulse", "is handled by carrier CAR-003 with priority critical"),
        ((100, 690, 820, 820), "#eefaf7", teal, "Shipment SHP-004 -> Route RTE-002 SaoPaulo-Curitiba", "uses route RTE-002 and is currently delayed"),
        ((100, 850, 820, 980), "#fff3e8", gold, "Shipment SHP-004 -> Warehouse Curitiba Cold Storage", "departs from warehouse WH-003"),
        ((100, 1010, 820, 1140), "#fff3e8", gold, "Shipment SHP-004 -> Warehouse Salvador Regional Hub", "arrives at warehouse WH-005"),
        ((920, 530, 1700, 660), "#fdecef", red, "Event EVT-005 loaded -> Shipment SHP-004", "belongs to shipment SHP-004 and happened at 2026-04-05T09:30:00"),
        ((920, 690, 1700, 820), "#fdecef", red, "Event EVT-006 exception -> Shipment SHP-004", "belongs to shipment SHP-004 and happened at 2026-04-06T21:10:00"),
    ]

    for rect, fill, border, title, body in evidence_cards:
        draw.rounded_rectangle(rect, radius=24, fill=fill, outline=border, width=3)
        draw.text((rect[0] + 18, rect[1] + 16), title, font=_font(24, bold=True), fill=dark)
        draw.multiline_text((rect[0] + 18, rect[1] + 56), body, font=_font(19), fill="#495463", spacing=6)

    draw.rounded_rectangle((920, 870, 1700, 1140), radius=28, fill="#18263a")
    draw.text((950, 902), "Why the answer is grounded", font=_font(28, bold=True), fill="#f9fafb")
    draw.multiline_text(
        (950, 954),
        "The decisive edge is the shipment-to-carrier relationship.\n"
        "Other triples provide operational context but do not change\n"
        "the ownership answer. The graph allows the system to isolate\n"
        "the relevant relation instead of reading raw CSV rows directly.",
        font=_font(22),
        fill="#d8e4f0",
        spacing=8,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return output_path


def render_project_diagrams(base_dir: Path) -> tuple[Path, Path]:
    """Generate both requested diagram assets for the project."""
    ontology_path = base_dir / "artifacts" / "ontology-neo4j-style.png"
    answer_path = base_dir / "artifacts" / "answer-flow-infographic.png"
    render_ontology_diagram(ontology_path)
    render_answer_infographic(answer_path)
    return ontology_path, answer_path
