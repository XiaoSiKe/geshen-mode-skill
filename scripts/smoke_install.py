#!/usr/bin/env python3
"""Copy the skill package to a temporary install root and validate it."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDES = {".git", "__pycache__", ".pytest_cache"}


def ignore(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDES}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="geshen-mode-install-") as temp:
        target = Path(temp) / "geshen-mode"
        shutil.copytree(ROOT, target, ignore=ignore)
        result = subprocess.run(
            ["python3", "scripts/validate_skill.py"],
            cwd=target,
            text=True,
            capture_output=True,
            check=False,
        )
        print(result.stdout, end="")
        if result.returncode:
            print(result.stderr, end="")
            return result.returncode
        required = ("SKILL.md", "agents/openai.yaml", "references/core-models.md")
        missing = [path for path in required if not (target / path).is_file()]
        if missing:
            print(f"FAIL  安装副本缺少：{', '.join(missing)}")
            return 1
        print("PASS  临时目录安装烟雾测试")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
