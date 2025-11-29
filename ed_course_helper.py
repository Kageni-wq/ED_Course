"""MIT License

Copyright (c) 2025 Kagen Aeby

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import webview
import tempfile
import os

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ED Course Helper (Local)</title>
  <style>
    * {
      box-sizing: border-box;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
        sans-serif;
    }
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      background: #f4f4f6;
      color: #222;
    }
    .app {
      display: flex;
      width: 100%;
      height: 100%;
    }
    .sidebar {
      width: 260px;
      background: #1f2933;
      color: #f9fafb;
      display: flex;
      flex-direction: column;
    }
    .sidebar-header {
      padding: 12px 14px;
      border-bottom: 1px solid #374151;
      font-size: 16px;
      font-weight: 600;
    }
    .sidebar-controls {
      padding: 8px 10px;
      border-bottom: 1px solid #374151;
    }
    button {
      cursor: pointer;
      border-radius: 4px;
      border: none;
      padding: 6px 10px;
      font-size: 13px;
    }
    .btn-primary {
      background: #2563eb;
      color: white;
    }
    .btn-primary:hover {
      background: #1d4ed8;
    }
    .btn-secondary {
      background: #e5e7eb;
      color: #111827;
    }
    .btn-secondary:hover {
      background: #d1d5db;
    }
    .btn-danger {
      background: #ef4444;
      color: #fef2f2;
    }
    .btn-danger:hover {
      background: #dc2626;
    }
    .patient-list {
      flex: 1;
      overflow-y: auto;
      padding: 6px 0;
    }
    .patient-item {
      padding: 8px 12px;
      margin: 4px 6px;
      border-radius: 4px;
      font-size: 13px;
      line-height: 1.3;
      background: transparent;
      border: 1px solid transparent;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .patient-item.active {
      background: #111827;
      border-color: #4f46e5;
    }
    .patient-item:hover {
      background: #111827;
    }
    .patient-label {
      flex: 1;
      margin-right: 4px;
      word-break: break-word;
    }
    .patient-room {
      font-size: 11px;
      opacity: 0.75;
    }
    .main {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 12px 14px;
      gap: 10px;
    }
    .header-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .header-title {
      font-size: 17px;
      font-weight: 600;
    }
    .header-subtitle {
      font-size: 13px;
      color: #4b5563;
      margin-top: 2px;
    }
    .patient-meta {
      font-size: 13px;
      color: #6b7280;
      margin-top: 4px;
    }
    .patient-meta span {
      margin-right: 10px;
    }
    .main-card {
      background: white;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.15);
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      height: 100%;
      min-height: 0;
    }
    .label-small {
      font-size: 12px;
      font-weight: 500;
      color: #4b5563;
    }
    textarea {
      width: 100%;
      resize: vertical;
      min-height: 64px;
      max-height: 160px;
      padding: 8px;
      border-radius: 6px;
      border: 1px solid #d1d5db;
      font-size: 13px;
      outline: none;
    }
    textarea:focus {
      border-color: #2563eb;
      box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.3);
    }
    .controls-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }
    .controls-row-left,
    .controls-row-right {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      align-items: center;
    }
    .time-format-toggle {
      font-size: 12px;
      color: #4b5563;
    }
    .time-format-toggle input {
      margin-right: 4px;
    }
    .entries-container {
      flex: 1;
      border-radius: 6px;
      border: 1px solid #e5e7eb;
      padding: 6px 8px;
      overflow-y: auto;
      font-size: 13px;
      background: #f9fafb;
    }
    .entry-item {
      padding: 4px 0;
      border-bottom: 1px solid #e5e7eb;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .entry-item:last-child {
      border-bottom: none;
    }
    .entry-timestamp {
      font-weight: 600;
      color: #111827;
      margin-right: 4px;
    }
    .empty-state {
      font-size: 13px;
      color: #9ca3af;
      font-style: italic;
    }
    .status-bar {
      font-size: 11px;
      color: #6b7280;
      margin-top: 2px;
    }
    .status-bar span {
      margin-right: 12px;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 2px 8px;
      font-size: 11px;
      border-radius: 999px;
      background: #e5e7eb;
      color: #374151;
    }
    .link-like {
      font-size: 11px;
      color: #2563eb;
      text-decoration: underline;
      cursor: pointer;
    }
    .hidden {
      display: none !important;
    }
    @media (max-width: 800px) {
      .sidebar {
        width: 200px;
      }
    }
  </style>
</head>
<body>
<div class="app">
  <div class="sidebar">
    <div class="sidebar-header">
      ED Course Helper
    </div>
    <div class="sidebar-controls">
      <button class="btn-primary" id="addPatientBtn">+ Add Patient</button>
    </div>
    <div class="patient-list" id="patientList">
    </div>
  </div>

  <div class="main">
    <div class="header-row">
      <div>
        <div class="header-title" id="headerTitle">
          No patient selected
        </div>
        <div class="header-subtitle">
          Add a patient on the left, then log timestamped ED course updates here.
        </div>
        <div class="patient-meta" id="patientMeta"></div>
      </div>
      <div class="controls-row-right">
        <button class="btn-secondary" id="renamePatientBtn" disabled>Rename</button>
        <button class="btn-danger" id="deletePatientBtn" disabled>Remove</button>
      </div>
    </div>

    <div class="main-card">
      <div>
        <div class="label-small">New ED course entry</div>
        <textarea id="entryInput" placeholder="Example: Reassessed – improving pain, VS stable. CT a/p ordered."></textarea>
      </div>

      <div class="controls-row">
        <div class="controls-row-left">
          <button class="btn-primary" id="addEntryBtn" disabled>Add Entry</button>
          <span style="font-size:11px;color:#6b7280;">
            Tip: Ctrl+Enter to add
          </span>
        </div>
        <div class="controls-row-right">
          <div class="time-format-toggle">
            <label>
              <input type="checkbox" id="timeFormatToggle" />
              Use 24-hour time
            </label>
          </div>
          <button class="btn-secondary" id="copyCourseBtn" disabled>Copy ED Course to Clipboard</button>
        </div>
      </div>

      <div>
        <div class="label-small">Entries (oldest at top)</div>
        <div class="entries-container" id="entriesContainer">
          <div class="empty-state">
            No entries yet. Add your first ED course update above.
          </div>
        </div>
      </div>

      <div class="status-bar">
        <span id="statusPatients">0 patients</span>
        <span id="statusEntries">0 entries</span>
        <span id="statusMessage"></span>
      </div>
    </div>
  </div>
</div>

<script>
  const STORAGE_KEY = "edCourseHelper_v1";
  let state = {
    patients: [],
    selectedPatientId: null,
    use24Hour: true,
  };

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && Array.isArray(parsed.patients)) {
          state = Object.assign(
            { patients: [], selectedPatientId: null, use24Hour: true },
            parsed
          );
        }
      }
    } catch (e) {
      console.error("Failed to load state", e);
    }
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      console.error("Failed to save state", e);
    }
  }

  function uuid() {
    return "p_" + Math.random().toString(36).substring(2, 10);
  }

  function formatTimestamp(date, use24Hour) {
    const d = date;
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");
    let hh = d.getHours();
    const mins = String(d.getMinutes()).padStart(2, "0");

    if (use24Hour) {
      return `${mm}/${dd}/${yyyy} ${String(hh).padStart(2, "0")}:${mins}`;
    } else {
      const ampm = hh >= 12 ? "PM" : "AM";
      hh = hh % 12;
      if (hh === 0) hh = 12;
      return `${mm}/${dd}/${yyyy} ${hh}:${mins} ${ampm}`;
    }
  }

  function getSelectedPatient() {
    return state.patients.find(p => p.id === state.selectedPatientId) || null;
  }

  function setStatusMessage(msg, timeoutMs = 2000) {
    const el = document.getElementById("statusMessage");
    el.textContent = msg || "";
    if (timeoutMs && msg) {
      setTimeout(() => {
        if (el.textContent === msg) {
          el.textContent = "";
        }
      }, timeoutMs);
    }
  }

  function renderPatients() {
    const list = document.getElementById("patientList");
    list.innerHTML = "";

    if (state.patients.length === 0) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.style.padding = "10px";
      empty.textContent = "No patients yet. Click \"+ Add Patient\" to start.";
      list.appendChild(empty);
      return;
    }

    state.patients.forEach(p => {
      const item = document.createElement("div");
      item.className = "patient-item" + (p.id === state.selectedPatientId ? " active" : "");
      item.dataset.id = p.id;

      const label = document.createElement("div");
      label.className = "patient-label";
      label.textContent = p.label || "Untitled";

      const room = document.createElement("div");
      room.className = "patient-room";
      if (p.room) {
        room.textContent = p.room;
      }

      item.appendChild(label);
      if (p.room) item.appendChild(room);

      item.addEventListener("click", () => {
        state.selectedPatientId = p.id;
        saveState();
        renderAll();
      });

      list.appendChild(item);
    });
  }

  function renderEntries() {
    const container = document.getElementById("entriesContainer");
    container.innerHTML = "";

    const patient = getSelectedPatient();

    if (!patient) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = "Select a patient to view their ED course entries.";
      container.appendChild(empty);
      return;
    }

    if (!patient.entries || patient.entries.length === 0) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = "No entries yet for this patient.";
      container.appendChild(empty);
      return;
    }

    const entries = [...patient.entries].sort((a, b) => a.timestamp - b.timestamp);

    entries.forEach(entry => {
      const item = document.createElement("div");
      item.className = "entry-item";

      const tsSpan = document.createElement("span");
      tsSpan.className = "entry-timestamp";
      tsSpan.textContent = formatTimestamp(new Date(entry.timestamp), state.use24Hour) + " –";

      const textSpan = document.createElement("span");
      textSpan.textContent = " " + entry.text;

      item.appendChild(tsSpan);
      item.appendChild(textSpan);

      container.appendChild(item);
    });
  }

  function renderHeader() {
    const headerTitle = document.getElementById("headerTitle");
    const patientMeta = document.getElementById("patientMeta");

    const patient = getSelectedPatient();

    if (!patient) {
      headerTitle.textContent = "No patient selected";
      patientMeta.textContent = "";
      return;
    }

    headerTitle.textContent = patient.label || "Untitled patient";

    const parts = [];
    if (patient.room) parts.push(`Room/Bed: ${patient.room}`);
    if (patient.createdAt) {
      parts.push(
        "Created: " + formatTimestamp(new Date(patient.createdAt), state.use24Hour)
      );
    }

    patientMeta.textContent = parts.join(" • ");
  }

  function renderStatusBar() {
    const statusPatients = document.getElementById("statusPatients");
    const statusEntries = document.getElementById("statusEntries");

    const totalPatients = state.patients.length;
    const totalEntries = state.patients.reduce(
      (sum, p) => sum + (p.entries ? p.entries.length : 0),
      0
    );

    statusPatients.textContent =
      totalPatients + (totalPatients === 1 ? " patient" : " patients");
    statusEntries.textContent =
      totalEntries + (totalEntries === 1 ? " entry" : " entries");
  }

  function renderControls() {
    const patientSelected = !!getSelectedPatient();

    document.getElementById("addEntryBtn").disabled = !patientSelected;
    document.getElementById("copyCourseBtn").disabled = !patientSelected;
    document.getElementById("renamePatientBtn").disabled = !patientSelected;
    document.getElementById("deletePatientBtn").disabled = !patientSelected;

    document.getElementById("timeFormatToggle").checked = state.use24Hour;
  }

  function renderAll() {
    renderPatients();
    renderEntries();
    renderHeader();
    renderStatusBar();
    renderControls();
  }

  function onAddPatient() {
    const label = prompt(
      "Patient label (e.g. 'B12 – 81M SBO' or 'B6 – 45F CP'):"
    );
    if (!label) {
      return;
    }

    const room = prompt("Room/Bed (optional):", "");

    const id = uuid();
    const now = Date.now();
    const newPatient = {
      id,
      label: label.trim(),
      room: room ? room.trim() : "",
      createdAt: now,
      entries: [],
    };

    state.patients.push(newPatient);
    state.selectedPatientId = id;
    saveState();
    renderAll();
  }

  function onRenamePatient() {
    const patient = getSelectedPatient();
    if (!patient) return;

    const newLabel = prompt("Edit patient label:", patient.label || "");
    if (newLabel === null) return;

    const newRoom = prompt(
      "Edit room/bed (optional):",
      patient.room ? patient.room : ""
    );
    patient.label = newLabel.trim() || patient.label;
    patient.room = newRoom ? newRoom.trim() : "";

    saveState();
    renderAll();
  }

  function onDeletePatient() {
    const patient = getSelectedPatient();
    if (!patient) return;

    const confirmDelete = confirm(
      `Remove patient "${patient.label}" and all their entries?`
    );
    if (!confirmDelete) return;

    state.patients = state.patients.filter(p => p.id !== patient.id);
    if (state.selectedPatientId === patient.id) {
      state.selectedPatientId = state.patients[0]?.id || null;
    }

    saveState();
    renderAll();
  }

  function onAddEntry() {
    const patient = getSelectedPatient();
    if (!patient) return;

    const input = document.getElementById("entryInput");
    const text = input.value.trim();
    if (!text) {
      setStatusMessage("Cannot add an empty entry.");
      return;
    }

    const now = Date.now();
    const entry = {
      timestamp: now,
      text,
    };

    if (!patient.entries) patient.entries = [];
    patient.entries.push(entry);

    input.value = "";
    saveState();
    renderAll();
    setStatusMessage("Entry added.");
    input.focus();
  }

  async function onCopyCourse() {
    const patient = getSelectedPatient();
    if (!patient) return;

    const use24 = state.use24Hour;

    const entries = (patient.entries || []).sort(
      (a, b) => a.timestamp - b.timestamp
    );

    if (entries.length === 0) {
      setStatusMessage("No entries to copy for this patient.");
      return;
    }

    const lines = entries.map(entry => {
      const ts = formatTimestamp(new Date(entry.timestamp), use24);
      return `${ts} - ${entry.text}`;
    });

    const header = patient.label ? patient.label + "\n" : "";
    const textToCopy = header + lines.join("\n");

    try {
      await navigator.clipboard.writeText(textToCopy);
      setStatusMessage("ED course copied to clipboard.");
    } catch (e) {
      console.error("Clipboard failed", e);
      setStatusMessage("Clipboard failed; you may need to copy manually.");
    }
  }

  function onTimeFormatToggle(e) {
    state.use24Hour = e.target.checked;
    saveState();
    renderAll();
  }

  function onEntryKeyDown(e) {
    if (e.key === "Enter" && e.ctrlKey) {
      e.preventDefault();
      onAddEntry();
    }
  }

  function init() {
    loadState();

    document
      .getElementById("addPatientBtn")
      .addEventListener("click", onAddPatient);
    document
      .getElementById("renamePatientBtn")
      .addEventListener("click", onRenamePatient);
    document
      .getElementById("deletePatientBtn")
      .addEventListener("click", onDeletePatient);
    document
      .getElementById("addEntryBtn")
      .addEventListener("click", onAddEntry);
    document
      .getElementById("copyCourseBtn")
      .addEventListener("click", onCopyCourse);
    document
      .getElementById("timeFormatToggle")
      .addEventListener("change", onTimeFormatToggle);
    document
      .getElementById("entryInput")
      .addEventListener("keydown", onEntryKeyDown);

    if (typeof state.use24Hour !== "boolean") {
      state.use24Hour = true;
    }

    renderAll();
  }

  window.addEventListener("load", init);
</script>
</body>
</html>
"""

def main():
    # Write HTML to a temporary file and open it in a webview window
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
        f.write(HTML_CONTENT.encode("utf-8"))
        temp_path = f.name

    # Create window
    window = webview.create_window("ED Course Helper", temp_path, width=1000, height=650)
    webview.start()

    # Cleanup temp file on close if you want
    try:
        os.remove(temp_path)
    except OSError:
        pass

if __name__ == "__main__":
    main()
