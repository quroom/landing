from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from landing.models import BuildNote


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
    """Parse YAML-like frontmatter between leading --- delimiters."""
    meta: dict[str, str] = {}
    body = content

    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        raw_meta = match.group(1)
        body = match.group(2)
        for line in raw_meta.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            meta[key] = val

    return meta, body.strip()


class Command(BaseCommand):
    help = "Publish or update a BuildNote without server redeployment."

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "file",
            nargs="?",
            type=str,
            help="Path to markdown file (with optional frontmatter).",
        )
        parser.add_argument("--slug", type=str, help="BuildNote slug.")
        parser.add_argument("--title", type=str, help="BuildNote title.")
        parser.add_argument("--summary", type=str, help="BuildNote summary.")
        parser.add_argument(
            "--category",
            type=str,
            choices=[c[0] for c in BuildNote.Category.choices],
            default=BuildNote.Category.SOLO_DEV,
            help="BuildNote category.",
        )
        parser.add_argument(
            "--tags", type=str, default="", help="Comma separated tags."
        )
        parser.add_argument("--seo-title", type=str, default="", help="SEO title.")
        parser.add_argument("--seo-desc", type=str, default="", help="SEO description.")
        parser.add_argument(
            "--status",
            type=str,
            choices=[s[0] for s in BuildNote.Status.choices],
            default=BuildNote.Status.PUBLISHED,
            help="Publication status (published or draft).",
        )

    def handle(self, *args: object, **options: object) -> None:
        file_path_arg = options.get("file")
        raw_content = ""

        if file_path_arg:
            p = Path(str(file_path_arg))
            if not p.exists():
                raise CommandError(f"File not found: {p}")
            raw_content = p.read_text(encoding="utf-8")
        elif not sys.stdin.isatty():
            raw_content = sys.stdin.read()
        else:
            raise CommandError(
                "Please specify a markdown file or pass markdown content via stdin."
            )

        meta, body_markdown = parse_frontmatter(raw_content)

        slug = options.get("slug") or meta.get("slug")
        title = options.get("title") or meta.get("title")
        summary = options.get("summary") or meta.get("summary")
        category = (
            options.get("category")
            or meta.get("category")
            or BuildNote.Category.SOLO_DEV
        )
        tags = options.get("tags") or meta.get("tags") or ""
        seo_title = options.get("seo_title") or meta.get("seo_title") or ""
        seo_description = options.get("seo_desc") or meta.get("seo_description") or ""
        status = (
            options.get("status") or meta.get("status") or BuildNote.Status.PUBLISHED
        )

        if not slug:
            raise CommandError(
                "Slug is required either via --slug or frontmatter 'slug: ...'"
            )
        if not title:
            raise CommandError(
                "Title is required either via --title or frontmatter 'title: ...'"
            )
        if not summary:
            # Generate fallback summary from first 200 chars of body
            clean_body = re.sub(r"[#*`\n\r>-]", " ", body_markdown).strip()
            clean_body = re.sub(r"\s+", " ", clean_body)
            summary = clean_body[:200]

        pub_at = timezone.now() if status == BuildNote.Status.PUBLISHED else None

        defaults = {
            "title": title,
            "summary": summary,
            "body_markdown": body_markdown,
            "category": category,
            "tags": tags,
            "seo_title": seo_title,
            "seo_description": seo_description,
            "status": status,
        }

        note, created = BuildNote.objects.update_or_create(
            slug=slug,
            defaults=defaults,
        )

        if status == BuildNote.Status.PUBLISHED and not note.published_at:
            note.published_at = pub_at
            note.save(update_fields=["published_at"])

        action_str = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully {action_str} BuildNote: '{note.title}' (slug: {note.slug}, status: {note.status})"
            )
        )
