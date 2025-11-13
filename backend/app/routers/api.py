from fastapi import APIRouter, Query, Body
from pathlib import Path
import json

router = APIRouter(prefix="/api")

base_dir = Path(__file__).resolve().parents[2] / "data"

def load(name: str):
    p = base_dir / name
    if not p.exists():
        return {"items": [], "total": 0, "updated_at": None, "source": []}
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def apply_common_filters(items, q: str | None):
    if q:
        ql = q.lower()
        items = [x for x in items if ql in str(x.get("name", "")).lower()]
    return items

def sort_items(items, key: str, order: str):
    reverse = order.lower() == "desc"
    return sorted(items, key=lambda x: x.get(key, 0), reverse=reverse)

@router.get("/mobile-soc")
def mobile_soc(sort: str = Query("score_total"), order: str = Query("desc"), q: str | None = Query(None)):
    data = load("mobile-soc.json")
    items = apply_common_filters(data.get("items", []), q)
    items = sort_items(items, sort, order)
    return {"items": items, "total": len(items), "updated_at": data.get("updated_at"), "source": data.get("source", [])}

@router.get("/cpu")
def cpu(sort: str = Query("score_multi"), order: str = Query("desc"), q: str | None = Query(None)):
    data = load("pc-cpu.json")
    items = apply_common_filters(data.get("items", []), q)
    items = sort_items(items, sort, order)
    return {"items": items, "total": len(items), "updated_at": data.get("updated_at"), "source": data.get("source", [])}

@router.get("/gpu")
def gpu(sort: str = Query("score_3d"), order: str = Query("desc"), q: str | None = Query(None)):
    data = load("pc-gpu.json")
    items = apply_common_filters(data.get("items", []), q)
    items = sort_items(items, sort, order)
    return {"items": items, "total": len(items), "updated_at": data.get("updated_at"), "source": data.get("source", [])}

@router.get("/meta")
def meta():
    return load("meta.json")

from datetime import datetime, timezone

@router.post("/update")
def update(target: str = Query("all")):
    meta = load("meta.json")
    ts = meta.get("updated_at")
    allow = True
    if ts:
        try:
            last = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            delta = (now - last).total_seconds()
            allow = delta >= 600
        except Exception:
            allow = True
    if not allow:
        return {"ok": False, "reason": "recently updated", "updated_at": ts}
    from ..scrapers.seed import run
    run(target)
    meta2 = load("meta.json")
    return {"ok": True, "target": target, "updated_at": meta2.get("updated_at")}
