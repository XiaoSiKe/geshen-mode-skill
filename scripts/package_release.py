#!/usr/bin/env python3
"""Build and verify a deterministic, runtime-only Skill archive."""

from __future__ import annotations

import argparse
import hashlib
import stat
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOTS = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "VERSION",
    "agents",
    "assets",
    "references",
)


def package_files() -> list[Path]:
    files: list[Path] = []
    for name in RUNTIME_ROOTS:
        path = ROOT / name
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file() and item.name != ".DS_Store")
        else:
            raise FileNotFoundError(f"Skill运行文件不存在：{name}")
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
    print(f"BUILD  v{version} Skill包 -> {output}")
    return output


def verify(archive_path: Path) -> int:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    required = {
        "geshen-mode/SKILL.md",
        "geshen-mode/VERSION",
        "geshen-mode/agents/openai.yaml",
        "geshen-mode/assets/icon.svg",
        "geshen-mode/references/core-models.md",
        "geshen-mode/references/research-protocol.md",
        "geshen-mode/references/response-recipes.md",
        "geshen-mode/references/quality-rubric.md",
    }
    forbidden_prefixes = (
        "geshen-mode/.github/",
        "geshen-mode/docs/",
        "geshen-mode/evals/",
        "geshen-mode/examples/",
        "geshen-mode/playground/",
        "geshen-mode/scripts/",
        "geshen-mode/tests/",
    )
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        missing = required - names
        if missing:
            raise ValueError(f"Skill包缺少：{sorted(missing)}")
        forbidden = [name for name in names if name.startswith(forbidden_prefixes)]
        if forbidden:
            raise ValueError(f"Skill包混入开发文件：{forbidden[:3]}")
        packaged_version = archive.read("geshen-mode/VERSION").decode().strip()
        if packaged_version != version:
            raise ValueError(f"版本不一致：{packaged_version} != {version}")
    print(f"PASS  纯Skill包：{len(names)}个文件，版本{version}")
    return len(names)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    if args.check:
        with tempfile.TemporaryDirectory(prefix="geshen-release-") as temp:
            first = build(Path(temp) / f"geshen-mode-v{version}-a.zip")
            second = build(Path(temp) / f"geshen-mode-v{version}-b.zip")
            verify(first)
            first_hash = hashlib.sha256(first.read_bytes()).hexdigest()
            second_hash = hashlib.sha256(second.read_bytes()).hexdigest()
            if first_hash != second_hash:
                raise ValueError("相同源码生成了不同Skill包")
            print(f"PASS  确定性SHA-256：{first_hash[:16]}…")
        return 0

    archive = build(ROOT / "dist" / f"geshen-mode-v{version}.zip")
    verify(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
