function rmOpenDrawer() {
  const d = document.getElementById("supportDrawer");
  if (!d) return;
  d.style.transform = "translateX(0)";
  d.setAttribute("aria-hidden", "false");
}
function rmCloseDrawer() {
  const d = document.getElementById("supportDrawer");
  if (!d) return;
  d.style.transform = "translateX(110%)";
  d.setAttribute("aria-hidden", "true");
}

window.addEventListener("DOMContentLoaded", () => {
  const helpBtn = document.getElementById("helpBtn");
  const closeHelp = document.getElementById("closeHelp");
  if (helpBtn) helpBtn.addEventListener("click", rmOpenDrawer);
  if (closeHelp) closeHelp.addEventListener("click", rmCloseDrawer);

  const form = document.getElementById("supportForm");
  if (form) form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const status = document.getElementById("supportStatus");
    if (status) status.textContent = "";
    const payload = {
      category: document.getElementById("supportCat")?.value || "",
      email: document.getElementById("supportEmail")?.value || "",
      message: document.getElementById("supportMsg")?.value || "",
      lang: localStorage.getItem("rm_lang") || "de"
    };
    const r = await fetch("/api/support", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    if (!r.ok) {
      if (status) status.textContent = "Senden fehlgeschlagen.";
      return;
    }
    if (status) status.textContent = "Gesendet.";
    form.reset();
  });
});
