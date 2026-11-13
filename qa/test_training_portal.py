from __future__ import annotations

import functools
import http.server
import json
import threading
import unittest
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.landmarks: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        if tag in {"header", "nav", "main", "footer"}:
            self.landmarks.append(tag)


def parse_page(relative: str) -> PageParser:
    parser = PageParser()
    parser.feed((ROOT / relative).read_text(encoding="utf-8"))
    return parser


def broken_internal_links(relative: str) -> list[str]:
    page = ROOT / relative
    parser = parse_page(relative)
    broken: list[str] = []
    ids = set(parser.ids)

    for href in parser.hrefs:
        parsed = urlsplit(href)
        if parsed.scheme in {"http", "https", "mailto"}:
            continue
        if not parsed.path:
            if parsed.fragment and parsed.fragment not in ids:
                broken.append(href)
            continue

        target = (page.parent / unquote(parsed.path)).resolve()
        if not target.exists():
            broken.append(href)
            continue

        if parsed.fragment and target == page.resolve() and parsed.fragment not in ids:
            broken.append(href)

        query = parse_qs(parsed.query)
        for doc in query.get("doc", []):
            if not (ROOT / unquote(doc)).is_file():
                broken.append(href)

    return broken


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


class TrainingPortalTests(unittest.TestCase):
    def test_training_and_home_pages_have_unique_ids(self) -> None:
        for relative in (
            "docs/index.html",
            "docs/training/index.html",
            "docs/admin/index.html",
        ):
            with self.subTest(file=relative):
                ids = parse_page(relative).ids
                duplicates = sorted({item for item in ids if ids.count(item) > 1})
                self.assertEqual([], duplicates)

    def test_training_page_has_required_accessibility_landmarks(self) -> None:
        parser = parse_page("docs/training/index.html")
        for landmark in ("header", "nav", "main", "footer"):
            with self.subTest(landmark=landmark):
                self.assertIn(landmark, parser.landmarks)
        source = (ROOT / "docs/training/index.html").read_text(encoding="utf-8")
        self.assertIn('class="skip-link" href="#main"', source)
        self.assertIn('name="viewport"', source)
        self.assertIn('lang="en"', source)
        self.assertIn('rel="icon" href="../assets/mgp-header-logo.png"', source)

    def test_training_and_home_internal_links_resolve(self) -> None:
        for relative in (
            "docs/index.html",
            "docs/training/index.html",
            "docs/admin/index.html",
        ):
            with self.subTest(file=relative):
                self.assertEqual([], broken_internal_links(relative))

    def test_negative_missing_anchor_is_detected(self) -> None:
        source = (ROOT / "docs/training/index.html").read_text(encoding="utf-8")
        mutated = source.replace('id="start-solution"', 'id="removed-start-solution"', 1)
        temporary = ROOT / "docs/training/.negative-link-test.html"
        try:
            temporary.write_text(mutated, encoding="utf-8")
            self.assertIn("#start-solution", broken_internal_links("docs/training/.negative-link-test.html"))
        finally:
            temporary.unlink(missing_ok=True)

    def test_negative_duplicate_id_is_detectable(self) -> None:
        parser = PageParser()
        parser.feed('<main id="main"><section id="main"></section></main>')
        duplicates = {item for item in parser.ids if parser.ids.count(item) > 1}
        self.assertEqual({"main"}, duplicates)

    def test_training_pages_serve_over_local_http(self) -> None:
        handler = functools.partial(QuietHandler, directory=str(ROOT))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for path in (
                "/docs/index.html",
                "/docs/training/index.html",
                "/docs/admin/index.html",
                "/docs/admin/catalog.json",
            ):
                with self.subTest(path=path):
                    with urllib.request.urlopen(
                        f"http://127.0.0.1:{server.server_port}{path}", timeout=5
                    ) as response:
                        self.assertEqual(200, response.status)
                        self.assertIn(
                            response.headers.get_content_type(),
                            {"text/html", "application/json"},
                        )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_admin_explorer_has_preview_and_source_views(self) -> None:
        source = (ROOT / "docs/admin/index.html").read_text(encoding="utf-8")
        for required_id in (
            'id="category-list"',
            'id="document-search"',
            'id="document-list"',
            'id="preview-tab"',
            'id="source-tab"',
            'id="document-preview"',
            'id="document-source"',
            'id="edit-with-copilot"',
            'id="suggest-change"',
            'id="change-dialog"',
            'id="generated-change-prompt"',
        ):
            with self.subTest(required_id=required_id):
                self.assertIn(required_id, source)
        self.assertNotIn("Admin passphrase", source)

    def test_admin_copilot_handoff_preserves_governance(self) -> None:
        source = (ROOT / "docs/admin/app.js").read_text(encoding="utf-8")
        for expected in (
            "@workspace",
            "Target file:",
            "Preserve confirmed facts, assumptions, unknowns, approval boundaries",
            "Run the smallest relevant validation",
            "feature branch and pull request",
            "Do not commit, push, deploy, or change production",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, source)

    def test_admin_catalog_is_complete_and_safe(self) -> None:
        catalog = json.loads(
            (ROOT / "docs/admin/catalog.json").read_text(encoding="utf-8")
        )
        documents = catalog["documents"]
        categories = {document["category"] for document in documents}
        self.assertTrue(
            {
                "Skills",
                "Instructions",
                "Agents",
                "Standards",
                "Templates",
                "QA",
                "Governance",
                "Architecture",
                "Training",
            }.issubset(categories)
        )
        self.assertEqual(len(documents), len({document["path"] for document in documents}))
        for document in documents:
            with self.subTest(path=document["path"]):
                self.assertNotIn("..", document["path"])
                self.assertTrue(document["path"].endswith(".md"))
                self.assertTrue((ROOT / document["path"]).is_file())

    def test_guide_allows_catalog_roots_and_embed_mode(self) -> None:
        source = (ROOT / "docs/guide/guide.js").read_text(encoding="utf-8")
        self.assertIn('".github"', source)
        self.assertIn('"agents"', source)
        self.assertIn('params.get("embed") === "1"', source)
        self.assertIn("readableMarkdown", source)
        styles = (ROOT / "docs/guide/guide.css").read_text(encoding="utf-8")
        self.assertIn(".guide-embed .guide-content", styles)


if __name__ == "__main__":
    unittest.main()
