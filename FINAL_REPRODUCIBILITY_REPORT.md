# Final reproducibility report

Audit date: 2026-09-25

## Environment

- Linux 6.8.0-1061-aws, x86_64
- Python 3.10.12
- locale `C.UTF-8`
- numpy 2.2.6
- pandas 2.3.3
- matplotlib 3.10.9
- scipy 1.15.3
- PyYAML 6.0.2
- python-docx 1.2.0
- python-pptx 1.0.2
- pytest 8.4.2

## Commands and results

The requested final commands were executed from the project root in the
activated `.venv`:

```bash
make reproduce
pytest
```

`make reproduce` completed in 49.505 seconds. It:

- verified 30 persisted raw source snapshots by size and SHA-256;
- the numerical pipeline regenerated all configured analyses;
- rebuilt the DOCX, PDF, PPTX, CSV, reproducibility ZIP, and final submission
  ZIP outputs;
- passed source compilation;
- passed **29 tests** in 1.32 seconds; and
- verified 26 manifested final files and the final ZIP CRC and membership.

The first direct `pytest` entry-point invocation exposed that the repository
root was not on that executable's import path, although `python -m pytest`
already passed. The project configuration now declares `pythonpath = ["."]`.
The required direct `pytest` rerun passed **29 tests** in 1.32 seconds
(1.638 seconds wall time).

No warnings remain. The one entry-point collection failure was corrected as
described above. No protected numerical result changed.
