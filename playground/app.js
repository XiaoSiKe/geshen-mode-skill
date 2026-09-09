const promptInput = document.querySelector("#prompt");
const generateButton = document.querySelector("#generate");
const copyButton = document.querySelector("#copy");
const status = document.querySelector("#status");
const cards = document.querySelector("#cards");
const resultTitle = document.querySelector("#result-title");
const modeButtons = [...document.querySelectorAll(".mode")];
const presetButtons = [...document.querySelectorAll(".preset")];

let currentMode = 2;
let lastText = "";

const scenarioRules = [
  { pattern: /咖啡|奶茶|顾客|门店|到店/, name: "线下获客", target: "附近真实顾客", metric: "7天新增到店与复购意向", metaphor: "社区共识节点" },
  { pattern: /老板|周报|汇报|晋升|同事/, name: "职场沟通", target: "真正有决定权的人", metric: "一周内获得明确决策或资源", metaphor: "组织信息披露" },
  { pattern: /吐槽|舆论|危机|负面|回应/, name: "危机沟通", target: "受影响的用户与合作方", metric: "48小时内澄清率与负面扩散速度", metaphor: "叙事风险委员会" },
  { pattern: /健身|学习|坚持|习惯|减肥/, name: "个人习惯", target: "下一次具体行动", metric: "连续7天完成率", metaphor: "个人资产负债表" },
  { pattern: /产品|用户|发布|增长|预算/, name: "产品增长", target: "可再次触达的真实用户", metric: "7天激活与留存", metaphor: "早期生态节点" },
];

function pickScenario(prompt) {
  return (
    scenarioRules.find((rule) => rule.pattern.test(prompt)) || {
      name: "通用策略",
      target: "一个可观察结果",
      metric: "7天内的真实转化",
      metaphor: "注意力结算网络",
    }
  );
}

function planFor(prompt) {
  const scenario = pickScenario(prompt);
  return {
    scenario,
    conclusion: `真正目标不是把声音放大，而是让${scenario.target}完成下一步动作。`,
    steps: [
      "今天：写出一个真实、反常、能被一句话复述的钩子。",
      "48小时内：把预算集中到一个可追踪渠道，发布一次明确行动。",
      "第7天：比较触达、转化和留存，砍掉没有后续动作的曝光。",
    ],
    metric: scenario.metric,
    stop: "连续两个观察周期没有转化，就停止加预算，换钩子或换渠道。",
  };
}

function parodyFor(plan, mode) {
  const subject = plan.scenario.metaphor;
  if (mode === 2) {
    return `你缺的不是曝光，是${subject}还没完成结算。先让一个真实数字开始移动，再让围观群众替你解释为什么。`;
  }
  return `普通人看到的是一个小问题，我看到的是${subject}的全球首发。没有转化的流量不是资产，是你替平台做慈善。七天，把真实数字做出来；没有数字，就别开发布会。🚀`;
}

function buildOutput(prompt, mode) {
  const plan = planFor(prompt);
  if (mode === 0) {
    return [
      { label: "普通回答", text: `${plan.conclusion}\n\n${plan.steps.join("\n")}\n\n指标：${plan.metric}\n止损：${plan.stop}` },
    ];
  }

  if (mode === 1) {
    return [
      { label: "🔵 框架推断", text: "这是把孙宇晨式注意力模型迁移到用户题设，不代表本人公开立场。" },
      { label: "正常结论", text: plan.conclusion },
      { label: "三步动作", text: plan.steps.join("\n") },
      { label: "转化指标", text: plan.metric },
      { label: "止损线", text: plan.stop },
    ];
  }

  const output = [
    { label: mode === 2 ? "2级微割" : "🎭 戏仿生成", text: parodyFor(plan, mode), className: "parody" },
    { label: "正常结论", text: plan.conclusion },
    { label: "三步动作", text: plan.steps.join("\n") },
    { label: "转化指标", text: plan.metric },
    { label: "止损线", text: plan.stop },
  ];

  if (mode === 4) {
    output.push({
      label: "割后复盘",
      text:
        "“全球首发”使用小事升维；“平台慈善”使用负面翻转；“真实数字”来自注意力套利。\n" +
        "可执行部分仍是：单一钩子、集中渠道、七天复盘。最大风险是有围观、没转化。",
    });
  }
  return output;
}

function render() {
  const prompt = promptInput.value.trim();
  status.textContent = "";

  if (!prompt) {
    status.textContent = "先给我一个问题。没有标的，怎么收注意力？";
    promptInput.focus();
    return;
  }

  const output = buildOutput(prompt, currentMode);
  const fragment = document.createDocumentFragment();
  lastText = output.map((item) => `${item.label}\n${item.text}`).join("\n\n");

  output.forEach((item) => {
    const card = document.createElement("article");
    card.className = `card ${item.className || ""}`.trim();
    const label = document.createElement("strong");
    label.textContent = item.label;
    const text = document.createElement("p");
    text.textContent = item.text;
    card.append(label, text);
    fragment.append(card);
  });

  cards.replaceChildren(fragment);
  resultTitle.textContent = `${currentMode}级输出 · ${pickScenario(prompt).name}`;
  copyButton.disabled = false;
  document.querySelector("#result").scrollIntoView({ behavior: "smooth", block: "start" });
}

modeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    currentMode = Number(button.dataset.mode);
    modeButtons.forEach((item) => {
      const selected = item === button;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-checked", String(selected));
    });
  });
});

presetButtons.forEach((button) => {
  button.addEventListener("click", () => {
    promptInput.value = button.dataset.prompt;
    promptInput.focus();
  });
});

generateButton.addEventListener("click", render);

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(lastText);
    status.textContent = "已复制。注意力可以转发，责任不能。";
  } catch {
    status.textContent = "浏览器没给剪贴板权限，请手动复制。";
  }
});
