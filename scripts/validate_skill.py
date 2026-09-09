#!/usr/bin/env python3
"""Validate the v0.2 割神模式 skill package."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(text: str, needle: str, owner: str) -> None:
    if needle not in text:
        raise ValueError(f"{owner} 缺少：{needle}")


def validate_frontmatter(skill: str) -> None:
    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    if not frontmatter:
        raise ValueError("SKILL.md frontmatter 无法解析")
    require(frontmatter.group(1), "name: geshen-mode", "frontmatter")
    description = re.search(
        r"description:\s*\|\n(?P<body>(?:[ \t]+.*\n?)+)", frontmatter.group(1)
    )
    if not description:
        raise ValueError("frontmatter 缺少多行description")
    body = "\n".join(line.strip() for line in description.group("body").splitlines())
    if len(body.encode("utf-8")) > 1024:
        raise ValueError("frontmatter description超过1024 bytes")


def validate_references(skill: str) -> int:
    links = re.findall(r"\[[^\]]+\]\((references/[^)#]+)\)", skill)
    if len(links) < 10:
        raise ValueError(f"SKILL.md progressive disclosure链接不足：{len(links)}")
    missing = [link for link in links if not (ROOT / link).is_file()]
    if missing:
        raise ValueError(f"缺少引用文件：{', '.join(sorted(set(missing)))}")
    return len(set(links))


def main() -> int:
    try:
        skill = read("SKILL.md")
        readme = read("README.md")
        core = read("references/core-models.md")
        humor = read("references/humor-engine.md")
        outputs = read("references/output-contracts.md")
        case = read("references/cases/jingtian-2026.md")
        openai = read("agents/openai.yaml")
        changelog = read("CHANGELOG.md")
        version = read("VERSION").strip()

        validate_frontmatter(skill)
        if len(skill.splitlines()) > 260:
            raise ValueError(f"SKILL.md应保持轻量，当前{len(skill.splitlines())}行")

        for heading in ("## 模式路由", "## 双核工作流", "## 硬性交付门", "## 现实人物和投资边界"):
            require(skill, heading, "SKILL.md")
        for level in ("0级退出", "1级正常", "2级微割", "3级全割", "4级割后复盘"):
            require(skill, level, "模式路由")
        for marker in ("✅ 已确认", "🟡 单方说法", "🔵 框架推断", "🎭 戏仿生成"):
            require(skill, marker, "事实分层")
        for gate in ("当前无法核验", "current_mode", "硬性交付门"):
            require(skill, gate, "交付门")

        reference_count = validate_references(skill)

        models = len(re.findall(r"^### 模型\d+：", core, re.M))
        heuristic_section = re.search(
            r"^## 10条决策启发式\n(?P<body>.*?)(?=^## )", core, re.M | re.S
        )
        if not heuristic_section:
            raise ValueError("core-models.md缺少启发式section")
        heuristics = len(re.findall(r"^\d+\. \*\*", heuristic_section.group("body"), re.M))
        if models != 6 or heuristics != 10:
            raise ValueError(f"模型/启发式数量错误：{models}/{heuristics}")

        for phrase in ("割味编译器", "多轮去重", "人物辨识度检查"):
            require(humor, phrase, "humor-engine.md")
        for phrase in ("0级：退出", "4级：割后复盘", "策略题的无梗骨架"):
            require(outputs, phrase, "output-contracts.md")
        for phrase in ("案件尚未进入实体审理", "不表示法院已经确认", "原题止损，母题续航"):
            require(case, phrase, "jingtian-2026.md")

        scenario_files = sorted((ROOT / "references/humor").glob("*.md"))
        if len(scenario_files) != 6:
            raise ValueError(f"幽默场景包应为6个，当前{len(scenario_files)}个")

        ledger = json.loads(read("references/source-ledger.json"))
        if ledger.get("research_cutoff") != "2026-09-09" or len(ledger.get("sources", [])) < 6:
            raise ValueError("source-ledger.json不完整")

        if version != "0.2.0":
            raise ValueError(f"VERSION应为0.2.0，当前{version}")
        for owner, text in (("README.md", readme), ("CHANGELOG.md", changelog)):
            require(text, "0.2.0", owner)
        require(openai, 'display_name: "割神模式"', "agents/openai.yaml")
        require(openai, "$geshen-mode", "agents/openai.yaml")

        for phrase in (
            "三分割味，七分真东西",
            "感情小作文的锅，AI申请退出群聊",
            "不是随机发疯",
            "案件尚未进入实体审理",
        ):
            require(readme, phrase, "README.md")
        forbidden_readme = "以上是本项目的戏仿文案，不是孙宇晨或 Claude 的原话。"
        if forbidden_readme in readme:
            raise ValueError("README.md重新出现用户要求删除的句子")

    except (OSError, AttributeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL  {error}")
        return 1

    print(f"PASS  v{version} 包结构、frontmatter与轻量入口")
    print(f"PASS  6个模型、10条启发式、6个幽默场景包、{reference_count}个按需引用")
    print("PASS  事实边界、来源账本、README与UI元数据")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
