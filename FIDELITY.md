# 割神模式 v0.4.0 · 验证报告

**状态：Release Candidate PASS**
**验证日期：2026-09-09**

## 定位检查

v0.4只交付人物思维Skill：

- 根目录入口：`SKILL.md`
- UI元数据：`agents/openai.yaml`
- 图标：`assets/icon.svg`
- 模型、协议、案例与调研：`references/`

项目不包含Web页面、浏览器应用或交互演示。Release安装包也不包含CI、测试、评测、文档站或开发脚本。

## 结果

| 验证面 | 结果 |
|---|---:|
| Agent Skills官方quick validator | PASS |
| 纯Skill结构与frontmatter | PASS |
| `SKILL.md`轻量入口 | PASS |
| README简洁度 | PASS |
| 6个模型、10条启发式 | PASS |
| 6个幽默场景包 | PASS |
| 事实研究协议 | PASS |
| 7类回答配方 | PASS |
| 100分质量量表 | PASS |
| 行为评测集 | 40题、10类 |
| 参考回答评分 | 12/12 PASS |
| Python单元测试 | 21/21 PASS |
| 前向评测批次生成器 | PASS |
| 临时安装 | PASS |
| 纯Skill Release包 | 28个文件 |
| 双构建SHA-256 | 一致 |

## 本轮深化

### 事实研究协议

`references/research-protocol.md` 增加：

- 搜索前先定义最多三个事实问题；
- 法院、监管、原帖、采访、媒体与评论的来源优先级；
- 证据卡；
- 事实、单方说法、框架推断和戏仿的判定；
- 时效、冲突、引语与工具失败处理；
- 现实人物隐私边界。

### 回答配方

`references/response-recipes.md` 提供七类最低交付：

- 营销与发布
- 危机沟通
- 现实人物或近期事件
- 普通策略
- 割后复盘
- 多视角比较
- 简短问答

配方不是统一模板。短问题不会被强制写成三步全球发布会。

### 质量量表

`references/quality-rubric.md` 包含：

- 编造事实、突破边界和空洞口号的一票否决；
- 事实30分、模型20分、行动20分、表达15分、克制15分；
- 85分交付线；
- 只输出总分、否决项、最弱维度和一处修改，不要求隐藏思维过程。

### Skill行为评测

`evals/cases.json` 从30题扩展到40题，新增：

- 来源冲突
- 实时价格
- 引语核验
- 缺少一手来源
- 隐私材料
- 幽默剂量
- 简短回答
- 多视角比较
- 空洞口号
- 简单问题过度回答

`scripts/build_eval_batch.py` 可以按类别生成Markdown评测批次，或生成待填回答的JSONL。

## 安装包检查

`scripts/package_release.py` 使用运行文件白名单：

- `SKILL.md`
- `README.md`
- `LICENSE`
- `VERSION`
- `agents/`
- `assets/`
- `references/`

明确排除：

- `.github/`
- `docs/`
- `evals/`
- `examples/`
- `scripts/`
- `tests/`
- 任何Web页面

临时安装后重新检查frontmatter、22个链接引用和禁止目录。

## 可重复验证

```bash
python3 scripts/validate_skill.py
python3 scripts/run_evals.py
python3 scripts/run_evals.py --responses evals/reference-responses.jsonl --allow-partial
python3 scripts/build_eval_batch.py --category research --limit 2
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
python3 scripts/smoke_install.py
python3 scripts/package_release.py --check
```

## 边界

- 静态合同评分不替代真实模型前向测试。
- 参考回答只验证评分器，不冒充孙宇晨本人。
- 景甜事件没有公开实体裁判，本项目不判断双方责任。
- 公开采访只能证明当事人说过什么，不自动证明其叙述内容。
