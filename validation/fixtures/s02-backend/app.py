"""Minimal in-memory item API used by the S02 validation fixture."""
import json

ITEMS = {}


def handle(method, path, body=None):
    """Return (status, payload) for a request."""
    parts = [p for p in path.split("/") if p]
    if parts[:1] != ["items"]:
        return 404, {"error": "not found"}
    if method == "GET" and len(parts) == 1:
        return 200, sorted(ITEMS.values(), key=lambda i: i["id"])
    if method == "GET" and len(parts) == 2:
        item = ITEMS.get(parts[1])
        return (200, item) if item else (404, {"error": "not found"})
    if method == "POST" and len(parts) == 1:
        data = json.loads(body or "{}")
        if not isinstance(data.get("name"), str) or not data["name"].strip():
            return 400, {"error": "name required"}
        item_id = str(len(ITEMS) + 1)
        ITEMS[item_id] = {"id": item_id, "name": data["name"].strip()}
        return 201, ITEMS[item_id]
    return 405, {"error": "method not allowed"}
