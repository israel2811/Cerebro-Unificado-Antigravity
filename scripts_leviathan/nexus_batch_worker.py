#!/usr/bin/env python3
"""Finite, portable batch worker for NEXUS cloud offload."""
from __future__ import annotations

import argparse
import compileall
import hashlib
import json
import os
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".nexus-artifacts"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def resolve_source(value: str | None) -> Path:
    candidate = ROOT / (value or "scripts_leviathan/raw_corpus_extraction.txt")
    candidate = candidate.resolve()
    if ROOT != candidate and ROOT not in candidate.parents:
        raise ValueError("source_path must stay inside the repository")
    if not candidate.exists():
        raise FileNotFoundError(candidate)
    return candidate


def system_metrics() -> dict:
    mem_total_kib = None
    mem_available_kib = None
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        vals = {}
        for line in meminfo.read_text(errors="ignore").splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                vals[key] = value.strip().split()[0]
        mem_total_kib = int(vals.get("MemTotal", 0)) or None
        mem_available_kib = int(vals.get("MemAvailable", 0)) or None
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "mem_total_kib": mem_total_kib,
        "mem_available_kib": mem_available_kib,
    }

def mode_validate() -> dict:
    scripts = ROOT / "scripts_leviathan"
    ok = compileall.compile_dir(str(scripts), quiet=1, force=False)
    py_files = list(scripts.rglob("*.py"))
    return {
        "ok": bool(ok),
        "python_files": len(py_files),
        "scripts_root": str(scripts.relative_to(ROOT)),
    }


def mode_inventory(source_value: str | None) -> dict:
    source = resolve_source(source_value) if source_value else ROOT
    files = []
    if source.is_file():
        files = [source]
    else:
        for path in source.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if ".git" in rel.parts or ".nexus-artifacts" in rel.parts or "__pycache__" in rel.parts:
                continue
            files.append(path)
    total = sum(p.stat().st_size for p in files)
    largest = sorted(files, key=lambda p: p.stat().st_size, reverse=True)[:20]
    return {
        "file_count": len(files),
        "total_bytes": total,
        "largest": [{"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size} for p in largest],
    }

def mode_split_corpus(source_value: str | None, chunk_mb: int) -> dict:
    source = resolve_source(source_value)
    if not source.is_file():
        raise ValueError("split-corpus requires a file source")
    chunks_dir = OUT / "chunks"
    if chunks_dir.exists():
        shutil.rmtree(chunks_dir)
    chunks_dir.mkdir(parents=True, exist_ok=True)
    target_bytes = max(1, chunk_mb) * 1024 * 1024
    manifest = []
    current_lines = []
    current_bytes = 0
    chunk_index = 1

    def flush() -> None:
        nonlocal current_lines, current_bytes, chunk_index
        if not current_lines:
            return
        out = chunks_dir / f"chunk_{chunk_index:04d}.txt"
        out.write_text("".join(current_lines), encoding="utf-8")
        manifest.append({"path": str(out.relative_to(ROOT)), "bytes": out.stat().st_size, "sha256": sha256_file(out)})
        chunk_index += 1
        current_lines = []
        current_bytes = 0

    with source.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line_bytes = len(line.encode("utf-8"))
            if current_lines and current_bytes + line_bytes > target_bytes:
                flush()
            current_lines.append(line)
            current_bytes += line_bytes
    flush()
    manifest_path = OUT / "chunk_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {
        "source": str(source.relative_to(ROOT)),
        "source_bytes": source.stat().st_size,
        "source_sha256": sha256_file(source),
        "chunk_mb": chunk_mb,
        "chunk_count": len(manifest),
        "manifest": str(manifest_path.relative_to(ROOT)),
    }


def write_result(result: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["validate", "inventory", "split-corpus"], default="validate")
    parser.add_argument("--source", default=None)
    parser.add_argument("--chunk-mb", type=int, default=4)
    parser.add_argument("--job-id", default="")
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    started = utc_now()
    base = {"job_id": args.job_id or None, "mode": args.mode, "started_at": started, "worker": "github-actions", "system": system_metrics()}
    try:
        if args.mode == "validate":
            detail = mode_validate()
        elif args.mode == "inventory":
            detail = mode_inventory(args.source)
        else:
            detail = mode_split_corpus(args.source, args.chunk_mb)
        result = {**base, "state": "completed", "finished_at": utc_now(), "result": detail}
        write_result(result)
        print(json.dumps(result, ensure_ascii=False))
        return 0 if detail.get("ok", True) else 1
    except Exception as exc:
        result = {**base, "state": "failed", "finished_at": utc_now(), "error": f"{type(exc).__name__}: {exc}"}
        write_result(result)
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

