.PHONY: format lint type test coverage quality clean install-dev help test-cli test-generators test-ninja test-package test-domaine test-ddd check-tests check-tests

help:
	@echo "Commandes disponibles :"
	@echo "  make install-dev  - Installer les dépendances de développement"
	@echo "  make format       - Formater le code avec Black"
	@echo "  make lint         - Vérifier et corriger avec Ruff"
	@echo "  make type         - Vérifier les types avec Mypy"
	@echo "  make test         - Exécuter tous les tests"
	@echo "  make test-cli     - Tester uniquement les commandes CLI"
	@echo "  make test-generators - Tester uniquement les générateurs"
	@echo "  make test-ninja   - Tester le générateur ninja_routes"
	@echo "  make test-package - Tester le générateur package"
	@echo "  make test-domaine - Tester le générateur domaine"
	@echo "  make test-ddd     - Tester le générateur domaine DDD"
	@echo "  make coverage     - Exécuter les tests avec couverture"
	@echo "  make quality      - Exécuter tous les outils de qualité"
	@echo "  make check-tests  - Vérifier que tous les fichiers de test existent"
	@echo "  make clean        - Nettoyer les fichiers temporaires"

install-dev:
	@echo "Installation avec uv (recommandé)..."
	uv sync || pip install -e ".[dev]"

format:
	@if command -v uv >/dev/null 2>&1; then \
		uv run black pyfastcli/ tests/; \
	else \
		black pyfastcli/ tests/; \
	fi

lint:
	@if command -v uv >/dev/null 2>&1; then \
		uv run ruff check --fix pyfastcli/ tests/; \
	else \
		ruff check --fix pyfastcli/ tests/; \
	fi

type:
	@if command -v uv >/dev/null 2>&1; then \
		uv run mypy pyfastcli/; \
	else \
		mypy pyfastcli/; \
	fi

test:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest -v; \
	else \
		pytest -v; \
	fi

test-cli:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest -v tests/test_cli.py; \
	else \
		pytest -v tests/test_cli.py; \
	fi

test-generators:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest -v tests/test_ninja_routes.py tests/test_package_generator.py tests/test_domaine_generator.py tests/test_ddd_domaine_generator.py; \
	else \
		pytest -v tests/test_ninja_routes.py tests/test_package_generator.py tests/test_domaine_generator.py tests/test_ddd_domaine_generator.py; \
	fi

test-ninja:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest -v tests/test_ninja_routes.py; \
	else \
		pytest -v tests/test_ninja_routes.py; \
	fi

test-package:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest -v tests/test_package_generator.py; \
	else \
		pytest -v tests/test_package_generator.py; \
	fi

test-domaine:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest -v tests/test_domaine_generator.py; \
	else \
		pytest -v tests/test_domaine_generator.py; \
	fi

test-ddd:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest -v tests/test_ddd_domaine_generator.py; \
	else \
		pytest -v tests/test_ddd_domaine_generator.py; \
	fi

coverage:
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest --cov=pyfastcli --cov-report=term-missing --cov-report=html; \
	else \
		pytest --cov=pyfastcli --cov-report=term-missing --cov-report=html; \
	fi

quality: format lint type test
	@echo " Tous les outils de qualité ont été exécutés avec succès !"

check-tests:
	@echo "Vérification des fichiers de test..."
	@test -f tests/test_cli.py && echo "✓ test_cli.py" || echo "✗ test_cli.py manquant"
	@test -f tests/test_ninja_routes.py && echo "✓ test_ninja_routes.py" || echo "✗ test_ninja_routes.py manquant"
	@test -f tests/test_package_generator.py && echo "✓ test_package_generator.py" || echo "✗ test_package_generator.py manquant"
	@test -f tests/test_domaine_generator.py && echo "✓ test_domaine_generator.py" || echo "✗ test_domaine_generator.py manquant"
	@test -f tests/test_ddd_domaine_generator.py && echo "✓ test_ddd_domaine_generator.py" || echo "✗ test_ddd_domaine_generator.py manquant"
	@echo "Vérification terminée !"

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
	@echo " Nettoyage terminé !"

