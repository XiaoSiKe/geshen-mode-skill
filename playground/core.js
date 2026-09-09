(function attachGeshenCore(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.GeshenCore = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function createGeshenCore() {
  "use strict";

  const MODE_LABELS = { 0: "退出", 1: "正常", 2: "微割", 3: "全割", 4: "割后复盘" };

  const SCENARIOS = [
    {
      key: "local",
      pattern: /咖啡|奶茶|顾客|门店|到店|摆摊|早餐/,
      name: "线下获客",
      target: "附近真实顾客",
      metric: "7天新增到店、核销与复购意向",
      metaphors: ["社区共识节点", "线下流量清算所", "早间能源交易网络"],
      steps: [
        "今天：向10位附近顾客确认一个真正影响到店的理由。",
        "48小时内：围绕一个真实里程碑做一次社区活动，每个渠道使用独立核销码。",
        "第7天：比较到店、核销和复购意向，只保留有效渠道。",
      ],
      stop: "连续两个活动周期没有带来新增到店或留资，停止加预算，换钩子。",
    },
    {
      key: "workplace",
      pattern: /老板|周报|汇报|晋升|同事|会议/,
      name: "职场沟通",
      target: "真正有决定权的人",
      metric: "两周内的阅读、回复和决策完成率",
      metaphors: ["组织信息披露", "内部上市文件", "跨部门外交照会"],
      steps: [
        "今天：把结论、变化数字和需要的决定压到第一页。",
        "下次汇报前：针对决策人只保留一个明确请求。",
        "两周后：比较阅读与决策响应，删除没人使用的附录。",
      ],
      stop: "两轮汇报仍没有产生明确决定，就改沟通渠道或重新确认负责人。",
    },
    {
      key: "crisis",
      pattern: /吐槽|舆论|危机|负面|回应|抄袭|投诉/,
      name: "危机沟通",
      target: "受影响的用户与合作方",
      metric: "48小时内事实澄清率与负面扩散速度",
      metaphors: ["叙事风险委员会", "舆论防火墙", "公开信息清算庭"],
      steps: [
        "现在：列出已确认事实、未知事项和需要纠正的错误信息。",
        "24小时内：向真正受影响的人发布一次有证据的回应。",
        "48小时后：停止重复辩解，只更新新增事实和处理结果。",
      ],
      stop: "回应开始制造新误解或暴露无关隐私时，立即停止扩散并换到程序处理。",
    },
    {
      key: "daily",
      pattern: /健身|学习|坚持|习惯|减肥|整理/,
      name: "个人习惯",
      target: "下一次具体行动",
      metric: "连续7天完成率",
      metaphors: ["个人资产负债表", "习惯共识协议", "身体运营系统"],
      steps: [
        "今天：把任务缩到10分钟内可以完成。",
        "未来7天：固定同一触发时间，只记录完成或未完成。",
        "第8天：保留最容易坚持的动作，再增加一点难度。",
      ],
      stop: "连续三天失败，就继续缩小动作，不靠补偿性加码。",
    },
    {
      key: "startup",
      pattern: /创业|融资|投资人|商业模式|MVP/,
      name: "创业融资",
      target: "愿意付出时间或金钱的真实用户",
      metric: "14天访谈、激活、付费与留存",
      metaphors: ["资本认知升级", "产品主网上线", "商业模式压力测试"],
      steps: [
        "今天：写清一个具体用户和一个高频问题。",
        "72小时内：做一个只解决该问题的可用版本。",
        "第14天：用激活、付费和留存决定继续、调整或停止。",
      ],
      stop: "没有用户愿意持续使用或付费时，停止扩大叙事，回到问题验证。",
    },
    {
      key: "relationships",
      pattern: /对象|恋爱|分手|感情|关系|不回消息/,
      name: "关系沟通",
      target: "一段清晰且尊重边界的沟通",
      metric: "一次沟通后是否得到明确回应和可接受边界",
      metaphors: ["人类责任委员会", "双方共识协议", "历史账本停止写入"],
      steps: [
        "现在：分开事实、感受和自己的期待。",
        "下一次沟通：只提出一个明确问题或边界。",
        "得到回应后：按对方真实选择行动，不用公开施压换答案。",
      ],
      stop: "对方明确拒绝、沉默或要求停止联系时，不再追加沟通。",
    },
    {
      key: "product",
      pattern: /产品|用户|发布|增长|预算|转化/,
      name: "产品增长",
      target: "可再次触达的真实用户",
      metric: "7天激活与留存",
      metaphors: ["早期生态节点", "注意力结算网络", "用户共识层"],
      steps: [
        "今天：访谈10位真实用户，找出一句能复述的价值。",
        "48小时内：集中一个渠道发布一个可验证的里程碑。",
        "第7天：比较激活与留存，砍掉只有曝光没有后续动作的渠道。",
      ],
      stop: "连续两个观察周期激活或留存不改善，停止加预算，换钩子或产品路径。",
    },
  ];

  const RISK_RULES = [
    {
      pattern: /停药|用药|剂量|诊断|治疗方案/,
      refusal: "我不能替医生决定用药、停药或治疗方案。",
      alternative: "请联系医生或药师核对；出现紧急症状时使用当地急救服务。这个问题不进入割味模式。",
    },
    {
      pattern: /拉盘|操纵市场|洗盘|内幕交易|偷偷建仓/,
      refusal: "我不能提供操纵市场、内幕交易或规避监管的方法。",
      alternative: "可以改为分析合法的信息披露、流动性风险、持仓集中度和市场教育。",
    },
    {
      pattern: /必涨|稳赚|保证.{0,8}(十倍|收益)|一年.{0,5}十倍/,
      refusal: "没有任何币种可以保证收益，我也不能替你给出确定性重仓指令。",
      alternative: "可以比较用途、流动性、集中度、代币释放、合约权限和监管风险。",
    },
    {
      pattern: /让.{0,8}后悔|公开羞辱|骚扰|报复/,
      refusal: "我不能帮助公开羞辱、骚扰或报复他人。",
      alternative: "可以把问题改成一次清晰沟通、边界设置和停止联系条件。",
    },
  ];

  const EXTERNAL_FACT_PATTERN = /景甜|孙宇晨|赵长鹏|\bCZ\b|币价|Gas费|TRON转账|案件|诉讼|法院/iu;

  function hash(text) {
    let value = 2166136261;
    for (const char of text) {
      value ^= char.codePointAt(0);
      value = Math.imul(value, 16777619);
    }
    return value >>> 0;
  }

  function pick(items, seed, offset = 0) {
    return items[(seed + offset) % items.length];
  }

  function scenarioFor(prompt) {
    return SCENARIOS.find((scenario) => scenario.pattern.test(prompt)) || {
      key: "general",
      name: "通用策略",
      target: "一个可观察结果",
      metric: "7天内的真实转化",
      metaphors: ["注意力结算网络", "行动公开市场", "结果审计台"],
      steps: [
        "今天：把目标改写成一个可观察结果。",
        "48小时内：选择一个真实钩子和一个可追踪渠道。",
        "第7天：比较行动与转化，停止无效投入。",
      ],
      stop: "连续两个观察周期没有转化，就缩小目标或更换路径。",
    };
  }

  function resolveControl(prompt, currentMode) {
    if (/有几级|各级.{0,4}区别/.test(prompt)) return { kind: "info", mode: currentMode };
    if (/退出|别演了|切回正常/.test(prompt)) return { kind: "exit", mode: 0 };
    if (/再狠点|再割一点/.test(prompt)) return { kind: "relative", mode: Math.min(3, currentMode + 1) };
    if (/收一点|少演点/.test(prompt)) return { kind: "relative", mode: Math.max(1, currentMode - 1) };
    if (/4级|割后复盘|先演.{0,4}再拆/.test(prompt)) return { kind: "mode", mode: 4 };
    if (/3级|全割|割味拉满/.test(prompt)) return { kind: "mode", mode: 3 };
    if (/1级|正常模式|客观分析/.test(prompt)) return { kind: "mode", mode: 1 };
    if (/2级|微割|割神模式|孙割视角|孙割会怎么做/.test(prompt)) return { kind: "mode", mode: 2 };
    return { kind: "none", mode: currentMode };
  }

  function isControlOnly(prompt) {
    return /^(再狠点|再割一点|收一点|少演点|退出|别演了|切回正常|割后复盘)[。！!？?\s]*$/.test(prompt);
  }

  function makePlan(prompt) {
    const scenario = scenarioFor(prompt);
    const seed = hash(prompt);
    return {
      scenario,
      seed,
      metaphor: pick(scenario.metaphors, seed),
      conclusion: `真正目标不是把声音放大，而是让${scenario.target}完成下一步动作。`,
      steps: scenario.steps,
      metric: scenario.metric,
      stop: scenario.stop,
    };
  }

  function promptAnchors(prompt) {
    return [...new Set(prompt.match(/\d+(?:\.\d+)?(?:元|万|个|位|天|周|小时|%)?/g) || [])];
  }

  function parodyFor(plan, mode) {
    const micro = [
      `你缺的不是曝光，是${plan.metaphor}还没完成结算。先让一个真实数字移动，再谈放大。`,
      `现在不是没人关注，是${plan.metaphor}还停在内测。先做出可验证里程碑，别用形容词融资。`,
      `这不是流量问题，是${plan.metaphor}缺少第一个公开节点。数字先上线，口号晚一点。`,
    ];
    const full = [
      `普通人看到的是小问题，我看到的是${plan.metaphor}的全球首发。没有转化的流量不是资产，是替平台做慈善。七天把真实数字做出来；没有数字，就别开发布会。🚀`,
      `这件事最大的风险不是失败，是失败得没有标题。把${plan.metaphor}做成一个公开里程碑，让数字自己走上台；数字不动，项目立即退市。📈`,
      `市场不欠你掌声，只欠你一次能被验证的行动。${plan.metaphor}今天进入价格发现：先做、再测、到止损线就关灯。🌞`,
    ];
    return pick(mode === 2 ? micro : full, plan.seed, mode);
  }

  function cardsToText(cards) {
    return cards.map((card) => `${card.label}\n${card.text}`).join("\n\n");
  }

  class GeshenSession {
    constructor(initialMode = 2) {
      this.currentMode = initialMode;
      this.previousMode = initialMode;
      this.parodyNoticeShown = false;
      this.recentStyleSignatures = [];
      this.lastPrompt = "";
      this.lastResult = null;
    }

    setMode(mode) {
      if (!Number.isInteger(mode) || mode < 0 || mode > 4) {
        throw new RangeError("mode必须是0到4的整数");
      }
      if (mode !== 4) this.previousMode = mode;
      this.currentMode = mode;
    }

    compile(rawPrompt, options = {}) {
      let prompt = String(rawPrompt || "").trim();
      if (!prompt) return { ok: false, error: "先给我一个问题。没有标的，怎么收注意力？" };

      if (options.mode !== undefined) this.setMode(options.mode);
      const control = resolveControl(prompt, this.currentMode);

      if (control.kind === "info") {
        const cards = [{ label: "五档割味", text: "0级退出；1级正常；2级微割；3级全割；4级割后复盘。这里只介绍模式，不改变当前状态。" }];
        return this.finish({ mode: this.currentMode, scenario: "模式说明", cards }, prompt, false);
      }

      if (control.kind === "exit" && isControlOnly(prompt)) {
        this.currentMode = 0;
        const cards = [{ label: "普通模式", text: "已退出割神模式。后续不会因为提到孙宇晨或TRON自动复活。" }];
        return this.finish({ mode: 0, scenario: "退出", cards }, prompt, false);
      }

      if (control.kind === "relative") {
        this.currentMode = control.mode;
        if (isControlOnly(prompt) && this.lastPrompt) prompt = this.lastPrompt;
      } else if (control.kind === "mode") {
        this.currentMode = control.mode;
      }

      if (this.currentMode === 4 && isControlOnly(prompt)) {
        if (!this.lastResult) {
          const cards = [{ label: "割后复盘", text: "上一条没有割神输出可复盘。" }];
          return this.finish({ mode: 4, scenario: "复盘", cards }, prompt, false);
        }
        const cards = [{ label: "割后复盘", text: `上一条使用了${this.lastResult.scenario}场景。段子负责记忆，行动、指标和止损负责交付。` }];
        const result = this.finish({ mode: 4, scenario: "复盘", cards }, prompt, false);
        this.currentMode = this.previousMode;
        return result;
      }

      const risk = RISK_RULES.find((rule) => rule.pattern.test(prompt));
      if (risk) {
        const cards = [
          { label: "安全边界", text: risk.refusal },
          { label: "合法替代", text: risk.alternative },
        ];
        return this.finish({ mode: 1, scenario: "安全降级", cards, refused: true }, prompt, false);
      }

      if (EXTERNAL_FACT_PATTERN.test(prompt)) {
        const cards = [
          { label: "事实核降级", text: "当前离线试玩无法核验外部人物、行情或案件状态，因此降到1级，不用戏仿填补事实空白。" },
          { label: "下一步", text: "在完整Skill中先查原始来源、程序材料和可靠报道，再区分✅已确认、🟡单方说法、🔵框架推断与🎭戏仿生成。" },
        ];
        return this.finish({ mode: 1, scenario: "外部事实", cards, requiresSearch: true }, prompt, false);
      }

      const plan = makePlan(prompt);
      const mode = this.currentMode;
      const cards = [];

      if (mode >= 3 && !this.parodyNoticeShown) {
        cards.push({ label: "模式提示", text: "以下是基于公开资料提炼的孙宇晨式戏仿，不代表本人观点。" });
        this.parodyNoticeShown = true;
      }

      if (mode >= 2) {
        cards.push({ label: mode === 2 ? "2级微割" : "🎭 戏仿生成", text: parodyFor(plan, mode), className: "parody" });
      }

      const anchors = promptAnchors(prompt);
      if (anchors.length) {
        cards.push({ label: "题设锚点", text: `用户给出的数字：${anchors.join("、")}。它们按题设使用，不扩展成外部事实。` });
      }

      cards.push(
        { label: "正常结论", text: plan.conclusion },
        { label: "三步动作", text: plan.steps.join("\n") },
        { label: "转化指标", text: plan.metric },
        { label: "止损线", text: plan.stop }
      );

      if (mode === 4) {
        cards.push({ label: "割后复盘", text: `“${plan.metaphor}”使用小事升维；公开数字来自注意力套利；三步动作保留真实执行。最大风险是有围观、没转化。` });
      }

      const result = this.finish({ mode, scenario: plan.scenario.name, scenarioKey: plan.scenario.key, cards }, prompt, true);
      if (mode === 4) this.currentMode = this.previousMode;
      return result;
    }

    finish(result, prompt, rememberPrompt) {
      const complete = { ok: true, refused: false, requiresSearch: false, modeLabel: MODE_LABELS[result.mode], ...result };
      complete.text = cardsToText(complete.cards);
      if (rememberPrompt) this.lastPrompt = prompt;
      if (!["模式说明", "退出", "复盘"].includes(result.scenario)) this.lastResult = complete;
      return complete;
    }
  }

  return {
    MODE_LABELS,
    SCENARIOS,
    GeshenSession,
    createSession: (mode = 2) => new GeshenSession(mode),
    scenarioFor,
  };
});
