#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"
SKIPPED_SCHEMES = ("http", "https", "mailto", "javascript", "data", "tel")
TITLE_PATTERN = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
H1_PATTERN = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class CatalogEntry:
    href: str
    title: str
    description: str


@dataclass(frozen=True)
class Reference:
    attribute: str
    value: str
    tag: str


class CatalogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.entries: list[CatalogEntry] = []
        self._current_href: str | None = None
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return

        attr_map = {key: value or "" for key, value in attrs}
        if "viz-link" not in attr_map.get("class", "").split():
            return

        self._current_href = attr_map.get("href", "")
        self._text_parts = []

    def handle_data(self, data: str) -> None:
        if self._current_href is None:
            return

        text = " ".join(data.split())
        if text:
            self._text_parts.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or self._current_href is None:
            return

        title = self._text_parts[0] if self._text_parts else ""
        description = " ".join(self._text_parts[1:]).strip()
        self.entries.append(CatalogEntry(self._current_href, title, description))
        self._current_href = None
        self._text_parts = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[Reference] = []
        self.ids: set[str] = set()
        self.scripts: list[tuple[str, str]] = []
        self._script_type: str | None = None
        self._script_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}

        tag_id = attr_map.get("id")
        if tag_id:
            self.ids.add(tag_id)

        for attr_name in ("href", "src", "xlink:href"):
            value = attr_map.get(attr_name)
            if value:
                self.references.append(Reference(attr_name, value, tag))

        if tag == "script":
            if not attr_map.get("src"):
                self._script_type = (attr_map.get("type") or "text/javascript").strip().lower()
                self._script_chunks = []

    def handle_data(self, data: str) -> None:
        if self._script_type is not None:
            self._script_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._script_type is not None:
            self.scripts.append((self._script_type, "".join(self._script_chunks)))
            self._script_type = None
            self._script_chunks = []


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_tags(text: str) -> str:
    return " ".join(TAG_PATTERN.sub(" ", text).replace("&amp;", "and").split())


def extract_title(text: str) -> str:
    match = TITLE_PATTERN.search(text)
    return strip_tags(match.group(1)) if match else ""


def extract_h1(text: str) -> str:
    match = H1_PATTERN.search(text)
    return strip_tags(match.group(1)) if match else ""


def parse_catalog_entries() -> list[CatalogEntry]:
    parser = CatalogParser()
    parser.feed(load_text(INDEX_PATH))
    return [entry for entry in parser.entries if is_local_reference(entry.href)]


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(load_text(path))
    return parser


def is_local_reference(value: str) -> bool:
    parts = urlsplit(value)
    return not parts.scheme and not parts.netloc


def should_skip_reference(value: str) -> bool:
    parts = urlsplit(value)
    if parts.scheme in SKIPPED_SCHEMES or parts.netloc:
        return True
    return False


def resolve_reference(base_path: Path, value: str) -> tuple[Path | None, str]:
    parts = urlsplit(value)
    fragment = parts.fragment
    path_part = parts.path

    if should_skip_reference(value):
        return None, fragment

    if not path_part:
        return base_path, fragment

    if path_part.startswith("/"):
        return (ROOT / path_part.lstrip("/")).resolve(), fragment

    return (base_path.parent / path_part).resolve(), fragment


def collect_ids(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        cache[path] = parse_page(path).ids
    return cache[path]


def check_inline_script_syntax(path: Path, scripts: list[tuple[str, str]]) -> list[str]:
    issues: list[str] = []

    for index, (script_type, script_text) in enumerate(scripts, start=1):
        normalized_type = script_type or "text/javascript"
        if "json" in normalized_type or "text/babel" in normalized_type:
            continue

        suffix = ".mjs" if normalized_type == "module" else ".js"
        with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False) as handle:
            temp_path = Path(handle.name)
            handle.write(script_text)

        result = subprocess.run(
            ["node", "--check", str(temp_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        temp_path.unlink(missing_ok=True)

        if result.returncode != 0:
            details = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "syntax error"
            issues.append(f"{path.relative_to(ROOT).as_posix()} inline script #{index}: {details}")

    return issues


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []
    id_cache: dict[Path, set[str]] = {}

    catalog_entries = parse_catalog_entries()
    seen_pages: set[Path] = set()

    for entry in catalog_entries:
        page_path = (ROOT / entry.href).resolve()
        rel_path = page_path.relative_to(ROOT).as_posix()
        seen_pages.add(page_path)

        if not page_path.exists():
            errors.append(f"Missing catalog target: {entry.href}")
            continue

        page_text = load_text(page_path)
        parser = parse_page(page_path)
        title = extract_title(page_text)
        h1 = extract_h1(page_text)

        if not title:
            errors.append(f"Missing title: {rel_path}")
        if not h1:
            errors.append(f"Missing H1: {rel_path}")

        for issue in check_inline_script_syntax(page_path, parser.scripts):
            errors.append(f"Inline script syntax error: {issue}")

        for reference in parser.references:
            value = reference.value.strip()
            if should_skip_reference(value):
                continue

            resolved_path, fragment = resolve_reference(page_path, value)
            if resolved_path is None:
                continue

            if not resolved_path.exists():
                errors.append(
                    f"Broken local reference in {rel_path}: <{reference.tag} {reference.attribute}=\"{value}\">"
                )
                continue

            if fragment and resolved_path.suffix == ".html":
                target_ids = collect_ids(resolved_path, id_cache)
                if fragment not in target_ids:
                    errors.append(
                        f"Missing fragment target in {rel_path}: {value}"
                    )

    notes.append(
        "Browser console checks are not part of this lightweight smoke test. "
        "This runner verifies catalog coverage, local links, title/H1 presence, "
        "and inline script syntax."
    )

    if errors:
        print("Smoke test failed:\n")
        for error in errors:
            print(f"ERROR: {error}")
        if notes:
            print("\nNotes:")
            for note in notes:
                print(f"NOTE: {note}")
        return 1

    print(f"Smoke test passed for {len(seen_pages)} catalog pages.")
    if notes:
        print("\nNotes:")
        for note in notes:
            print(f"NOTE: {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
