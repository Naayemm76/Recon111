window.addEventListener("DOMContentLoaded", async () => {
  rmInitLang("lang");

  const termsModal = document.getElementById("termsModal");
  const showTerms = document.getElementById("showTerms");
  const closeTerms = document.getElementById("closeTerms");
  const termsBody = document.getElementById("termsBody");

  if (showTerms) showTerms.addEventListener("click", async () => {
    const r = await fetch("/api/legal/terms");
    const t = await r.text();
    if (termsBody) termsBody.textContent = t || "";
    if (termsModal) { termsModal.style.display = "flex"; termsModal.setAttribute("aria-hidden","false"); }
  });
  if (closeTerms) closeTerms.addEventListener("click", () => {
    if (termsModal) { termsModal.style.display = "none"; termsModal.setAttribute("aria-hidden","true"); }
  });

  const form = document.getElementById("loginForm");
  const msg = document.getElementById("msg");
  if (form) form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (msg) msg.textContent = "";
    const payload = {
      username: document.getElementById("username")?.value || "",
      password: document.getElementById("password")?.value || "",
      accept: document.getElementById("accept")?.checked || false,
      lang: localStorage.getItem("rm_lang") || "de"
    };
    const r = await fetch("/api/login", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    if (!r.ok) {
      const t = await r.text();
      if (msg) msg.textContent = t || "Login fehlgeschlagen.";
      return;
    }
    window.location.href = "/app";
  });
});
