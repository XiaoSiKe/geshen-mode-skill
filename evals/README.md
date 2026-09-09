# Skill行为评测

本目录测试Agent回答，不运行网页或模拟产品。

## 文件

- `cases.json`：40个真实使用场景及最低合同。
- `reference-responses.jsonl`：评分器回归样本，不冒充实时模型回答。
- `response-schema.json`：捕获回答的最小数据格式。

## 生成前向评测批次

```bash
python3 scripts/build_eval_batch.py --limit 10
python3 scripts/build_eval_batch.py --category research
python3 scripts/build_eval_batch.py --format jsonl > /tmp/geshen-responses.jsonl
```

Markdown输出同时包含答题提示和评测合同。运行真实前向测试时，只把“提示”发送给答题Agent，评测合同留给独立评分者。

JSONL输出中的 `response` 初始为空。填入完整回答后评分：

```bash
python3 scripts/run_evals.py --responses /tmp/geshen-responses.jsonl
```

## 覆盖

- 激活与误触发
- 跨轮状态
- 营销和策略
- 现实人物与近期事实
- 景甜事件边界
- 投资、市场操纵、隐私和医疗
- 研究冲突与引语核验
- 幽默剂量、简短回答和多视角比较

静态评分只能检查可观察合同。人物保真度和建议质量仍需要独立Agent评审。
