
document.addEventListener("DOMContentLoaded", () => {
  const totalQuestions = document.querySelectorAll(".question-block").length;
  const progressBar = document.getElementById("progress-bar-fill");

  function updateProgressBar() {
    const answered = new Set();
    document.querySelectorAll("input[type='radio']:checked").forEach((input) => {
      answered.add(input.name);
    });
    const percent = (answered.size / totalQuestions) * 100;
    progressBar.style.width = `${percent}%`;
    progressBar.textContent = `${Math.round(percent)}%`;
  }

  document.querySelectorAll("input[type='radio']").forEach((radio) => {
    radio.addEventListener("change", updateProgressBar);
  });
});
