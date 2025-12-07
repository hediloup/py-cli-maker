"""Commandes CLI modulaires pour py-cli-maker."""

from py_cli_maker.commands.domaine_command import make_domaine
from py_cli_maker.commands.domaine_ddd_command import make_domaine_ddd
from py_cli_maker.commands.package_command import make_package
from py_cli_maker.commands.url_command import make_url

__all__ = ["make_url", "make_package", "make_domaine", "make_domaine_ddd"]
