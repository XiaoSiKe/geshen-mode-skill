#!/usr/bin/env python3
"""Build or verify a deterministic release zip for the current version."""

from __future__ import annotations

import argparse
import hashlib
import stat
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", "dist", "__pycache__", ".pytest_cache"}
EXCLUDED_NAMES = {".DS_Store"}


def package_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if not path.is_file():
            continue
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def build(output: Path) -> Path:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in package_files():
            relative = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"geshen-mode/{relative}", date_time=(2026, 9, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            permissions = 0o755 if path.stat().st_mode & stat.S_IXUSR else 0o644
            info.external_attr = permissions << 16
            archive.writestr(info, path.read_bytes())
    print(f"BUILD  v{version} -> {output}")
    return output


def verify(archive_path: Path) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    required = {
        "geshen-mode/SKILL.md",
        "geshen-mode/VERSION",
        "geshen-mode/agents/openai.yaml",
        "geshen-mode/references/core-models.md",
        "geshen-mode/playground/core.js",
    }
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        missing = required - names
        if missing:
            raise ValueError(f"release包缺少：{sorted(missing)}")
        packaged_version = archive.read("geshen-mode/VERSION").decode().strip()
        if packaged_version != version:
            raise ValueError(f"版本不一致：{packaged_version} != {version}")
        bad = [name for name in names if "/.git/" in name or "/dist/" in name or "__pycache__" in name]
        if bad:
            raise ValueError(f"release包包含临时文件：{bad[:3]}")
    print(f"PASS  release包：{len(names)}个文件，版本{version}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    if args.check:
        with tempfile.TemporaryDirectory(prefix="geshen-release-") as temp:
            archive = build(Path(temp) / f"geshen-mode-v{version}-a.zip")
            second = build(Path(temp) / f"geshen-mode-v{version}-b.zip")
            verify(archive)
            first_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
            second_hash = hashlib.sha256(second.read_bytes()).hexdigest()
            if first_hash != second_hash:
                raise ValueError("相同源码生成了不同Release包")
            print(f"PASS  确定性SHA-256：{first_hash[:16]}…")
        return 0

    archive = build(ROOT / "dist" / f"geshen-mode-v{version}.zip")
    verify(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
