.PHONY: format lint type test coverage quality clean install-dev help

help:
	@echo "Commandes disponibles :"
	@echo "  make install-dev  - Installer les dépendances de développement"
	@echo "  make format       - Formater le code avec Black"
	@echo "  make lint         - Vérifier et corriger avec Ruff"
	@echo "  make type         - Vérifier les types avec Mypy"
	@echo "  make test         - Exécuter les tests"
	@echo "  make coverage     - Exécuter les tests avec couverture"
	@echo "  make quality      - Exécuter tous les outils de qualité"
	@echo "  make clean        - Nettoyer les fichiers temporaires"

install-dev:
	@echo "Installation avec uv (recommandé)..."
	uv sync || pip install -e ".[dev]"

format:
	@if command -v uv >/dev/null 2>&1; then \
		uv run black py_cli_maker/ tests/; \
	else \
		black py_cli_maker/ tests/; \
	fi

lint:
	@if command -v uv >/dev/null 2>&1; then \
		uv run ruff check --fix py_cli_maker/ tests/; \
	else \
		ruff check --fix py_cli_maker/ tests/; \
	fi

type:
	@if command -v uv >/dev/null 2>&1; then \
		uv run mypy py_cli_maker/; \
	else \
		mypy py_cli_maker/; \
	fi

test:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest -v; \
	else \
		pytest -v; \
	fi

coverage:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest --cov=py_cli_maker --cov-report=term-missing --cov-report=html; \
	else \
		pytest --cov=py_cli_maker --cov-report=term-missing --cov-report=html; \
	fi

quality: format lint type test
	@echo "✅ Tous les outils de qualité ont été exécutés avec succès !"

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	@echo "🧹 Nettoyage terminé !"

