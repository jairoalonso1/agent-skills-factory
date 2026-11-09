#!/usr/bin/env python3
"""Lightweight validation of a generated or supplied FIC HTML report."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from html.parser import HTMLParser

class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.lang: str | None = None
        self.links: list[str] = []
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        attrs_dict = dict(attrs)
        if tag == 'html':
            self.lang = attrs_dict.get('lang')
        if tag == 'title':
            self.in_title = True
        if tag == 'a' and attrs_dict.get('href'):
            self.links.append(str(attrs_dict['href']))
    def handle_endtag(self, tag: str) -> None:
        if tag == 'title':
            self.in_title = False
    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data.strip())

def validate(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f'HTML report does not exist: {path}')
    raw = path.read_bytes()
    if not raw.strip():
        raise ValueError('HTML report is empty')
    text = raw.decode('utf-8-sig')
    parser = ReportParser()
    parser.feed(text)
    parser.close()
    errors: list[str] = []
    if 'html' not in parser.tags:
        errors.append('Missing <html> element')
    if 'head' not in parser.tags:
        errors.append('Missing <head> element')
    if 'body' not in parser.tags:
        errors.append('Missing <body> element')
    if 'title' not in parser.tags or not ''.join(parser.title_parts).strip():
        errors.append('Missing non-empty <title>')
    if re.search(r'\{\{[A-Z0-9_]+\}\}', text):
        errors.append('Unresolved template placeholder(s) remain')
    if parser.lang and parser.lang.lower() not in {'es', 'es-co'}:
        errors.append(f'Unexpected language declaration: {parser.lang}')
    result = {
        'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
        'language': parser.lang, 'title': ''.join(parser.title_parts).strip(),
        'link_count': len(parser.links), 'external_links': [u for u in parser.links if u.startswith(('http://', 'https://'))],
        'errors': errors, 'valid': not errors,
    }
    return result

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html', type=Path)
    ap.add_argument('--json', dest='json_path', type=Path)
    args = ap.parse_args()
    result = validate(args.html)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.json_path:
        args.json_path.write_text(rendered + '\n', encoding='utf-8')
    return 0 if result['valid'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
