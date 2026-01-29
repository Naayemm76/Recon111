const RM_I18N = {
  de: {
    subtitle: "Secure Assessment Workspace",
    help: "Hilfe?",
    logout: "Logout",
    loginTitle: "Anmeldung",
    usernameLabel: "Benutzername",
    passwordLabel: "Passwort",
    acceptText: "Ich akzeptiere die Bedingungen.",
    showTerms: "Bedingungen anzeigen",
    loginBtn: "Einloggen",
    termsTitle: "Bedingungen",
    supportTitle: "Support",
    supportCategory: "Kategorie",
    supportEmail: "E-Mail",
    supportMsg: "Nachricht",
    sendBtn: "Senden",
    catAccess: "Zugriff / Freischaltung",
    catBilling: "Abrechnung",
    catBug: "Bug / Fehler",
    catFeature: "Feature-Wunsch",
    catOther: "Sonstiges",
    projectTitle: "Projekt",
    projectName: "Projektname",
    projectTarget: "Ziel (Domain/IP/Name)",
    projectScope: "Scope (Kurzbeschreibung)",
    createProject: "Projekt anlegen",
    modulesTitle: "Module",
    logsTitle: "Live-Logs",
    refresh: "Aktualisieren"
  },
  en: {
    subtitle: "Secure Assessment Workspace",
    help: "Help?",
    logout: "Logout",
    loginTitle: "Sign in",
    usernameLabel: "Username",
    passwordLabel: "Password",
    acceptText: "I accept the terms.",
    showTerms: "View terms",
    loginBtn: "Login",
    termsTitle: "Terms",
    supportTitle: "Support",
    supportCategory: "Category",
    supportEmail: "Email",
    supportMsg: "Message",
    sendBtn: "Send",
    catAccess: "Access / Approval",
    catBilling: "Billing",
    catBug: "Bug / Issue",
    catFeature: "Feature request",
    catOther: "Other",
    projectTitle: "Project",
    projectName: "Project name",
    projectTarget: "Target (Domain/IP/Name)",
    projectScope: "Scope (short description)",
    createProject: "Create project",
    modulesTitle: "Modules",
    logsTitle: "Live logs",
    refresh: "Refresh"
  }
};

function rmApplyI18n(lang) {
  const dict = RM_I18N[lang] || RM_I18N.de;
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const k = el.getAttribute("data-i18n");
    if (dict[k]) el.textContent = dict[k];
  });
}

function rmInitLang(selectId="lang") {
  const sel = document.getElementById(selectId);
  const saved = localStorage.getItem("rm_lang") || "de";
  if (sel) sel.value = saved;
  rmApplyI18n(saved);
  if (sel) sel.addEventListener("change", () => {
    localStorage.setItem("rm_lang", sel.value);
    rmApplyI18n(sel.value);
  });
}
