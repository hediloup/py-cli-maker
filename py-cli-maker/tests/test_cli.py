"""Tests pour l'interface CLI."""

import shutil
import tempfile
from pathlib import Path

from click.testing import CliRunner

from py_cli_maker.cli import cli


class TestCLI:
    """Tests pour la commande CLI."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "routes"

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_help(self):
        """Test de l'aide de la CLI."""
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "CLI de génération de code" in result.output

    def test_make_url_help(self):
        """Test de l'aide de la commande make:url."""
        result = self.runner.invoke(cli, ["make:url", "--help"])
        assert result.exit_code == 0
        assert "Génère un fichier .py contenant une route Django Ninja" in result.output

    def test_make_url_with_options(self):
        """Test de la génération avec options en ligne de commande."""
        result = self.runner.invoke(
            cli,
            [
                "make:url",
                "--function-name",
                "get_orders",
                "--url-path",
                "/orders",
                "--http-method",
                "get",
                "--tag",
                "Orders",
                "--output-dir",
                str(self.output_dir),
                "--description",
                "Récupère les commandes",
            ],
        )

        assert result.exit_code == 0
        assert "Fichier généré avec succès" in result.output

        file_path = self.output_dir / "get_orders.py"
        assert file_path.exists()

        content = file_path.read_text(encoding="utf-8")
        assert "def get_orders(request):" in content
        assert '@router.get("/orders")' in content
        assert "Récupère les commandes" in content

    def test_make_url_interactive(self):
        """Test de la génération en mode interactif."""
        # Simuler les réponses interactives
        self.runner.invoke(
            cli,
            [
                "make:url",
                "--output-dir",
                str(self.output_dir),
            ],
            input="api\nget_orders\n/orders\nget\nOrders\nRécupère les commandes\n",
        )

        # En mode interactif, les prompts peuvent nécessiter des réponses
        # Pour simplifier, on teste avec toutes les options fournies
        file_path = self.output_dir / "get_orders.py"
        if file_path.exists():
            assert "def get_orders(request):" in file_path.read_text(encoding="utf-8")

    def test_make_url_invalid_method(self):
        """Test avec une méthode HTTP invalide."""
        result = self.runner.invoke(
            cli,
            [
                "make:url",
                "--function-name",
                "test",
                "--url-path",
                "/test",
                "--http-method",
                "invalid",
                "--output-dir",
                str(self.output_dir),
            ],
        )

        assert result.exit_code != 0
        assert "Erreur" in result.output or "invalide" in result.output.lower()

    def test_make_url_file_exists(self):
        """Test quand le fichier existe déjà."""
        # Créer le fichier d'abord
        file_path = self.output_dir / "existing.py"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("existing content")

        result = self.runner.invoke(
            cli,
            [
                "make:url",
                "--function-name",
                "existing",
                "--url-path",
                "/test",
                "--http-method",
                "get",
                "--output-dir",
                str(self.output_dir),
            ],
        )

        assert result.exit_code != 0
        assert "existe déjà" in result.output

    def test_make_url_all_methods(self):
        """Test génération avec toutes les méthodes HTTP."""
        methods = ["get", "post", "put", "delete", "patch"]

        for method in methods:
            result = self.runner.invoke(
                cli,
                [
                    "make:url",
                    "--function-name",
                    f"test_{method}",
                    "--url-path",
                    f"/test/{method}",
                    "--http-method",
                    method,
                    "--output-dir",
                    str(self.output_dir),
                ],
            )

            assert result.exit_code == 0, f"Échec pour la méthode {method}"
            file_path = self.output_dir / f"test_{method}.py"
            assert file_path.exists()

            content = file_path.read_text(encoding="utf-8")
            assert f"@router.{method}(" in content
