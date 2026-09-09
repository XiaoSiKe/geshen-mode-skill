<div align="center">

# 割神模式（孙割Skill）

### 三分割味，七分真东西。

**v0.4.0**

[![CI](https://github.com/XiaoSiKe/geshen-mode-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/XiaoSiKe/geshen-mode-skill/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/XiaoSiKe/geshen-mode-skill?color=ffb000)](https://github.com/XiaoSiKe/geshen-mode-skill/releases)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-6C47FF)](#安装)
[![License](https://img.shields.io/badge/License-MIT-black)](LICENSE)

基于孙宇晨公开言论和行为模式，分析注意力、叙事、营销与危机沟通。

</div>

---

## 这是什么

这是一套人物思维Skill。

它不是给AI贴一张香蕉表情包，然后让它逢事就喊“All in”。真正被蒸馏的是：

- 怎么把一笔支出变成公共事件；
- 怎么争夺“这件事应该如何解释”的权力；
- 怎么借身份、数字和速度放大分发；
- 什么时候继续说，什么时候关掉原题、切换母题。

回答先过事实核，再选模型，最后才加幽默。

笑话可以上杠杆，证据不行。

## 适合做什么

| 场景 | 它会问 |
|---|---|
| 产品发布 | 为什么这还不是一个值得传播的事件？ |
| 内容营销 | 哪个真实数字可以成为标题？ |
| 品牌危机 | 应该回应、纠错、沉默还是换轨？ |
| 创业与合作 | 哪个身份或渠道能放大分发？ |
| 割后复盘 | 哪句是模型，哪句只是节目效果？ |

普通币价、Gas费和TRON技术问题不会自动进入角色。

## 五档割味

| 等级 | 模式 | 输出 |
|---|---|---|
| 0 | 退出 | 普通助手，不自动复活 |
| 1 | 正常 | 第三人称分析，只讲证据、模型和局限 |
| 2 | 微割 | 默认；70%能执行，30%想截图 |
| 3 | 全割 | 沉浸式戏仿，但保留行动、指标和止损 |
| 4 | 割后复盘 | 先演，再拆模型、行动和风险 |

```text
割神模式，分析这个产品发布
2级微割，帮我改营销方案
全割模式，给我的早餐摊做定位
把刚才那段割后复盘
别演了
```

## 工作方式

```text
问题
  ↓
事实核：查人物、数字、时间和程序状态
  ↓
割神核：选择1—3个心智模型
  ↓
行动骨架：目标、三步、指标、止损
  ↓
喜剧层：按0—4级控制剂量
```

涉及现实人物争议时，强制区分：

- ✅ 已确认
- 🟡 单方说法
- 🔵 框架推断
- 🎭 戏仿生成

无法核验就降到1级。不能拿段子给证据补妆。

## 6个核心模型

| 模型 | 核心问题 |
|---|---|
| 注意力套利 | 这笔钱能买到多少可转化注意力？ |
| 叙事覆盖 | 谁拥有问题的定义权？ |
| 身份杠杆 | 哪个真实身份能放大影响力？ |
| 场景切换 | 面前的人能奖励、伤害，还是只在围观？ |
| 快速复制 + 品牌溢价 | 市场已经替我验证了什么？ |
| 金钱万能钥匙 | 哪个障碍有价格，哪个东西买不到？ |

完整证据、局限与10条启发式见 [core-models.md](references/core-models.md)。

## 一个例子

问题：

> 产品上线三天，只有30个用户，预算3000元。

2级微割：

> 30个用户不叫失败，叫创世区块已经正常出块。3000元也不是广告预算，是注意力种子轮。
>
> 真正目标是7天内找到一个可复述的传播钩子，并把30个人变成能反馈、可再次触达的种子用户。
>
> 今天访谈10个人；48小时内公开一个真实里程碑；第7天砍掉没有激活和留存的渠道。
>
> 指标看激活与7日留存。连续两个周期不改善，停止加预算，换钩子。

删掉第一段，建议仍然成立。这才算幽默，不算放烟花。

## 景甜事件怎么处理

2026年的相关事件是重要案例，也是最容易写过界的地方。

- 代理律师公开称案件已立案并申请财产保全，景甜方提出管辖权异议。
- 案件尚未进入实体审理，没有公开最终裁判。
- 《我的女友景甜》中的关系、医疗、金额和Claude对话细节属于孙宇晨单方叙述。
- 景甜及工作室的回应是另一方立场，也不等于法院认定。
- “关灯”不代表和解、撤诉或结案。更准确的框架是“原题止损，母题续航”。

在这个案例里，笑点只能落在传播机制、叙事结构和AI角色上，不消费生育、医疗和私人身体细节。

完整材料见 [jingtian-2026.md](references/cases/jingtian-2026.md) 和 [source-ledger.json](references/source-ledger.json)。

## v0.4深化了什么

- 删除与Skill运行无关的Web层，项目回到人物思维Skill本身。
- 新增事实研究协议：搜索问题、证据卡、时效、冲突和失败降级。
- 新增七类回答配方，避免所有问题套同一副“三步走”。
- 新增100分质量量表和一票否决。
- 行为评测扩展到40题，覆盖触发、事实、策略、边界、研究和表达质量。
- Release压缩包只包含Skill运行所需文件，不再打包CI、测试和开发工具。

## 安装

```bash
npx skills add XiaoSiKe/geshen-mode-skill
```

也可以从 [Releases](https://github.com/XiaoSiKe/geshen-mode-skill/releases) 下载Skill压缩包。

## 结构

```text
geshen-mode-skill/
├── SKILL.md
├── agents/openai.yaml
├── assets/icon.svg
└── references/
    ├── core-models.md
    ├── humor-engine.md
    ├── output-contracts.md
    ├── research-protocol.md
    ├── response-recipes.md
    ├── quality-rubric.md
    ├── cases/
    ├── humor/
    └── research/
```

Skill入口只保留路由和硬边界，详细内容按任务加载。

## 测试

```bash
python3 scripts/validate_skill.py
python3 scripts/run_evals.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_install.py
python3 scripts/package_release.py --check
```

测试覆盖格式、引用、模式、事实边界、40题评测集、评分器、安装包和版本一致性。结果见 [FIDELITY.md](FIDELITY.md)。

## 声明

本项目是研究与戏仿作品，与孙宇晨、景甜、TRON、Anthropic及相关机构无隶属或授权关系。

它不构成投资建议、法律意见，也不替未决争议站队。

---

<div align="center">

**不是所有热点都值得蹭。**

如果一定要蹭，先把事实查清楚。

</div>
