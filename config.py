import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

DEFAULT_BASE_URL = "https://naveenautomationlabs.com/opencart/"
HOME_PATH = "/index.php?route=common/home"
LOGIN_PATH = "/index.php?route=account/login"
ACCOUNT_PATH = "/index.php?route=account/account"
CART_PATH = "/index.php?route=checkout/cart"
DESKTOP_CATEGORY_PATH = "/index.php?route=product/category&path=20"
MAC_CATEGORY_PATH = "/index.php?route=product/category&path=20_27"
IMAC_PRODUCT_PATH = "/index.php?route=product/product&path=20_27&product_id=41"
DEFAULT_TIMEOUT = 20_000
SUPPORTED_ENVIRONMENTS = {"qa", "uat", "staging", "production"}


def local_settings_path() -> Path:
    configured_path = os.getenv("OPENCART_CREDENTIALS_FILE")
    if configured_path:
        path = Path(configured_path)
        return path if path.is_absolute() else Path.cwd() / path
    return Path(__file__).resolve().parent / "credentials.json"


def load_local_settings() -> dict[str, Any]:
    settings_path = local_settings_path()
    if not settings_path.is_file():
        return {}

    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {settings_path}: {error}") from error

    if not isinstance(settings, dict):
        raise ValueError(f"Settings file must contain a JSON object: {settings_path}")
    return settings


def get_environment() -> str:
    environment = os.getenv("OPENCART_ENV", "qa").strip().lower()
    if environment not in SUPPORTED_ENVIRONMENTS:
        supported = ", ".join(sorted(SUPPORTED_ENVIRONMENTS))
        raise ValueError(f"OPENCART_ENV must be one of: {supported}.")
    return environment


def get_environment_settings(settings: dict[str, Any] | None = None) -> dict[str, Any]:
    settings = load_local_settings() if settings is None else settings
    profiles = settings.get("environments", {})
    if not isinstance(profiles, dict):
        raise ValueError("The 'environments' setting must be a JSON object.")
    if not profiles:
        return {}

    environment = get_environment()
    profile = profiles.get(environment)
    if not isinstance(profile, dict):
        raise ValueError(f"No configuration found for the '{environment}' environment.")
    return profile


def get_base_url() -> str:
    configured_url = os.getenv("OPENCART_BASE_URL")
    if configured_url == "":
        configured_url = None
    if configured_url is None:
        settings = load_local_settings()
        environment = get_environment()
        profile = get_environment_settings(settings)
        if profile:
            configured_url = profile.get("base_url")
            if configured_url is None:
                raise ValueError(f"No base_url configured for the '{environment}' environment.")
        elif environment != "qa":
            raise ValueError(f"No base_url configured for the '{environment}' environment.")
        else:
            configured_url = settings.get("base_url", DEFAULT_BASE_URL)

    if not isinstance(configured_url, str) or not configured_url.strip():
        raise ValueError("The configured base_url must be a non-empty URL string.")

    configured_url = configured_url.strip()
    parsed_url = urlsplit(configured_url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError("The configured base_url must start with http:// or https://.")

    return configured_url.rstrip("/") + "/"


def build_url(path: str) -> str:
    return f"{get_base_url().rstrip('/')}/{path.lstrip('/')}"
