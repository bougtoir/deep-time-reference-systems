PYTHON ?= .venv/bin/python

.PHONY: setup data analysis manuscript all test lint verify-submission reproduce clean-generated

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e .

data:
	$(PYTHON) scripts/verify_raw_data.py

analysis:
	$(PYTHON) scripts/run_pipeline.py --config configs/default.yml

manuscript: analysis
	$(PYTHON) scripts/build_submission.py

all: data manuscript

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m compileall -q src scripts tests

verify-submission:
	$(PYTHON) scripts/verify_submission.py

reproduce: data manuscript lint test verify-submission

clean-generated:
	rm -f data/processed/*.csv results/*.csv figures/*.png tables/*.csv
	rm -f manuscript/*.docx manuscript/*.pdf supplement/*.pdf
	rm -f manuscript/*.pptx supplement/*.docx
	rm -f submission/*.docx submission/*.pdf submission/*.csv submission/*.zip
	rm -f submission/figures/*.png submission/tables/*.csv
	rm -rf submission_final
