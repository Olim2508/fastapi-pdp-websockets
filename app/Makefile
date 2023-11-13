run:
	uvicorn app:app --host 0.0.0.0 --port 8007 --reload

mg:
	alembic upgrade head

m:
	alembic revision -m ${mess} --autogenerate

style:
	black . && isort . && flake8 .