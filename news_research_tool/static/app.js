const queryInput = document.querySelector("#query");
const searchForm = document.querySelector(".search-form");
const submitButton = document.querySelector(".primary-button");
const quickTopics = document.querySelectorAll("[data-topic]");
const languageSelect = document.querySelector("#target_language");

quickTopics.forEach((button) => {
  button.addEventListener("click", () => {
    if (!queryInput) {
      return;
    }

    queryInput.value = button.dataset.topic;
    queryInput.focus();
  });
});

if (searchForm && submitButton) {
  searchForm.addEventListener("submit", () => {
    submitButton.disabled = true;
    const targetLanguage = languageSelect?.value || "English";
    const actionText = targetLanguage === "English" ? "Analyzing..." : "Translating...";

    submitButton.querySelector("span").textContent = actionText;
  });
}
