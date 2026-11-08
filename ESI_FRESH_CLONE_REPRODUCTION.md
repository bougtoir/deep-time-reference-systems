> Superseded by `PUBLIC_FRESH_CLONE_REPRODUCTION.md`. The SHA below was not the public HEAD observed at the later audit (`9233d094`); this file is kept as history.

# Fresh-clone reproduction (ESI package)

- Public repository: https://github.com/bougtoir/deep-time-reference-systems, main at `76cb50402f0f4d3b60526943f337171518dcdfcb` (synced from wip branch `devin/1792230689-jog-final-audit`, fast-forwarded to `devin/1793944467-dtrs-esi-pivot` f12a95ad).
- Before reproduction the cloned tree was identical to the canonical subdirectory (`diff -rq` reported only local caches).
- Procedure: `python3 -m venv .venv && .venv/bin/pip install -e . pytest && make reproduce` on a new clone.
- Result: exit 0; 49 tests passed; lint passed; "Verified 20 final files and ZIP integrity."
- Differences after regeneration: only wall-clock values `rec_cost_*_median_decode_ms` and `results/record_cost.csv` timing columns, binary re-renders (DOCX/PDF/ZIP timestamps), and last-digit floating-point noise in `data/processed/itrf_selected_sites.csv`. No seeded value differed.
