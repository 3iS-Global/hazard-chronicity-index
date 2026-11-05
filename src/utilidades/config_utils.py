"""Carga y validación de la configuración YAML del proyecto EFCI Ecuador.

English:
Load and validate the project's YAML configuration.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class ConfigError(RuntimeError):
    """Se lanza cuando el archivo de configuración no existe o es inválido.

    English:
    Raised when the configuration file does not exist or is invalid.
    """


def load_config(config_path: str | Path) -> dict[str, Any]:
    """Carga el archivo de configuración YAML del proyecto.

    Args:
        config_path: Ruta al archivo ``config.yaml`` (absoluta o relativa al
            directorio de trabajo actual).

    Returns:
        Diccionario con la configuración completa del proyecto (rutas,
        alcance de peligros, umbrales, etc.).

    Raises:
        ConfigError: Si el archivo no existe o no se puede parsear como YAML.

    Example:
        >>> cfg = load_config("config/config.yaml")
        >>> cfg["hazard_scope"]["Inundación"]
        'flood'

    English:
    Load the project's YAML configuration file.

    Args:
        config_path: Path to ``config.yaml`` (absolute, or relative to the current working directory).

    Returns:
        Dictionary with the full project configuration (paths, hazard scope, thresholds, etc.).

    Raises:
        ConfigError: If the file does not exist or cannot be parsed as YAML.
    """
    path = Path(config_path)
    if not path.exists():
        # Fallamos rápido y con un mensaje claro: preferible a un KeyError
        # críptico más adelante en el pipeline.
        # Fail fast with a clear message: better than a cryptic KeyError later in the pipeline.
        raise ConfigError(f"No se encontró el archivo de configuración: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            config: dict[str, Any] = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ConfigError(f"Error al parsear {path} como YAML: {exc}") from exc

    if not config:
        raise ConfigError(f"El archivo de configuración {path} está vacío.")

    logger.info("Configuración cargada desde %s", path)
    return config


def resolve_path(config: dict[str, Any], key: str, base_dir: str | Path) -> Path:
    """Resuelve una ruta relativa declarada en ``paths`` contra un directorio base.

    Args:
        config: Diccionario de configuración cargado con :func:`load_config`.
        key: Nombre de la clave dentro de ``config["paths"]`` (p. ej. ``"raw_workbook"``).
        base_dir: Directorio base contra el cual se resuelve la ruta relativa
            (normalmente el directorio donde vive el notebook o script que llama).

    Returns:
        Ruta absoluta resuelta.

    Raises:
        ConfigError: Si la clave no existe en ``config["paths"]``.

    English:
    Resolve a relative path declared under ``paths`` against a base directory.

    Args:
        config: Configuration dictionary loaded with :func:`load_config`.
        key: Key inside ``config["paths"]`` (e.g. ``"raw_workbook"``).
        base_dir: Base directory used to resolve the relative path (usually the folder of the calling notebook or script).

    Returns:
        Resolved absolute path.

    Raises:
        ConfigError: If the key does not exist.
    """
    try:
        raw_path = config["paths"][key]
    except KeyError as exc:
        raise ConfigError(f"La clave 'paths.{key}' no existe en la configuración.") from exc

    resolved = (Path(base_dir) / raw_path).resolve()
    return resolved
