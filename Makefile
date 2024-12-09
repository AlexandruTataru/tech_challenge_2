init:
	pip install -r requirements.txt

test:
	pytest

analysis:
	pylint `ls *.py`

.PHONY: init test