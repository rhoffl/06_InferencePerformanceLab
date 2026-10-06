.PHONY: setup test up down demo
setup:
	python -m pip install -e '.[dev]'
test:
	pytest -q
up:
	docker compose up --build -d
down:
	docker compose down
demo:
	docker compose exec api inference-lab run configs/experiments/demo.yaml

