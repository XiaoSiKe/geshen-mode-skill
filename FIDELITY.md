# 割神模式 v0.3.0 · 验证报告

**状态：Release Candidate PASS**
**验证日期：2026-09-09**

## 总览

| 验证面 | 结果 | 实际证据 |
|---|---:|---|
| Agent Skills格式 | PASS | 官方quick validator通过 |
| 包结构 | PASS | 版本、frontmatter、UI元数据、引用路径有效 |
| README开头图片 | PASS | 文档不再以Markdown图片开头 |
| Python单元测试 | 20/20 PASS | Skill、评测器、试玩页合同 |
| Node运行核心测试 | 12/12 PASS | 模式状态、安全降级、场景和错误路径 |
| Agent行为评测 | PASS | 30题、8类；12条参考回答12/12 |
| 可执行运行时评测 | PASS | 17组场景、162项断言 |
| 临时安装烟雾测试 | PASS | 复制到临时Skill目录后重新验证 |
| Release包 | PASS | 48个文件、版本一致、无临时目录 |
| Python / JavaScript语法 | PASS | `compileall` 与三个Node语法检查 |
| 桌面浏览器 | PASS | 页面加载、共享核心、模式切换和降级 |
| 移动端390px | PASS | 无横向溢出 |
| 可访问性 | PASS | axe WCAG 2A/2AA：0 violations；渐变对比度无法自动判定 |

## v0.3深化目标

v0.2已经完成progressive disclosure，但试玩页仍自己维护一套模式和安全规则。v0.3把这份重复逻辑抽到 `playground/core.js`：

```text
GeshenSession
├── 浏览器app.js
├── Node test runner
├── 17组runtime evals
└── CI
```

现在以下行为是执行结果，不只是文档承诺：

- 0级退出持续到再次激活。
- “再狠点”上调一级，“收一点”下调一级。
- 3级模式提示同一会话只出现一次。
- 4级完成后恢复之前模式。
- 没有上一条回答时不现场编造复盘。
- 医疗、市场操纵、确定收益和骚扰请求先降到1级。
- 景甜、币价和案件等外部事实在离线试玩中要求搜索，不用段子补空白。
- 用户题设中的数字进入独立锚点，不扩展成外部事实。

## 运行时测试

### Node核心测试

12项覆盖：

- 模式说明不改变状态；
- 退出持续；
- 相对升降级；
- 上一题复用；
- 3级声明去重；
- 4级恢复；
- 空复盘；
- 高风险降级；
- 外部事实降级；
- 策略合同；
- 多场景识别；
- 非法模式和空输入。

### 数据驱动评测

`evals/runtime-cases.json` 包含17组场景和多轮对话。`scripts/run_runtime_evals.mjs` 对实际 `GeshenSession` 输出执行162项断言。

第一次运行发现两个问题并修复：

1. 用户给出的“30个用户、3000元”在输出中丢失。现在增加题设锚点。
2. 评测把“不要公开施压”误判成鼓励施压。现在禁用模式只匹配正向危险指令。

## 浏览器实测

地址：`http://127.0.0.1:4173/playground/`

验证结果：

- v0.3.0标题显示正确；
- `core.js`、`app.js`、CSS和favicon全部200；
- 页面非空，无错误覆盖层；
- 3级产品增长保留“30个、3000元”；
- 第二次3级生成不重复模式提示；
- 景甜事实请求输出“1级 · 外部事实”；
- 拉盘请求输出“1级 · 安全降级”；
- 390px viewport下scrollWidth为390；
- axe WCAG 2A/2AA为0 violations；
- 浏览器错误列表为空。

## Release包

`scripts/package_release.py`：

- 按固定顺序收集文件；
- 使用固定Zip时间戳；
- 保留可执行权限；
- 排除Git、dist和缓存；
- 验证版本与必需文件；
- CI使用临时目录检查；
- 正式Release附加 `geshen-mode-v0.3.0.zip`。

## 可重复命令

```bash
python3 scripts/validate_skill.py
python3 scripts/run_evals.py
python3 scripts/run_evals.py --responses evals/reference-responses.jsonl --allow-partial
python3 -m unittest discover -s tests -v
node --test tests/runtime.test.cjs
node scripts/run_runtime_evals.mjs
python3 -m compileall -q scripts tests
node --check playground/core.js
node --check playground/app.js
node --check scripts/run_runtime_evals.mjs
python3 scripts/smoke_install.py
python3 scripts/package_release.py --check
```

## 边界

- `core.js` 验证的是离线输出合同，不是完整LLM本身。
- 参考回答用于评分器回归，不冒充实时模型评测。
- 景甜事件仍没有公开实体裁判，本项目不判断双方责任。
- 渐变背景导致axe无法自动计算部分文字对比度，但没有报告确定违规。
