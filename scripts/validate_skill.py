#!/usr/bin/env python3
"""Validate the skill-only 割神模式 package."""

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
        raise ValueError("SKILL.md frontmatter无法解析")
    require(frontmatter.group(1), "name: geshen-mode", "frontmatter")
    description = re.search(
        r"description:\s*\|\n(?P<body>(?:[ \t]+.*\n?)+)", frontmatter.group(1)
    )
    if not description:
        raise ValueError("frontmatter缺少多行description")
    body = "\n".join(line.strip() for line in description.group("body").splitlines())
    if len(body.encode("utf-8")) > 1024:
        raise ValueError("frontmatter description超过1024 bytes")


def validate_references(skill: str) -> int:
    links = re.findall(r"\[[^\]]+\]\((references/[^)#]+)\)", skill)
    if len(set(links)) < 14:
        raise ValueError(f"progressive disclosure引用不足：{len(set(links))}")
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
        research = read("references/research-protocol.md")
        recipes = read("references/response-recipes.md")
        rubric = read("references/quality-rubric.md")
        case = read("references/cases/jingtian-2026.md")
        openai = read("agents/openai.yaml")
        changelog = read("CHANGELOG.md")
        version = read("VERSION").strip()

        validate_frontmatter(skill)
        if len(skill.splitlines()) > 220:
            raise ValueError(f"SKILL.md应保持轻量，当前{len(skill.splitlines())}行")
        if len(readme.splitlines()) > 220:
            raise ValueError(f"README.md应保持简洁，当前{len(readme.splitlines())}行")

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
        for phrase in ("证据卡", "来源优先级", "失败降级"):
            require(research, phrase, "research-protocol.md")
        for phrase in ("营销与发布", "现实人物或近期事件", "割后复盘"):
            require(recipes, phrase, "response-recipes.md")
        for phrase in ("一票否决", "100分量表", "85—100"):
            require(rubric, phrase, "quality-rubric.md")
        for phrase in ("案件尚未进入实体审理", "不表示法院已经确认", "原题止损，母题续航"):
            require(case, phrase, "jingtian-2026.md")

        scenario_files = sorted((ROOT / "references/humor").glob("*.md"))
        if len(scenario_files) != 6:
            raise ValueError(f"幽默场景包应为6个，当前{len(scenario_files)}个")

        ledger = json.loads(read("references/source-ledger.json"))
        if ledger.get("research_cutoff") != "2026-09-09" or len(ledger.get("sources", [])) < 6:
            raise ValueError("source-ledger.json不完整")

        cases = json.loads(read("evals/cases.json"))
        if len(cases) < 40:
            raise ValueError(f"Skill行为评测至少40题，当前{len(cases)}题")

        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError(f"VERSION不是语义化版本：{version}")
        for owner, text in (("README.md", readme), ("CHANGELOG.md", changelog), ("SKILL.md", skill)):
            require(text, version, owner)
        require(openai, 'display_name: "割神模式"', "agents/openai.yaml")
        require(openai, "$geshen-mode", "agents/openai.yaml")
        for icon_key in ("icon_small", "icon_large"):
            match = re.search(rf'{icon_key}: "(.+)"', openai)
            if not match or not (ROOT / match.group(1)).is_file():
                raise ValueError(f"agents/openai.yaml的{icon_key}无效")

        for phrase in ("三分割味，七分真东西", "笑话可以上杠杆，证据不行", "案件尚未进入实体审理"):
            require(readme, phrase, "README.md")
        if "试玩" in readme or "playground" in readme.lower():
            raise ValueError("README.md仍包含试玩页定位")
        if (ROOT / "playground").is_dir() and any((ROOT / "playground").iterdir()):
            raise ValueError("项目仍包含playground文件")
        if readme.lstrip().startswith("!["):
            raise ValueError("README.md开头仍有图片")

    except (OSError, AttributeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL  {error}")
        return 1

    print(f"PASS  v{version} 纯Skill结构、frontmatter和精简README")
    print(f"PASS  6个模型、10条启发式、6个幽默场景包、{reference_count}个按需引用")
    print("PASS  研究协议、回答配方、质量量表、40题评测与UI元数据")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
