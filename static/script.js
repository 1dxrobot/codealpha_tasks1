(function () {
  "use strict";

  const form = document.getElementById("check-form");
  const urlInput = document.getElementById("url");
  const emailInput = document.getElementById("email_content");
  const submitBtn = document.getElementById("submit-btn");
  const resultArea = document.getElementById("result-area");
  const resultCard = document.getElementById("result-card");
  const resultValue = document.getElementById("result-value");
  const resultUrl = document.getElementById("result-url");
  const errorArea = document.getElementById("error-area");
  const errorMessage = document.getElementById("error-message");

  function hideAll() {
    resultArea.classList.add("hidden");
    errorArea.classList.add("hidden");
  }

  function showResult(result, url) {
    hideAll();
    resultValue.textContent = result;
    resultUrl.textContent = "Checked: " + url;
    resultCard.classList.remove("safe", "phishing");
    if (result === "PHISHING DETECTED") {
      resultCard.classList.add("phishing");
    } else {
      resultCard.classList.add("safe");
    }
    resultArea.classList.remove("hidden");
  }

  function showError(msg) {
    hideAll();
    errorMessage.textContent = msg;
    errorArea.classList.remove("hidden");
  }

  function setLoading(loading) {
    submitBtn.disabled = loading;
    submitBtn.classList.toggle("loading", loading);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var url = urlInput.value.trim();
    if (!url) {
      showError("Please enter a URL.");
      return;
    }

    setLoading(true);
    hideAll();

    fetch("/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: url,
        email_content: emailInput.value.trim() || null
      })
    })
      .then(function (res) {
        return res.json().then(function (data) {
          if (!res.ok) throw new Error(data.error || "Request failed");
          return data;
        });
      })
      .then(function (data) {
        showResult(data.result, data.url);
      })
      .catch(function (err) {
        showError(err.message || "Something went wrong. Try again.");
      })
      .finally(function () {
        setLoading(false);
      });
  });
})();
