const API_BASE = "/api";

// Load everything on startup
document.addEventListener("DOMContentLoaded", () => {
  loadStatus();
  loadRules();
});

// ---------------- STATUS ----------------
async function loadStatus() {
  try {
    const res = await fetch(`${API_BASE}/ufw/status`);
    const data = await res.json();

    document.getElementById("statusText").innerText =
      `Firewall is ${data.status || "Unknown"}`;
  } catch (err) {
    document.getElementById("statusText").innerText = "Failed to load status";
  }
}

// Enable firewall
document.getElementById("enableBtn").addEventListener("click", async () => {
  await fetch(`${API_BASE}/ufw/enable`, {
    method: "POST",
  });

  loadStatus();
});

// Disable firewall
document.getElementById("disableBtn").addEventListener("click", async () => {
  await fetch(`${API_BASE}/ufw/disable`, {
    method: "POST",
  });

  loadStatus();
});

// ---------------- RULES ----------------
async function loadRules() {
  try {
    const res = await fetch(`${API_BASE}/ufw`);
    const rules = await res.json();

    const tableBody = document.getElementById("rulesTableBody");
    tableBody.innerHTML = "";

    if (rules.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="3">No rules found</td></tr>`;
      return;
    }

    rules.forEach((rule) => {
      const row = document.createElement("tr");

      row.innerHTML = `
                <td>${rule.id}</td>
                <td>${rule.rule}</td>
                <td>
                    <button class="delete-btn" onclick="deleteRule(${rule.id})">
                        Delete
                    </button>
                </td>
            `;

      tableBody.appendChild(row);
    });
  } catch (err) {
    console.error(err);
  }
}

// Add rule
document.getElementById("ruleForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const port = document.getElementById("port").value;
  const protocol = document.getElementById("protocol").value;
  const rule = document.getElementById("ruleType").value;

  const res = await fetch(`${API_BASE}/ufw`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      port,
      protocol,
      rule,
    }),
  });

  const data = await res.json();

  alert(data.message || data.error);

  loadRules();
});

// Delete rule
async function deleteRule(id) {
  if (!confirm("Delete this rule?")) return;

  const res = await fetch(`${API_BASE}/ufw`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id,
    }),
  });

  const data = await res.json();

  alert(data.message || data.error);

  loadRules();
}
