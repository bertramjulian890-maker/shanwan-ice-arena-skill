from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

_RO_ATTRS = frozenset({"venue_id", "display_name"})


def _data_root() -> Path:
    env = os.environ.get("ICE_ARENA_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parent.parent / "data" / "venues"


def _strip_redacted(obj: Any) -> Any:
    """Remove fields marked redacted:true from nested structures (compliance / drafts)."""
    if isinstance(obj, dict):
        if obj.get("redacted") is True:
            return None
        out: dict[str, Any] = {}
        for k, v in obj.items():
            if k in _RO_ATTRS:
                out[k] = v
                continue
            cleaned = _strip_redacted(v)
            if cleaned is not None:
                out[k] = cleaned
        return out
    if isinstance(obj, list):
        items = [_strip_redacted(x) for x in obj]
        return [x for x in items if x is not None]
    return obj


class VenueStore:
    """Loads all venue YAML files once; keeps dict in memory for low latency."""

    def __init__(self, venues_dir: Path | None = None) -> None:
        self._venues_dir = venues_dir or _data_root()
        self._by_id: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        self._by_id.clear()
        if not self._venues_dir.is_dir():
            raise FileNotFoundError(f"Venues directory not found: {self._venues_dir}")
        for path in sorted(self._venues_dir.glob("*.yaml")):
            if path.name.startswith("_") or path.name.startswith("."):
                continue
            with path.open(encoding="utf-8") as f:
                raw = yaml.safe_load(f)
            if not isinstance(raw, dict):
                raise ValueError(f"Invalid YAML (expected mapping): {path}")
            vid = raw.get("venue_id")
            if not vid:
                raise ValueError(f"Missing venue_id in {path}")
            self._by_id[str(vid)] = raw
        if not self._by_id:
            raise ValueError(f"No venue YAML files in {self._venues_dir}")

    def reload(self) -> None:
        self._load()

    def list_venue_ids(self) -> list[str]:
        return list(self._by_id.keys())

    def get_raw(self, venue_id: str | None) -> dict[str, Any]:
        vid = venue_id or os.environ.get("ICE_ARENA_DEFAULT_VENUE") or next(iter(self._by_id))
        if vid not in self._by_id:
            raise KeyError(f"Unknown venue_id={vid!r}. Known: {sorted(self._by_id)}")
        return self._by_id[vid]

    def section(self, venue_id: str | None, key: str, *, redact: bool = True) -> dict[str, Any]:
        data = self.get_raw(venue_id)
        block = data.get(key)
        if block is None:
            return {"venue_id": data.get("venue_id"), "display_name": data.get("display_name"), "notice": "待补充"}
        if not isinstance(block, dict):
            block = {"value": block}
        out = dict(block)
        out.setdefault("venue_id", data.get("venue_id"))
        out.setdefault("display_name", data.get("display_name"))
        if redact:
            cleaned = _strip_redacted(out)
            assert isinstance(cleaned, dict)
            return cleaned
        return out


_store: VenueStore | None = None


def get_store() -> VenueStore:
    global _store
    if _store is None:
        _store = VenueStore()
    return _store


def reset_store_for_tests() -> None:
    global _store
    _store = None
