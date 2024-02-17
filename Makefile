lint:
		poetry run ruff check .

test:
		poetry run coverage run
		poetry run coverage report

test-cov:
		poetry run coverage xml
