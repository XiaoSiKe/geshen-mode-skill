const promptInput = document.querySelector("#prompt");
const generateButton = document.querySelector("#generate");
const copyButton = document.querySelector("#copy");
const status = document.querySelector("#status");
const cards = document.querySelector("#cards");
const resultTitle = document.querySelector("#result-title");
const modeButtons = [...document.querySelectorAll(".mode")];
const presetButtons = [...document.querySelectorAll(".preset")];

const session = window.GeshenCore.createSession(2);
let currentMode = 2;
let lastText = "";

function render() {
  status.textContent = "";
  const result = session.compile(promptInput.value, { mode: currentMode });

  if (!result.ok) {
    status.textContent = result.error;
    promptInput.focus();
    return;
  }

  const fragment = document.createDocumentFragment();
  lastText = result.text;

  result.cards.forEach((item) => {
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
  resultTitle.textContent = `${result.mode}级输出 · ${result.scenario}`;
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

copyButton.addEventListener("click", copyResult);

async function copyResult() {
  try {
    await navigator.clipboard.writeText(lastText);
    status.textContent = "已复制。注意力可以转发，责任不能。";
  } catch {
    status.textContent = "浏览器没给剪贴板权限，请手动复制。";
  }
}
