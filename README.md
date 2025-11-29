# ED_Course

Lightweight, local-first helpers for jotting ED course updates and related note sections. Each HTML file can be opened directly in a browser (no backend); data is stored in that browser's `localStorage`.

## Variants
- `ed_note.html` — Full note helper with HPI / PE / MDM text areas plus ED course log (oldest-first), patient add/rename/delete, 12/24h toggle, copy course to clipboard, and export all patients to a `.txt`.
- `ed_note+tasks.html` — Everything in `ed_note.html` plus a per-patient tasks checklist (default “Publish note” / “Sign note”), done pills in the sidebar, and task add/delete/complete controls.
- `ed_course.html` — Minimal ED course logger: patients + timestamped course entries (oldest-first), 12/24h toggle, copy course to clipboard. No HPI/PE/MDM fields or tasks.
- `ed_course_helper.py` — Python wrapper that serves the minimal ED course UI in a PyWebView window for quick desktop use. Run `python ed_course_helper.py`.

## Notes
- Data stays in the browser profile you use to open the HTML (no sync across browsers/devices).
- Variants do not share storage keys; use the same file consistently if you want to keep existing notes.
