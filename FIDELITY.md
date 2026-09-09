# 割神模式 v0.2.0 · 验证报告

**状态：Release Candidate PASS**
**验证日期：2026-09-09**

## 总览

| 验证面 | 结果 | 实际证据 |
|---|---:|---|
| Agent Skills格式 | PASS | 官方quick validator通过 |
| 包结构 | PASS | 版本、frontmatter、UI元数据、引用路径全部有效 |
| 轻量入口 | PASS | `SKILL.md` 从516行降到169行 |
| Progressive disclosure | PASS | 11个按需引用、6个场景包 |
| 行为评测集 | PASS | 30题、8类、ID唯一、字段完整 |
| 参考回答评分 | 12/12 PASS | 路由、策略、事实、投资与关系边界 |
| 单元测试 | 18/18 PASS | Skill、评测器、试玩页合同 |
| 临时安装烟雾测试 | PASS | 复制到临时Skill目录后重新验证 |
| Python / JavaScript语法 | PASS | `compileall` 与 `node --check` |
| 桌面浏览器 | PASS | 页面加载、交互、3级输出、复制状态 |
| 移动端390px | PASS | 无横向溢出，模式按钮与内容正常 |
| 可访问性 | PASS | axe WCAG 2A/2AA：0 violations；1项渐变背景对比度无法自动判定 |

## 五条深化路线的验证

### 1. 轻量运行时

- `SKILL.md` 只保留激活、路由、事实核、模型选择、硬门和安全边界。
- 模型、幽默、输出合同、景甜事件分别拥有独立reference。
- 普通问答不会加载全部案例和场景包。

### 2. 行为评测

`evals/cases.json` 包含30题：

- routing 8
- state 4
- strategy 5
- facts 5
- finance 3
- boundaries 2
- debrief 2
- inference 1

`scripts/run_evals.py` 可以：

- 验证评测集结构；
- 对捕获的Agent回答评分；
- 检查必要词、禁用词、事实标签、明确拒绝和策略合同；
- 支持部分回答集，用于快速回归。

说明：仓库内12条reference responses是评分器回归样本，不冒充实时模型运行。真实模型保真仍需在安装环境中定期前向测试。

### 3. 定向研究

新增 `07-v0.2-deepening.md` 和结构化 `source-ledger.json`。

结论：

- AI决策保持为有限证据启发式，不升级第7模型。
- 表达DNA增加“商业确定性 vs 私人脆弱性”。
- “关灯”改为“原题止损，母题续航”，不误写成彻底停止表达。
- 明确哪些场景更容易出现收束、程序语言或换轨。

### 4. 幽默系统

新增一个编译器和六个场景包：

- 营销
- 创业
- 危机
- 职场
- 日常
- 关系

测试要求：删掉笑话后，策略仍保留目标、三步、转化指标和止损。

### 5. 产品化

- `agents/openai.yaml`
- 品牌图标与README横幅
- 五档离线试玩页
- GitHub Actions
- `VERSION` 与 `CHANGELOG.md`
- 临时安装烟雾测试
- 示例画廊

## 浏览器实测

地址：`http://127.0.0.1:4173/playground/`

桌面：

- 页面标题正确；
- 正文非空；
- 无错误覆盖层；
- 控制台无捕获错误；
- 0—4级全部可访问；
- 3级选择后生成“线下获客”结果；
- 输出含戏仿、正常结论、三步动作、指标和止损；
- 复制按钮由disabled变为enabled。

移动端：

- viewport：390 × 844；
- document scrollWidth：390；
- 无横向溢出；
- 模式按钮变为两列；
- 主视觉、输入区、输出区和三核卡片正常堆叠。

## 可重复命令

```bash
python3 scripts/validate_skill.py
python3 scripts/run_evals.py
python3 scripts/run_evals.py --responses evals/reference-responses.jsonl --allow-partial
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
node --check playground/app.js
python3 scripts/smoke_install.py
```

## 边界

- 景甜事件尚无公开实体裁判，本项目不判断双方责任。
- 公开采访只能证明孙宇晨说过什么，不自动证明公司AI规模和私聊内容。
- 网页试玩是离线输出合同演示，不调用LLM，也不查询实时事实。
- 参考回答测试验证评分器和合同，不等于对所有模型、所有运行环境的保证。
