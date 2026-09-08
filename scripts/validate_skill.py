#!/usr/bin/env python3
"""Static contract checks for the 割神模式 skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"
RESEARCH = ROOT / "references" / "research"


def fail(message: str) -> None:
    print(f"FAIL  {message}")
    raise SystemExit(1)


def require(text: str, needle: str, owner: str) -> None:
    if needle not in text:
        fail(f"{owner} 缺少：{needle}")


def main() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    if not frontmatter:
        fail("SKILL.md frontmatter 无法解析")

    require(frontmatter.group(1), "name: geshen-mode", "frontmatter")
    description_match = re.search(
        r"description:\s*\|\n(?P<body>(?:[ \t]+.*\n?)+)", frontmatter.group(1)
    )
    if not description_match:
        fail("frontmatter 缺少多行 description")
    description = "\n".join(
        line.strip() for line in description_match.group("body").splitlines()
    )
    if len(description.encode("utf-8")) > 1024:
        fail("frontmatter description 超过 1024 bytes")

    for heading in (
        "# 割神模式（孙割Skill）",
        "## 模式路由",
        "## 双核工作流",
        "## 事实、推断与段子",
        "## 核心心智模型",
        "## 决策启发式",
        "## 表达DNA",
        "## 诚实边界",
        "## 附录：调研来源",
    ):
        require(skill, heading, "SKILL.md")

    for level in ("0级", "1级", "2级", "3级", "4级"):
        require(skill, level, "模式路由")

    for safety_rule in (
        "尚未进入实体审理",
        "孙宇晨单方叙述",
        "纯属虚构",
        "不得编造",
        "不构成投资建议",
    ):
        require(skill, safety_rule, "事实边界")

    for marker in ("✅ 已确认", "🟡 单方说法", "🔵 框架推断", "🎭 戏仿生成"):
        require(skill, marker, "来源标记")

    for hard_gate in ("当前无法核验", "current_mode", "硬性交付门"):
        require(skill, hard_gate, "交付门与会话状态")

    require(readme, "# 割神模式（孙割Skill）", "README.md")
    require(readme, "景甜", "README.md")
    require(readme, "Claude", "README.md")
    require(readme, "这不是事实裁判器", "README.md")
    require(readme, "案件尚未进入实体审理", "README.md")

    expected_research = [
        "01-writings.md",
        "02-conversations.md",
        "03-expression-dna.md",
        "04-external-views.md",
        "05-decisions.md",
        "06-timeline.md",
    ]
    missing = [name for name in expected_research if not (RESEARCH / name).is_file()]
    if missing:
        fail(f"缺少调研文件：{', '.join(missing)}")

    model_count = len(re.findall(r"^### 模型\d+:", skill, re.M))
    if not 3 <= model_count <= 7:
        fail(f"心智模型数量应为 3-7，当前为 {model_count}")

    heuristic_section = re.search(
        r"^## 决策启发式\n(?P<body>.*?)(?=^## 表达DNA)", skill, re.M | re.S
    )
    if not heuristic_section:
        fail("无法定位决策启发式 section")
    heuristic_count = len(
        re.findall(r"^\d+\. \*\*", heuristic_section.group("body"), re.M)
    )
    if not 5 <= heuristic_count <= 12:
        fail(f"决策启发式数量应为 5-12，当前为 {heuristic_count}")

    print("PASS  frontmatter、双核路由、事实边界、README 与调研目录均符合契约")
    print(f"PASS  {model_count} 个心智模型，{heuristic_count} 条决策启发式")


if __name__ == "__main__":
    main()
