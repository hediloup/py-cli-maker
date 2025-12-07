from pathlib import Path

import click

from py_cli_maker.generators.ddd_domaine_generator import (
    generate_ddd_domaine_structure,
)
from py_cli_maker.generators.domaine_generator import (
    generate_domaine_structure,
)
from py_cli_maker.generators.ninja_routes import (
    generate_ninja_route_file,
)
from py_cli_maker.generators.package_generator import (
    generate_package_structure,
)


@click.group()
def cli():
    """CLI de génération de code (type make:xxx)."""
    pass


@cli.command("make:url")
@click.option(
    "--module-name",
    "-m",
    default="api",
    help="Nom du module / app (ex: orders)",
    prompt="Nom du module / app (ex: orders)",
    prompt_required=False,
)
@click.option(
    "--function-name",
    "-f",
    default="hello",
    help="Nom de la fonction (ex: get_orders)",
    prompt="Nom de la fonction (ex: get_orders)",
    prompt_required=False,
)
@click.option(
    "--url-path",
    "-u",
    default="/hello",
    help="Chemin d'URL (ex: /orders)",
    prompt="Chemin d'URL (ex: /orders)",
    prompt_required=False,
)
@click.option(
    "--http-method",
    "-M",
    default="get",
    type=click.Choice(
        ["get", "post", "put", "delete", "patch", "head", "options"],
        case_sensitive=False,
    ),
    help="Méthode HTTP",
    prompt="Méthode HTTP",
    prompt_required=False,
)
@click.option(
    "--tag",
    "-t",
    default="Default",
    help="Tag Ninja (ex: Orders)",
    prompt="Tag Ninja (ex: Orders)",
    prompt_required=False,
)
@click.option(
    "--output-dir",
    "-o",
    default="app/api/routes",
    help="Dossier de sortie (relatif au projet Django)",
    prompt="Dossier de sortie (relatif au projet Django)",
    prompt_required=False,
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Description de l'endpoint",
)
def make_url(
    module_name, function_name, url_path, http_method, tag, output_dir, description
):
    """
    Génère un fichier .py contenant une route Django Ninja.

    Exemple d'utilisation:
        py-cli make:url --function-name get_orders --url-path /orders --http-method get
    """
    try:
        # Validation du dossier de sortie
        output_path = Path(output_dir)
        if not output_path.is_absolute():
            # Si c'est un chemin relatif, on le convertit en absolu
            # depuis le répertoire courant
            output_path = Path.cwd() / output_path

        # Si description n'est pas fournie, on demande interactivement
        if description is None:
            description = click.prompt(
                "Description de l'endpoint (optionnel, Entrée pour ignorer)",
                default="",
                show_default=False,
            )
            if not description.strip():
                description = None

        file_path = generate_ninja_route_file(
            module_name=module_name,
            function_name=function_name,
            url_path=url_path,
            http_method=http_method,
            tag=tag,
            output_dir=str(output_path),
            description=description,
        )

        click.echo(
            click.style(f"✅ Fichier généré avec succès : {file_path}", fg="green")
        )
        click.echo(
            click.style(
                "💡 N'oublie pas d'inclure ce router dans tes urls Ninja.", fg="yellow"
            )
        )
        click.echo("\nExemple d'utilisation dans votre fichier urls.py:")
        click.echo(
            f"  from {Path(file_path).parent.name}.{Path(file_path).stem} import router"
        )
        click.echo("  api.add_router(router)")

    except ValueError as e:
        click.echo(click.style(f" Erreur de validation : {e}", fg="red"), err=True)
        raise click.Abort()
    except FileExistsError as e:
        click.echo(click.style(f" Erreur : {e}", fg="red"), err=True)
        raise click.Abort()
    except OSError as e:
        click.echo(click.style(f" Erreur d'écriture : {e}", fg="red"), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f" Erreur inattendue : {e}", fg="red"), err=True)
        raise click.Abort()


@cli.command("make:package")
@click.option(
    "--project-name",
    "-p",
    default=None,
    help="Nom du projet (avec tirets, ex: my-package)",
    prompt="Nom du projet (avec tirets, ex: my-package)",
)
@click.option(
    "--package-name",
    "-n",
    default=None,
    help="Nom du package Python (avec underscores, ex: my_package)",
)
@click.option(
    "--version",
    "-v",
    default="0.1.0",
    help="Version initiale du package",
    prompt="Version initiale (ex: 0.1.0)",
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Description du package",
    prompt="Description du package",
)
@click.option(
    "--author-name",
    "-a",
    default=None,
    help="Nom de l'auteur",
    prompt="Nom de l'auteur",
)
@click.option(
    "--author-email",
    "-e",
    default=None,
    help="Email de l'auteur",
    prompt="Email de l'auteur",
)
@click.option(
    "--python-version",
    default="3.8",
    help="Version Python minimale requise (ex: 3.8)",
    prompt="Version Python minimale (ex: 3.8)",
)
@click.option(
    "--license",
    "-l",
    "license_type",
    default="MIT",
    type=click.Choice(
        ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause"], case_sensitive=False
    ),
    help="Type de licence",
    prompt="Type de licence",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Dossier de sortie où créer le package",
    prompt="Dossier de sortie",
)
@click.option(
    "--include-makefile/--no-makefile",
    default=True,
    help="Inclure un Makefile avec des commandes utiles",
)
@click.option(
    "--include-manifest/--no-manifest",
    default=True,
    help="Inclure un fichier MANIFEST.in",
)
@click.option(
    "--include-setup-py/--no-setup-py",
    default=False,
    help="Inclure setup.py (optionnel, pyproject.toml suffit)",
)
@click.option(
    "--dependencies",
    default=None,
    help="Dépendances séparées par des virgules (ex: requests>=2.0.0,click>=8.0.0)",
)
@click.option(
    "--dev-dependencies",
    default=None,
    help=(
        "Dépendances de développement séparées par des virgules "
        "(ex: pytest>=7.0.0,black>=23.0.0)"
    ),
)
@click.option(
    "--github-username",
    default=None,
    help="Nom d'utilisateur GitHub (optionnel)",
)
@click.option(
    "--homepage-url",
    default=None,
    help="URL de la page d'accueil (optionnel)",
)
def make_package(
    project_name,
    package_name,
    version,
    description,
    author_name,
    author_email,
    python_version,
    license_type,
    output_dir,
    include_makefile,
    include_manifest,
    include_setup_py,
    dependencies,
    dev_dependencies,
    github_username,
    homepage_url,
):
    """
    Génère une structure complète de package Python selon les best practices.

    Crée tous les fichiers recommandés pour un package Python moderne :
    - pyproject.toml (configuration complète)
    - README.md (template)
    - LICENSE (selon le type choisi)
    - .gitignore (standard Python)
    - Structure du package avec __init__.py
    - Structure de tests
    - MANIFEST.in (optionnel)
    - Makefile (optionnel)

    Exemple d'utilisation:
        py-cli make:package --project-name my-package --package-name my_package
    """
    try:
        # Validation du dossier de sortie
        output_path = Path(output_dir)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path

        # Génération automatique du nom de package si non fourni
        if package_name is None:
            # Utilise le project_name comme base
            package_name = project_name.replace("-", "_").lower()

        # Parsing des dépendances si fournies
        deps_list = None
        if dependencies:
            deps_list = [dep.strip() for dep in dependencies.split(",") if dep.strip()]

        dev_deps_list = None
        if dev_dependencies:
            dev_deps_list = [
                dep.strip() for dep in dev_dependencies.split(",") if dep.strip()
            ]

        package_dir = generate_package_structure(
            project_name=project_name,
            package_name=package_name,
            version=version,
            description=description,
            author_name=author_name,
            author_email=author_email,
            python_version=python_version,
            license_type=license_type,
            output_dir=str(output_path),
            include_makefile=include_makefile,
            include_manifest=include_manifest,
            include_setup_py=include_setup_py,
            dependencies=deps_list,
            dev_dependencies=dev_deps_list,
            github_username=github_username,
            homepage_url=homepage_url,
        )

        click.echo(
            click.style(f"✅ Package créé avec succès dans : {package_dir}", fg="green")
        )
        click.echo("\n📁 Structure créée :")
        click.echo(f"  {package_dir}/")
        click.echo("    ├── pyproject.toml")
        click.echo("    ├── README.md")
        click.echo("    ├── LICENSE")
        click.echo("    ├── .gitignore")
        if include_manifest:
            click.echo("    ├── MANIFEST.in")
        if include_makefile:
            click.echo("    ├── Makefile")
        click.echo(f"    ├── {package_name}/")
        click.echo("    │   └── __init__.py")
        click.echo("    └── tests/")
        click.echo("        ├── __init__.py")
        click.echo(f"        └── test_{package_name}.py")

        click.echo(click.style("\n💡 Prochaines étapes :", fg="yellow"))
        click.echo(f"  1. cd {package_dir}")
        click.echo("  2. git init")
        click.echo("  3. git add .")
        click.echo("  4. git commit -m 'Initial commit'")
        click.echo("  5. pip install -e '.[dev]'  # Installer en mode développement")

    except ValueError as e:
        click.echo(click.style(f"❌ Erreur de validation : {e}", fg="red"), err=True)
        raise click.Abort()
    except FileExistsError as e:
        click.echo(click.style(f"❌ Erreur : {e}", fg="red"), err=True)
        raise click.Abort()
    except OSError as e:
        click.echo(click.style(f"❌ Erreur d'écriture : {e}", fg="red"), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"❌ Erreur inattendue : {e}", fg="red"), err=True)
        raise click.Abort()


@cli.command("make:domaine")
@click.option(
    "--app-name",
    "-a",
    default=None,
    help="Nom de l'app Django (ex: pratique)",
    prompt="Nom de l'app Django (ex: pratique)",
)
@click.option(
    "--model-name",
    "-m",
    default=None,
    help="Nom du modèle principal (ex: Pratique)",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Dossier de sortie où créer l'app",
    prompt="Dossier de sortie",
)
@click.option(
    "--include-services/--no-services",
    default=True,
    help="Inclure services.py (recommandé)",
)
@click.option(
    "--include-selectors/--no-selectors",
    default=True,
    help="Inclure selectors.py (recommandé)",
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Description du domaine",
)
def make_domaine(
    app_name,
    model_name,
    output_dir,
    include_services,
    include_selectors,
    description,
):
    """
    Génère une structure complète de domaine Django selon les best practices.

    Crée tous les fichiers recommandés pour un domaine Django :
    - models.py (modèles Pratique, SessionPratique, etc.)
    - views.py (vues liées à la pratique)
    - urls.py (routes de cette app)
    - forms.py (formulaires liés à la pratique)
    - services.py (logique métier réutilisable, optionnel)
    - selectors.py (requêtes complexes sur les modèles, optionnel)
    - templates/pratique/ (liste.html, detail.html, formulaire.html)

    Exemple d'utilisation:
        py-cli make:domaine --app-name pratique --model-name Pratique
    """
    try:
        # Validation du dossier de sortie
        output_path = Path(output_dir)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path

        # Génération automatique du nom de modèle si non fourni
        if model_name is None:
            # Utilise l'app_name comme base et le convertit en PascalCase
            model_name = app_name.replace("_", " ").title().replace(" ", "")

        # Si description n'est pas fournie, on demande interactivement
        if description is None:
            description = click.prompt(
                "Description du domaine (optionnel, Entrée pour ignorer)",
                default="",
                show_default=False,
            )
            if not description.strip():
                description = None

        app_dir = generate_domaine_structure(
            app_name=app_name,
            model_name=model_name,
            output_dir=str(output_path),
            include_services=include_services,
            include_selectors=include_selectors,
            description=description,
        )

        click.echo(
            click.style(f"✅ Domaine créé avec succès dans : {app_dir}", fg="green")
        )
        click.echo("\n📁 Structure créée :")
        click.echo(f"  {app_dir}/")
        click.echo("    ├── __init__.py")
        click.echo("    ├── apps.py")
        click.echo("    ├── admin.py")
        click.echo("    ├── models.py")
        click.echo("    ├── views.py")
        click.echo("    ├── urls.py")
        click.echo("    ├── forms.py")
        if include_services:
            click.echo("    ├── services.py")
        if include_selectors:
            click.echo("    ├── selectors.py")
        click.echo("    └── templates/")
        click.echo(f"        └── {app_name}/")
        click.echo("            ├── liste.html")
        click.echo("            ├── detail.html")
        click.echo("            └── formulaire.html")

        click.echo(click.style("\n💡 Prochaines étapes :", fg="yellow"))
        click.echo(f"  1. Ajoutez '{app_name}' à INSTALLED_APPS dans settings.py")
        click.echo("  2. Incluez les URLs dans votre urls.py principal:")
        click.echo("     from django.urls import include, path")
        click.echo(f"     path('{app_name}/', include('{app_name}.urls')),")
        click.echo(
            f"  3. Exécutez les migrations: python manage.py makemigrations {app_name}"
        )
        click.echo("  4. Appliquez les migrations: python manage.py migrate")

    except ValueError as e:
        click.echo(click.style(f"❌ Erreur de validation : {e}", fg="red"), err=True)
        raise click.Abort()
    except FileExistsError as e:
        click.echo(click.style(f"❌ Erreur : {e}", fg="red"), err=True)
        raise click.Abort()
    except OSError as e:
        click.echo(click.style(f"❌ Erreur d'écriture : {e}", fg="red"), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"❌ Erreur inattendue : {e}", fg="red"), err=True)
        raise click.Abort()


@cli.command("make:domaine-ddd")
@click.option(
    "--app-name",
    "-a",
    default=None,
    help="Nom de l'app Django (ex: pratique)",
    prompt="Nom de l'app Django (ex: pratique)",
)
@click.option(
    "--model-name",
    "-m",
    default=None,
    help="Nom du modèle principal (ex: Pratique)",
)
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Dossier de sortie où créer l'app",
    prompt="Dossier de sortie",
)
@click.option(
    "--include-serializers/--no-serializers",
    default=True,
    help="Inclure serializers.py pour DRF (recommandé)",
)
@click.option(
    "--description",
    "-d",
    default=None,
    help="Description du domaine",
)
def make_domaine_ddd(
    app_name,
    model_name,
    output_dir,
    include_serializers,
    description,
):
    """
    Génère une structure complète de domaine Django selon les principes DDD
    (Domain-Driven Design) light.

    Crée tous les fichiers recommandés pour un domaine Django organisé en couches :
    - domain/models.py (entités métier, logique métier pure)
    - domain/services.py (règles métier complexes)
    - domain/value_objects.py (objets de valeur immutables)
    - infrastructure/repositories.py (accès DB, querysets personnalisés)
    - presentation/views.py (Django views)
    - presentation/forms.py (formulaires)
    - presentation/serializers.py (DRF serializers, optionnel)
    - presentation/urls.py (routes)
    - presentation/templates/pratique/ (templates HTML)
    - tests/ (test_models.py, test_services.py, test_views.py)

    Exemple d'utilisation:
        py-cli make:domaine-ddd --app-name pratique --model-name Pratique
    """
    try:
        # Validation du dossier de sortie
        output_path = Path(output_dir)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path

        # Génération automatique du nom de modèle si non fourni
        if model_name is None:
            # Utilise l'app_name comme base et le convertit en PascalCase
            model_name = app_name.replace("_", " ").title().replace(" ", "")

        # Si description n'est pas fournie, on demande interactivement
        if description is None:
            description = click.prompt(
                "Description du domaine (optionnel, Entrée pour ignorer)",
                default="",
                show_default=False,
            )
            if not description.strip():
                description = None

        app_dir = generate_ddd_domaine_structure(
            app_name=app_name,
            model_name=model_name,
            output_dir=str(output_path),
            include_serializers=include_serializers,
            description=description,
        )

        click.echo(
            click.style(f"✅ Domaine DDD créé avec succès dans : {app_dir}", fg="green")
        )
        click.echo("\n📁 Structure créée :")
        click.echo(f"  {app_dir}/")
        click.echo("    ├── __init__.py")
        click.echo("    ├── apps.py")
        click.echo("    ├── admin.py")
        click.echo("    ├── domain/")
        click.echo("    │   ├── models.py")
        click.echo("    │   ├── services.py")
        click.echo("    │   └── value_objects.py")
        click.echo("    ├── infrastructure/")
        click.echo("    │   └── repositories.py")
        click.echo("    ├── presentation/")
        click.echo("    │   ├── views.py")
        click.echo("    │   ├── forms.py")
        if include_serializers:
            click.echo("    │   ├── serializers.py")
        click.echo("    │   └── urls.py")
        click.echo(f"    ├── templates/{app_name}/")
        click.echo("    │   ├── liste.html")
        click.echo("    │   ├── detail.html")
        click.echo("    │   └── formulaire.html")
        click.echo("    └── tests/")
        click.echo("        ├── test_models.py")
        click.echo("        ├── test_services.py")
        click.echo("        └── test_views.py")

        click.echo(click.style("\n💡 Prochaines étapes :", fg="yellow"))
        click.echo(f"  1. Ajoutez '{app_name}' à INSTALLED_APPS dans settings.py")
        click.echo("  2. Incluez les URLs dans votre urls.py principal:")
        click.echo("     from django.urls import include, path")
        click.echo(
            f"     path('{app_name}/', include('{app_name}.presentation.urls')),"
        )
        click.echo(
            f"  3. Exécutez les migrations: python manage.py makemigrations {app_name}"
        )
        click.echo("  4. Appliquez les migrations: python manage.py migrate")
        if include_serializers:
            click.echo(
                "  5. Assurez-vous d'avoir 'rest_framework' dans INSTALLED_APPS "
                "pour les serializers"
            )

    except ValueError as e:
        click.echo(click.style(f"❌ Erreur de validation : {e}", fg="red"), err=True)
        raise click.Abort()
    except FileExistsError as e:
        click.echo(click.style(f"❌ Erreur : {e}", fg="red"), err=True)
        raise click.Abort()
    except OSError as e:
        click.echo(click.style(f"❌ Erreur d'écriture : {e}", fg="red"), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"❌ Erreur inattendue : {e}", fg="red"), err=True)
        raise click.Abort()
