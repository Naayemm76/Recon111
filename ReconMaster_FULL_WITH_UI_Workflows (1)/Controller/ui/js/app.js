async function rmFetchJson(url, opts) {
  const r = await fetch(url, opts || {});
  if (!r.ok) throw new Error(await r.text());
  return await r.json();
}

function rmModuleRow(m) {
  const d = document.createElement("div");
  d.className = "module";
  const left = document.createElement("div");
  left.className = "modLeft";
  const name = document.createElement("div");
  name.className = "modName";
  name.textContent = m.title;
  const desc = document.createElement("div");
  desc.className = "modDesc";
  desc.textContent = m.explain;
  const badges = document.createElement("div");
  badges.style.marginTop = "6px";
  const b1 = document.createElement("span");
  b1.className = "badge";
  b1.textContent = m.state;
  const b2 = document.createElement("span");
  b2.className = "badge";
  b2.textContent = m.policy;
  badges.appendChild(b1);
  badges.appendChild(b2);
  left.appendChild(name);
  left.appendChild(desc);
  left.appendChild(badges);

  const right = document.createElement("div");
  const btn = document.createElement("button");
  btn.className = "btn";
  btn.textContent = m.action;
  btn.disabled = !m.enabled;
  btn.addEventListener("click", async () => {
    await rmFetchJson("/api/modules/run", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({module_id: m.id, project: document.getElementById("logProject").value})
    });
    await rmLoadLogs();
  });
  right.appendChild(btn);

  d.appendChild(left);
  d.appendChild(right);
  return d;
}

async function rmLoadModules() {
  const list = await rmFetchJson("/api/modules");
  const host = document.getElementById("modules");
  host.innerHTML = "";
  list.forEach(m => host.appendChild(rmModuleRow(m)));
}

async function rmLoadProjects() {
  const data = await rmFetchJson("/api/projects");
  const sel = document.getElementById("logProject");
  sel.innerHTML = "";
  data.projects.forEach(p => {
    const o = document.createElement("option");
    o.value = p.id;
    o.textContent = p.name;
    sel.appendChild(o);
  });
}

async function rmLoadLogs() {
  const p = document.getElementById("logProject").value;
  const r = await fetch("/api/logs/tail?project=" + encodeURIComponent(p));
  const t = await r.text();
  document.getElementById("logView").textContent = t || "";
}

window.addEventListener("DOMContentLoaded", async () => {
  rmInitLang("lang");

  const me = await rmFetchJson("/api/me");
  document.getElementById("whoami").textContent = me.username + " · " + me.role;

  document.getElementById("logoutBtn").addEventListener("click", async () => {
    await fetch("/api/logout", {method:"POST"});
    window.location.href = "/";
  });

  document.getElementById("refreshLogs").addEventListener("click", rmLoadLogs);

  const projectForm = document.getElementById("projectForm");
  projectForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById("projectName").value,
      target: document.getElementById("projectTarget").value,
      scope: document.getElementById("projectScope").value
    };
    const status = document.getElementById("projectStatus");
    status.textContent = "";
    try{
      await rmFetchJson("/api/projects/create", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
      });
      status.textContent = "OK";
      projectForm.reset();
      await rmLoadProjects();
      await rmLoadLogs();
    }catch(err){
      status.textContent = String(err.message || err);
    }
  });

  await rmLoadProjects();
  await rmLoadModules();
  await rmLoadLogs();
});
