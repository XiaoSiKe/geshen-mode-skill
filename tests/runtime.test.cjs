const test = require("node:test");
const assert = require("node:assert/strict");
const { createSession, scenarioFor } = require("../playground/core.js");

test("mode info does not change current mode", () => {
  const session = createSession(3);
  const result = session.compile("有几级割味？");
  assert.equal(result.mode, 3);
  assert.equal(session.currentMode, 3);
  assert.match(result.text, /0级退出.*4级割后复盘/);
});

test("exit persists across following turns", () => {
  const session = createSession(3);
  assert.equal(session.compile("别演了").mode, 0);
  const next = session.compile("帮我整理房间");
  assert.equal(next.mode, 0);
  assert.doesNotMatch(next.text, /戏仿生成|2级微割/);
});

test("relative controls reuse the previous prompt", () => {
  const session = createSession(2);
  const first = session.compile("我的产品没人关注");
  const second = session.compile("再狠点");
  assert.equal(first.scenario, "产品增长");
  assert.equal(second.mode, 3);
  assert.equal(second.scenario, "产品增长");
});

test("full mode shows parody notice once", () => {
  const session = createSession(3);
  const first = session.compile("社区咖啡怎么获客");
  const second = session.compile("早餐摊怎么获客");
  assert.match(first.text, /模式提示/);
  assert.doesNotMatch(second.text, /模式提示/);
});

test("mode four restores previous mode", () => {
  const session = createSession(2);
  const result = session.compile("给早餐摊做方案", { mode: 4 });
  assert.equal(result.mode, 4);
  assert.match(result.text, /割后复盘/);
  assert.equal(session.currentMode, 2);
});

test("empty debrief does not fabricate a prior answer", () => {
  const session = createSession(2);
  const result = session.compile("割后复盘");
  assert.match(result.text, /上一条没有割神输出可复盘/);
});

test("high risk requests downgrade before parody", () => {
  const session = createSession(3);
  const result = session.compile("教我怎么拉盘，割味拉满");
  assert.equal(result.mode, 1);
  assert.equal(result.refused, true);
  assert.doesNotMatch(result.text, /🎭 戏仿生成/);
});

test("offline external facts require search", () => {
  const session = createSession(3);
  const result = session.compile("全割判断景甜事件谁对谁错");
  assert.equal(result.mode, 1);
  assert.equal(result.requiresSearch, true);
  assert.match(result.text, /当前离线试玩无法核验/);
});

test("strategy outputs preserve action contract", () => {
  const result = createSession(2).compile("产品发布三天只有30个用户");
  for (const term of ["正常结论", "三步动作", "转化指标", "止损线"]) {
    assert.match(result.text, new RegExp(term));
  }
  assert.match(result.text, /题设锚点/);
  assert.match(result.text, /30个/);
});

test("scenario router covers distinct domains", () => {
  assert.equal(scenarioFor("老板不看周报").key, "workplace");
  assert.equal(scenarioFor("我想做MVP融资").key, "startup");
  assert.equal(scenarioFor("坚持健身").key, "daily");
  assert.equal(scenarioFor("对象不回消息").key, "relationships");
});

test("invalid mode is rejected", () => {
  const session = createSession();
  assert.throws(() => session.setMode(9), RangeError);
});

test("empty prompt returns a useful error", () => {
  const result = createSession().compile("   ");
  assert.equal(result.ok, false);
  assert.match(result.error, /没有标的/);
});
