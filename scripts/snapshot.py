#!/usr/bin/env python3
"""Fetch the public feed, keep only first-party fields, and write a dated snapshot
only when the content (ignoring the feed's own generatedAt timestamp) changed.

Usage: python3 scripts/snapshot.py            # writes snapshots/YYYY-MM-DD.json + latest.json when changed
Exit 0 always on success; prints "changed" or "unchanged".
"""
import datetime, json, os, sys, urllib.request

SOURCE_URL = "https://meetnewai.com/api/tools.json"
LIST_KEY = "items"
# First-party fields only. Anything else in the feed is dropped, so a third-party
# field added upstream never lands in this CC BY 4.0 dataset by accident.
ALLOWED_ITEM_FIELDS = ['slug', 'name', 'kind', 'category', 'categoryName', 'url', 'domain', 'pricing', 'tags', 'listingUrl', 'listingUrlZh', 'verified']
ALLOWED_TOP_FIELDS = ['version', 'name', 'provider', 'description', 'homepage', 'count', 'generatedAt']
MIN_ITEMS = 100

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP_DIR = os.path.join(ROOT, "snapshots")
LATEST = os.path.join(ROOT, "latest.json")


def fetch():
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "github-actions snapshot (+https://github.com/meetnewai/data)", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            sys.exit(f"HTTP {r.status} from {SOURCE_URL}")
        return json.load(r)


def clean(feed):
    items = feed.get(LIST_KEY)
    if not isinstance(items, list) or len(items) < MIN_ITEMS:
        sys.exit(f"feed has {len(items) if isinstance(items, list) else 'no'} {LIST_KEY}; refusing to write a snapshot")
    out = {k: feed[k] for k in ALLOWED_TOP_FIELDS if k in feed}
    out[LIST_KEY] = [{k: it[k] for k in ALLOWED_ITEM_FIELDS if k in it} for it in items]
    return out


def content_key(doc):
    d = {k: v for k, v in doc.items() if k != "generatedAt"}
    return json.dumps(d, sort_keys=True, ensure_ascii=False)


def main():
    new = clean(fetch())
    if os.path.exists(LATEST):
        with open(LATEST) as f:
            old = json.load(f)
        if content_key(old) == content_key(new):
            print("unchanged")
            return
    os.makedirs(SNAP_DIR, exist_ok=True)
    day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    body = json.dumps(new, ensure_ascii=False, indent=1) + "\n"
    for path in (os.path.join(SNAP_DIR, day + ".json"), LATEST):
        with open(path, "w") as f:
            f.write(body)
    print("changed", day, len(new[LIST_KEY]))


if __name__ == "__main__":
    main()
