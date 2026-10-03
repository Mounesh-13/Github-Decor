# Task 6 report — sequential visibility windows

## Timing fix (parent 309c578)
Plan copy-paste had left all opacity gates at 0.5–6s. Corrected keyTimes only
(values/begin/dur untouched) on assets/escape.svg:
- eyes-wide: 0;0.02;0.2;0.25 → 0;0.16;0.29;0.33 (4–8s)
- mallet: 0;0.02;0.25;0.3 → 0;0.33;0.54;0.58 (8–14s)
- leak: 0;0.02;0.25;0.3 → 0;0.58;0.71;0.75 (14–18s)
- big-red-button: 0;0.02;0.2;0.25 → 0;0.67;0.79;0.83 (16–20s)
Untouched: crack (0;0.02;0.6;0.65), spinner (0;0.79;0.96;1), flash rect, all begin/dur.
Tests: 13 passed (pytest tests/ -q); grep keyTimes confirms 4 new + 3 preserved gates.
