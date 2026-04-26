from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "submissions" / "dist"

DOCUMENTS = [
    (
        ROOT / "submissions" / "attachments" / "Predlozhenie_ediny_otkryty_API_1194918-8.md",
        "Predlozhenie_ediny_otkryty_API_cifrovaya_valyuta_1194918-8",
    ),
    (ROOT / "submissions" / "appeal-duma.ru.md", "Obraschenie_Gosduma_1194918-8"),
    (ROOT / "submissions" / "appeal-cbr.ru.md", "Obraschenie_Bank_Rossii_API"),
    (ROOT / "submissions" / "appeal-minfin.ru.md", "Obraschenie_Minfin_1194918-8"),
]


def markdown_to_html(markdown: str) -> str:
    rows: list[str] = []
    in_list = False
    in_quote = False

    def close_blocks() -> None:
        nonlocal in_list, in_quote
        if in_list:
            rows.append("</ul>")
            in_list = False
        if in_quote:
            rows.append("</blockquote>")
            in_quote = False

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if not line:
            close_blocks()
            continue

        if line.startswith("# "):
            close_blocks()
            rows.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            close_blocks()
            rows.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            close_blocks()
            rows.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("- "):
            if not in_list:
                close_blocks()
                rows.append("<ul>")
                in_list = True
            rows.append(f"<li>{inline_html(line[2:])}</li>")
        elif re.match(r"^\d+\. ", line):
            close_blocks()
            rows.append(f"<p>{inline_html(line)}</p>")
        elif line.startswith("> "):
            if not in_quote:
                close_blocks()
                rows.append("<blockquote>")
                in_quote = True
            rows.append(f"<p>{inline_html(line[2:])}</p>")
        else:
            close_blocks()
            rows.append(f"<p>{inline_html(line)}</p>")

    close_blocks()
    return "\n".join(rows)


def inline_html(text: str) -> str:
    safe = html.escape(text)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", safe)
    return safe


def html_document(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      color: #111827;
      font-family: Arial, sans-serif;
      font-size: 12pt;
      line-height: 1.45;
      margin: 32px auto;
      max-width: 820px;
    }}
    h1 {{ font-size: 20pt; margin: 0 0 18px; }}
    h2 {{ font-size: 15pt; margin: 22px 0 8px; }}
    h3 {{ font-size: 13pt; margin: 18px 0 6px; }}
    p {{ margin: 8px 0; }}
    ul {{ margin: 8px 0 8px 22px; padding: 0; }}
    li {{ margin: 4px 0; }}
    blockquote {{
      border-left: 3px solid #9ca3af;
      color: #374151;
      margin: 12px 0;
      padding: 4px 0 4px 14px;
    }}
    code {{
      background: #f3f4f6;
      border-radius: 3px;
      font-family: Consolas, monospace;
      padding: 1px 3px;
    }}
    @media print {{
      body {{ margin: 0; max-width: none; }}
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def markdown_to_docx(markdown: str, output: Path) -> None:
    body_parts: list[str] = []
    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if not line:
            body_parts.append(paragraph(""))
        elif line.startswith("# "):
            body_parts.append(paragraph(line[2:], style="Heading1"))
        elif line.startswith("## "):
            body_parts.append(paragraph(line[3:], style="Heading2"))
        elif line.startswith("### "):
            body_parts.append(paragraph(line[4:], style="Heading3"))
        elif line.startswith("- "):
            body_parts.append(paragraph(line[2:], style="ListBullet"))
        elif re.match(r"^\d+\. ", line):
            body_parts.append(paragraph(line, style="ListNumber"))
        elif line.startswith("> "):
            body_parts.append(paragraph(line[2:], style="Quote"))
        else:
            body_parts.append(paragraph(line))

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {''.join(body_parts)}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>
"""

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", doc_rels)
        docx.writestr("word/document.xml", document_xml)
        docx.writestr("word/styles.xml", styles_xml())


def paragraph(text: str, style: str | None = None) -> str:
    style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{style_xml}<w:r><w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r></w:p>"


def styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="30"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListBullet">
    <w:name w:val="List Bullet"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListNumber">
    <w:name w:val="List Number"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Quote">
    <w:name w:val="Quote"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="360"/></w:pPr>
    <w:rPr><w:i/></w:rPr>
  </w:style>
</w:styles>
"""


def main() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    for source, stem in DOCUMENTS:
        markdown = source.read_text(encoding="utf-8")
        title = markdown.splitlines()[0].lstrip("# ").strip()
        body = markdown_to_html(markdown)
        (DIST / f"{stem}.html").write_text(html_document(title, body), encoding="utf-8")
        markdown_to_docx(markdown, DIST / f"{stem}.docx")


if __name__ == "__main__":
    main()

