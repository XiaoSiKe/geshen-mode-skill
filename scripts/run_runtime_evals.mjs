#!/usr/bin/env node

import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const require = createRequire(import.meta.url);
const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "..");
const { createSession } = require(resolve(root, "playground/core.js"));
const cases = JSON.parse(readFileSync(resolve(root, "evals/runtime-cases.json"), "utf8"));

let assertions = 0;
const failures = [];

function check(condition, message) {
  assertions += 1;
  if (!condition) failures.push(message);
}

for (const testCase of cases) {
  const session = createSession(testCase.initial_mode);
  testCase.turns.forEach((turn, index) => {
    const result = session.compile(turn.prompt);
    const prefix = `${testCase.id} turn ${index + 1}`;
    check(result.ok, `${prefix}: result not ok`);
    check(result.mode === turn.expect.mode, `${prefix}: mode ${result.mode} != ${turn.expect.mode}`);
    check(result.scenario === turn.expect.scenario, `${prefix}: scenario ${result.scenario} != ${turn.expect.scenario}`);
    check(result.refused === turn.expect.refused, `${prefix}: refused mismatch`);
    check(result.requiresSearch === turn.expect.requires_search, `${prefix}: requiresSearch mismatch`);
    turn.expect.includes.forEach((term) => check(result.text.includes(term), `${prefix}: missing "${term}"`));
    turn.expect.excludes.forEach((term) => check(!result.text.includes(term), `${prefix}: forbidden "${term}"`));
  });
}

if (failures.length) {
  console.error(`FAIL  runtime evals: ${failures.length}/${assertions} assertions failed`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log(`PASS  runtime evals: ${cases.length} scenarios, ${assertions} assertions`);
