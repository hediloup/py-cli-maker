# py-cli-maker

CLI pour générer des fichiers Python et routes Django Ninja de manière interactive.

## Description

`py-cli-maker` est un outil en ligne de commande qui facilite la génération de routes Django Ninja. Il pose des questions interactives et génère automatiquement des fichiers Python avec les routes configurées.

##  Installation

### Installation depuis le code source

#### Avec uv (recommandé)

```bash
# Cloner le dépôt
git clone https://github.com/hedi/py-cli-maker.git
cd py-cli-maker

# Créer un environnement virtuel (si pas déjà fait)
uv venv

# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Synchroniser toutes les dépendances (y compris dev)
uv sync

# Ou installer en mode développement avec uv pip
uv pip install -e ".[dev]"
```

**⚠️ Important avec uv :**
-  **Ne pas utiliser** : `uv run pip install` (cela provoque une erreur "externally-managed-environment")
-  **Utiliser** : `uv sync` ou `uv pip install` directement

#### Avec pip standard

```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Installer en mode développement
pip install -e .

# Ou installer avec les dépendances de développement
pip install -e ".[dev]"
```

### Installation depuis PyPI (quand disponible)

```bash
pip install py-cli-maker
```

## Utilisation

### Génération interactive

La méthode la plus simple est d'utiliser le mode interactif :

```bash
py-cli make:url
```

Le CLI vous posera alors des questions sur :
- Le nom du module/app
- Le nom de la fonction
- Le chemin d'URL
- La méthode HTTP (get, post, put, delete, etc.)
- Le tag Ninja
- Le dossier de sortie
- La description de l'endpoint (optionnel)

### Génération avec options

Vous pouvez également fournir toutes les options directement :

```bash
py-cli make:url \
  --function-name get_orders \
  --url-path /orders \
  --http-method get \
  --tag Orders \
  --output-dir app/api/routes \
  --description "Récupère la liste des commandes"
```

### Options disponibles

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|--------|
| `--module-name` | `-m` | Nom du module/app | `api` |
| `--function-name` | `-f` | Nom de la fonction | `hello` |
| `--url-path` | `-u` | Chemin d'URL | `/hello` |
| `--http-method` | `-M` | Méthode HTTP | `get` |
| `--tag` | `-t` | Tag Ninja | `Default` |
| `--output-dir` | `-o` | Dossier de sortie | `app/api/routes` |
| `--description` | `-d` | Description de l'endpoint | Optionnel |

### Exemple de fichier généré

Pour la commande `py-cli make:url --function-name get_orders --url-path /orders --http-method get --tag Orders`, le fichier `get_orders.py` sera créé :

```python
from ninja import Router

router = Router(tags=["Orders"])


@router.get("/orders")
def get_orders(request):
    """
    Endpoint get_orders
    """
    return {"message": "Hello from get_orders!"}
```

### Intégration dans votre projet Django

Après la génération, n'oubliez pas d'inclure le router dans votre fichier `urls.py` :

```python
from django.urls import path
from ninja import NinjaAPI
from app.api.routes.get_orders import router as orders_router

api = NinjaAPI()

api.add_router(orders_router, prefix="/api")

urlpatterns = [
    path("api/", api.urls),
]
```

## 🔧 Dépannage : Erreur "externally-managed-environment"

### Pourquoi cette erreur se produit ?

Si vous obtenez l'erreur `externally-managed-environment` avec `uv run pip install`, c'est parce que :

1. **`uv run pip install` n'est pas la bonne commande** : `uv run` exécute une commande dans l'environnement virtuel, mais `pip` essaie d'installer dans l'environnement système Python (protégé par PEP 668).

2. **Solution avec uv** : Utilisez directement les commandes `uv` :
   ```bash
   # ✅ CORRECT - Synchroniser depuis pyproject.toml
   uv sync
   
   # ✅ CORRECT - Installer avec uv pip (sans "run")
   uv pip install -e ".[dev]"
   
   # ❌ INCORRECT - Ne pas utiliser cette commande
   uv run pip install ...
   ```

3. **Alternative** : Si vous voulez utiliser `pip` directement, activez d'abord l'environnement virtuel :
   ```bash
   # Activer l'environnement virtuel
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate  # Windows
   
   # Puis utiliser pip normalement
   pip install -e ".[dev]"
   ```

##  Outils de qualité de code pour développeurs

Ce projet utilise plusieurs outils pour maintenir un code de qualité. Voici comment les utiliser :

### Installation des outils

#### Avec uv (recommandé)

```bash
# Synchroniser toutes les dépendances de développement depuis pyproject.toml
uv sync

# Ou installer en mode développement
uv pip install -e ".[dev]"

# Ou utiliser les dependency-groups de uv
uv sync --group dev
```

#### Avec pip standard

```bash
# Installer tous les outils de développement
pip install -e ".[dev]"

# Ou installer individuellement
pip install black ruff mypy pytest pytest-cov ipdb
```

**⚠️ Erreur courante avec uv :**
Si vous obtenez l'erreur `externally-managed-environment` :
- ❌ **Ne pas utiliser** : `uv run pip install ...`
- ✅ **Utiliser** : `uv sync` ou `uv pip install ...` directement

### 1. Black - Formatage automatique

**Black** formate automatiquement votre code selon le style PEP 8.

#### Utilisation

**Avec uv :**
```bash
# Vérifier ce qui sera changé (sans modifier)
uv run black --check py_cli_maker/

# Formater tous les fichiers Python
uv run black py_cli_maker/ tests/

# Formater un fichier spécifique
uv run black py_cli_maker/cli.py
```

**Avec pip standard :**
```bash
# Vérifier ce qui sera changé (sans modifier)
black --check py_cli_maker/

# Formater tous les fichiers Python
black py_cli_maker/ tests/

# Formater un fichier spécifique
black py_cli_maker/cli.py
```

#### Configuration

La configuration de Black est dans `pyproject.toml` :

```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']
include = '\.pyi?$'
```

#### Intégration dans l'éditeur

Pour un formatage automatique à la sauvegarde, configurez votre éditeur (VS Code, PyCharm, etc.) pour utiliser Black.

### 2. Ruff - Linting ultra-rapide

**Ruff** est un linter ultra-rapide qui remplace Flake8, isort et d'autres outils.

#### Utilisation

**Avec uv :**
```bash
# Vérifier les erreurs
uv run ruff check py_cli_maker/ tests/

# Corriger automatiquement ce qui peut l'être
uv run ruff check --fix py_cli_maker/ tests/

# Vérifier un fichier spécifique
uv run ruff check py_cli_maker/cli.py

# Formater les imports (remplace isort)
uv run ruff format py_cli_maker/
```

**Avec pip standard :**
```bash
# Vérifier les erreurs
ruff check py_cli_maker/ tests/

# Corriger automatiquement ce qui peut l'être
ruff check --fix py_cli_maker/ tests/

# Vérifier un fichier spécifique
ruff check py_cli_maker/cli.py

# Formater les imports (remplace isort)
ruff format py_cli_maker/
```

#### Configuration

La configuration de Ruff est dans `pyproject.toml` :

```toml
[tool.ruff]
line-length = 88
target-version = "py38"
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []
```

#### Codes d'erreur

Consultez la [documentation des règles Ruff](https://docs.astral.sh/ruff/rules/) pour comprendre les codes d'erreur.

### 3. Mypy - Vérification de types statique

**Mypy** vérifie que vous utilisez correctement les annotations de types.

#### Utilisation

**Avec uv :**
```bash
# Vérifier les types dans tout le projet
uv run mypy py_cli_maker/

# Vérifier un fichier spécifique
uv run mypy py_cli_maker/cli.py

# Mode strict (recommandé pour les nouveaux projets)
uv run mypy --strict py_cli_maker/
```

**Avec pip standard :**
```bash
# Vérifier les types dans tout le projet
mypy py_cli_maker/

# Vérifier un fichier spécifique
mypy py_cli_maker/cli.py

# Mode strict (recommandé pour les nouveaux projets)
mypy --strict py_cli_maker/
```

#### Configuration

La configuration de Mypy est dans `pyproject.toml` :

```toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
```

#### Exemple d'annotation de types

```python
def generate_ninja_route_file(
    module_name: str,
    function_name: str,
    url_path: str,
    http_method: str,
    tag: str,
    output_dir: str,
    description: str | None = None,
) -> str:
    """Génère un fichier Python contenant une route Django Ninja."""
    # ...
```

### 4. Pytest - Framework de tests

**Pytest** est utilisé pour exécuter les tests automatisés.

#### Utilisation

**Avec uv :**
```bash
# Exécuter tous les tests
uv run pytest

# Mode verbose (affiche plus de détails)
uv run pytest -v

# Mode très verbose
uv run pytest -vv

# Exécuter un fichier de test spécifique
uv run pytest tests/test_ninja_routes.py

# Exécuter une classe de test spécifique
uv run pytest tests/test_ninja_routes.py::TestSanitizeFuncName

# Exécuter un test spécifique
uv run pytest tests/test_ninja_routes.py::TestSanitizeFuncName::test_simple_name

# Exécuter avec couverture de code
uv run pytest --cov=py_cli_maker --cov-report=term-missing

# Générer un rapport HTML de couverture
uv run pytest --cov=py_cli_maker --cov-report=html
# Ouvrir htmlcov/index.html dans votre navigateur
```

**Avec pip standard :**
```bash
# Exécuter tous les tests
pytest

# Mode verbose (affiche plus de détails)
pytest -v

# Mode très verbose
pytest -vv

# Exécuter un fichier de test spécifique
pytest tests/test_ninja_routes.py

# Exécuter une classe de test spécifique
pytest tests/test_ninja_routes.py::TestSanitizeFuncName

# Exécuter un test spécifique
pytest tests/test_ninja_routes.py::TestSanitizeFuncName::test_simple_name

# Exécuter avec couverture de code
pytest --cov=py_cli_maker --cov-report=term-missing

# Générer un rapport HTML de couverture
pytest --cov=py_cli_maker --cov-report=html
# Ouvrir htmlcov/index.html dans votre navigateur
```

#### Structure des tests

Les tests sont organisés dans le dossier `tests/` :

```
tests/
├── __init__.py
├── test_ninja_routes.py  # Tests pour le générateur
└── test_cli.py           # Tests pour l'interface CLI
```

#### Exemple de test

```python
def test_sanitize_func_name():
    """Test avec un nom simple."""
    assert _sanitize_func_name("get_orders") == "get_orders"
    assert _sanitize_func_name("get orders") == "get_orders"
```

### 5. ipdb - Débogueur interactif

**ipdb** est un débogueur interactif amélioré pour Python.

#### Configuration

```bash
# Configurer ipdb comme débogueur par défaut
export PYTHONBREAKPOINT=ipdb.set_trace

# Ou dans votre shell (bash/zsh)
echo 'export PYTHONBREAKPOINT=ipdb.set_trace' >> ~/.bashrc
```

#### Utilisation dans le code

```python
def generate_ninja_route_file(...):
    # Votre code
    breakpoint()  # Le débogueur s'arrête ici
    # Suite du code
```

#### Commandes principales

Une fois dans le débogueur :

| Commande | Description |
|----------|-------------|
| `n` (next) | Exécute la ligne suivante |
| `s` (step) | Entre dans une fonction |
| `c` (continue) | Continue jusqu'au prochain point d'arrêt |
| `l` (list) | Affiche le code autour de la ligne actuelle |
| `p variable` | Affiche la valeur d'une variable |
| `pp variable` | Affiche joliment la valeur d'une variable |
| `u` (up) | Remonte dans la pile d'appels |
| `d` (down) | Descend dans la pile d'appels |
| `q` (quit) | Quitte le débogueur |

#### Exemple d'utilisation

```python
def test_function():
    a = 10
    b = 5
    breakpoint()  # Arrêt ici
    result = a + b
    return result
```

Exécutez avec : `python -m pytest tests/test_file.py::test_function`

#### Analyse post-mortem

Pour inspecter l'état du programme après une erreur :

```python
def test_with_error():
    try:
        result = division(10, 0)
    except Exception as e:
        import ipdb; ipdb.post_mortem()
        raise
```

## 🔄 Workflow de développement recommandé

### Avec uv

1. **Installer les dépendances**
   ```bash
   uv sync
   ```

2. **Écrire le code**
   ```bash
   # Créer/modifier vos fichiers
   ```

3. **Formater avec Black**
   ```bash
   uv run black py_cli_maker/ tests/
   ```

4. **Vérifier avec Ruff**
   ```bash
   uv run ruff check --fix py_cli_maker/ tests/
   ```

5. **Vérifier les types avec Mypy**
   ```bash
   uv run mypy py_cli_maker/
   ```

6. **Exécuter les tests**
   ```bash
   uv run pytest -v
   ```

7. **Vérifier la couverture**
   ```bash
   uv run pytest --cov=py_cli_maker --cov-report=term-missing
   ```

### Avec pip standard

1. **Écrire le code**
   ```bash
   # Créer/modifier vos fichiers
   ```

2. **Formater avec Black**
   ```bash
   black py_cli_maker/ tests/
   ```

3. **Vérifier avec Ruff**
   ```bash
   ruff check --fix py_cli_maker/ tests/
   ```

4. **Vérifier les types avec Mypy**
   ```bash
   mypy py_cli_maker/
   ```

5. **Exécuter les tests**
   ```bash
   pytest -v
   ```

6. **Vérifier la couverture**
   ```bash
   pytest --cov=py_cli_maker --cov-report=term-missing
   ```

## 📦 Utilisation du Makefile

Le projet inclut un `Makefile` qui automatise toutes les tâches de développement. Le Makefile détecte automatiquement si vous utilisez `uv` ou `pip` standard.

### Afficher l'aide

Pour voir toutes les commandes disponibles :

```bash
make help
```

Ou simplement :

```bash
make
```

### Commandes disponibles

#### Installation

```bash
# Installer les dépendances de développement
make install-dev
```

Cette commande :
- Essaie d'abord d'utiliser `uv sync` (si `uv` est installé)
- Sinon, utilise `pip install -e ".[dev]"`

#### Formatage et qualité de code

```bash
# Formater le code avec Black
make format

# Vérifier et corriger le code avec Ruff
make lint

# Vérifier les types avec Mypy
make type
```

#### Tests

```bash
# Exécuter tous les tests
make test

# Exécuter les tests avec couverture de code
make coverage
```

La commande `coverage` génère :
- Un rapport dans le terminal
- Un rapport HTML dans `htmlcov/index.html` (ouvrez-le dans votre navigateur)

#### Pipeline complet

```bash
# Exécuter tous les outils de qualité en une seule commande
make quality
```

Cette commande exécute dans l'ordre :
1. `make format` - Formate le code
2. `make lint` - Vérifie et corrige le code
3. `make type` - Vérifie les types
4. `make test` - Exécute les tests

C'est la commande recommandée avant de committer votre code !

#### Nettoyage

```bash
# Nettoyer tous les fichiers temporaires
make clean
```

Cette commande supprime :
- Les dossiers `__pycache__`
- Les fichiers `.pyc` et `.pyo`
- Les dossiers `.egg-info`
- Les caches de pytest, mypy, ruff
- Les rapports de couverture

### Exemples d'utilisation

#### Workflow quotidien

```bash
# 1. Installer les dépendances (une seule fois)
make install-dev

# 2. Travailler sur votre code...

# 3. Avant de committer, exécuter le pipeline complet
make quality

# 4. Si tout passe, committer
git add .
git commit -m "Ma nouvelle fonctionnalité"
```

#### Vérification rapide

```bash
# Juste formater le code
make format

# Juste vérifier les erreurs
make lint

# Juste exécuter les tests
make test
```

#### Après les tests

```bash
# Générer un rapport de couverture détaillé
make coverage

# Ouvrir le rapport HTML
# Linux/Mac
open htmlcov/index.html
# Windows
start htmlcov/index.html
```

### Avantages du Makefile

1. **Détection automatique** : Détecte si vous utilisez `uv` ou `pip` et utilise la bonne commande
2. **Commandes simples** : `make quality` au lieu de taper plusieurs commandes
3. **Cohérence** : Tous les développeurs utilisent les mêmes commandes
4. **Documentation** : `make help` montre toutes les commandes disponibles

### Commandes équivalentes

Si vous préférez utiliser les commandes directement :

| Makefile | Commande équivalente (avec uv) | Commande équivalente (avec pip) |
|----------|--------------------------------|----------------------------------|
| `make format` | `uv run black py_cli_maker/ tests/` | `black py_cli_maker/ tests/` |
| `make lint` | `uv run ruff check --fix py_cli_maker/ tests/` | `ruff check --fix py_cli_maker/ tests/` |
| `make type` | `uv run mypy py_cli_maker/` | `mypy py_cli_maker/` |
| `make test` | `uv run pytest -v` | `pytest -v` |
| `make coverage` | `uv run pytest --cov=py_cli_maker --cov-report=html` | `pytest --cov=py_cli_maker --cov-report=html` |
| `make quality` | `uv run black ... && uv run ruff ... && uv run mypy ... && uv run pytest` | `black ... && ruff ... && mypy ... && pytest` |

##  Structure du projet

```
py-cli-maker/
├── py_cli_maker/          # Code source du package
│   ├── __init__.py
│   ├── cli.py             # Interface CLI
│   └── generators/        # Générateurs
│       ├── __init__.py
│       └── ninja_routes.py
├── tests/                 # Tests
│   ├── __init__.py
│   ├── test_ninja_routes.py
│   └── test_cli.py
├── pyproject.toml         # Configuration du projet
└── README.md             # Ce fichier
```

## Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

**N'oubliez pas** d'exécuter les outils de qualité avant de soumettre :
```bash
make quality  # ou exécutez les commandes individuellement
```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Liens utiles

- [Documentation Django Ninja](https://django-ninja.rest-framework.com/)
- [Documentation Click](https://click.palletsprojects.com/)
- [Documentation Black](https://black.readthedocs.io/)
- [Documentation Ruff](https://docs.astral.sh/ruff/)
- [Documentation Mypy](https://mypy.readthedocs.io/)
- [Documentation Pytest](https://docs.pytest.org/)

## 👤 Auteur

**Hedi** - hedi@dhib.com

## Remerciements

- Django Ninja pour le framework de routes
- Click pour l'interface CLI
- La communauté Python pour les outils de qualité

