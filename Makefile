.PHONY: install test train deploy clean lint format setup-hooks docker-build docker-run docker-stop

PYTHON = python3
PIP = pip3

install:
	$(PIP) install uv
	uv pip install -r requirements.txt

setup-hooks:
	pre-commit install

test:
	pytest tests/ -v

lint:
	flake8 src/ tests/
	black --check src/ tests/

format:
	black src/ tests/

train:
	$(PYTHON) src/training/train.py

deploy:
	./scripts/deploy.sh

docker-build:
	docker build -f docker/Dockerfile -t audio-sentiment-model:latest .

docker-run:
	docker run -p 8000:8000 --name audio-sentiment-api audio-sentiment-model:latest

docker-stop:
	docker stop audio-sentiment-api || true
	docker rm audio-sentiment-api || true

docker-compose-up:
	docker-compose up --build -d

docker-compose-down:
	docker-compose down

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf mlruns/
	docker-stop

setup-infra:
	cd infrastructure && terraform init && terraform apply

destroy-infra:
	cd infrastructure && terraform destroy

run-pipeline:
	$(PYTHON) src/pipeline.py

api:
	$(PYTHON) src/deployment/api.py

monitoring:
	streamlit run src/monitoring/dashboard.py
