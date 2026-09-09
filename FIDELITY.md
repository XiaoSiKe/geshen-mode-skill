# 割神模式 v0.5.0 · 验证报告

**状态：Release Candidate PASS**
**验证日期：2026-09-09**

## 研究基础

- 7份调研底稿
- 2489行研究材料
- 调研索引记录289条来源引用
- 6个核心心智模型
- 10条决策启发式
- 6个幽默场景包

内容基准来自女娲 `sun-yuchen-perspective`，并结合本项目对最新对话、决策记录、时间线和景甜事件的增量调研。

## v0.5优化

### README定位

新版定位：

> 孙宇晨式注意力策略、叙事工程与高风险决策框架

首页直接说明研究规模、分析对象和使用场景。以下旧表达已删除，并有回归测试防止重新出现：

- 三分割味，七分真东西
- 这是一套人物思维Skill
- 给AI贴一张香蕉表情包
- 笑话可以上杠杆，证据不行
- 不能拿段子给证据补妆

README从197行收敛到167行。

### 使用场景

README明确给出六类任务：

- 产品发布
- 内容营销
- 品牌定位
- 危机沟通
- 创业决策
- 策略复盘

每类任务写明分析重点和最终交付，不再只描述抽象能力。

### 三层工作流

Skill内部术语统一为：

1. 证据层
2. 决策层
3. 表达层

原“事实核、割神核、喜剧核”不再作为正式架构名称。模式只能改变表达，不能改变事实标准。

### 表达DNA

根据参考Skill整理五种核心公式：

- 借势关联，保留“碰瓷造句法”的来源含义；
- 数字轰炸；
- 暴论与反问；
- 重新定义；
- 行动宣言。

每种公式补充适用场景和失效条件。数字必须来自用户题设或已核验来源；反问必须推进判断；行动宣言必须带验收数字和止损。

## 文案去AI味检查

README中的以下模式计数均为0：

- 此外
- 不仅
- 至关重要
- 深入探讨
- 赋能
- 无缝
- 彰显
- 标志着
- 格局
- 这不仅仅是
- 希望这对

## 测试结果

| 检查 | 结果 |
|---|---:|
| Agent Skills官方quick validator | PASS |
| 纯Skill结构和frontmatter | PASS |
| README专业定位 | PASS |
| 旧文案回归检查 | PASS |
| 三层工作流一致性 | PASS |
| 40题、10类评测集 | PASS |
| 参考回答评分 | 12/12 PASS |
| Python单元测试 | 23/23 PASS |
| 前向评测批次生成 | PASS |
| 临时安装 | PASS |
| 安装后22个Skill链接 | 全部可解析 |
| 纯Skill Release包 | 28个文件 |
| 双构建SHA-256 | 一致 |

## 可重复验证

```bash
python3 scripts/validate_skill.py
python3 scripts/run_evals.py
python3 scripts/run_evals.py --responses evals/reference-responses.jsonl --allow-partial
python3 scripts/build_eval_batch.py --category quality --limit 2
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
python3 scripts/smoke_install.py
python3 scripts/package_release.py --check
```

## 边界

- 静态合同评分不替代真实模型前向测试。
- 来源引用数量是调研索引统计，不代表289个完全独立来源。
- 景甜事件没有公开实体裁判，本项目不判断双方责任。
- 公开采访只能证明人物说过什么，不自动证明其叙述内容。
