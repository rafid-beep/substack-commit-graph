"""Fetch posts from configured Substack RSS feeds and write data.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import feedparser
import yaml


def feed_url(pub_url: str) -> str:
    return pub_url.rstrip("/") + "/feed"


def pub_host(pub_url: str) -> str:
    return urlparse(pub_url).netloc.lower()


def entry_authors(entry) -> list:
    names = []
    for a in entry.get("authors", []) or []:
        name = (a.get("name") or "").strip()
        if name:
            names.append(name)
    single = (entry.get("author") or "").strip()
    if single and single not in names:
        names.append(single)
    return names


def collect(pub_url: str, kind: str, byline: Optional[str]) -> list:
    parsed = feedparser.parse(feed_url(pub_url))
    posts = []
    for e in parsed.entries:
        published = e.get("published_parsed") or e.get("updated_parsed")
        if not published:
            continue
        if kind == "guest":
            authors = entry_authors(e)
            if not byline or not any(byline.lower() == a.lower() for a in authors):
                continue
        posts.append({
            "date": f"{published.tm_year:04d}-{published.tm_mon:02d}-{published.tm_mday:02d}",
            "title": e.get("title", "").strip(),
            "url": e.get("link", ""),
            "publication": pub_host(pub_url),
            "kind": kind,
        })
    return posts


def main() -> int:
    root = Path(__file__).parent
    cfg = yaml.safe_load((root / "config.yml").read_text())
    byline = (cfg.get("byline") or "").strip() or None

    posts = []
    for url in cfg.get("own_publications") or []:
        posts.extend(collect(url, "own", byline=None))
    for url in cfg.get("guest_publications") or []:
        posts.extend(collect(url, "guest", byline=byline))

    seen = set()
    deduped = []
    for p in sorted(posts, key=lambda x: x["date"], reverse=True):
        key = p["url"] or (p["date"], p["title"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(p)

    out = {
        "byline": byline,
        "posts": deduped,
    }
    (root / "data.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {len(deduped)} posts to data.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
