#!/usr/bin/env python3
"""Install the runtime-only archive into a temporary directory and inspect it."""

from __future__ import annotations

import re
import tempfile
import zipfile
from pathlib import Path

from package_release import build, verify


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    with tempfile.TemporaryDirectory(prefix="geshen-mode-install-") as temp:
        temp_root = Path(temp)
        archive = build(temp_root / f"geshen-mode-v{version}.zip")
        verify(archive)
        with zipfile.ZipFile(archive) as package:
            package.extractall(temp_root / "installed")

        target = temp_root / "installed" / "geshen-mode"
        skill = (target / "SKILL.md").read_text(encoding="utf-8")
        if not skill.startswith("---\n") or "name: geshen-mode" not in skill:
            print("FAIL  安装后的SKILL.md frontmatter无效")
            return 1

        links = re.findall(r"\[[^\]]+\]\((references/[^)#]+)\)", skill)
        missing = [link for link in links if not (target / link).is_file()]
        if missing:
            print(f"FAIL  安装后缺少引用：{missing}")
            return 1

        forbidden = [name for name in ("playground", "tests", "evals", ".github") if (target / name).exists()]
        if forbidden:
            print(f"FAIL  安装包混入开发目录：{forbidden}")
            return 1

        print(f"PASS  临时安装：{len(links)}个Skill引用可解析，无网页/测试/CI目录")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
