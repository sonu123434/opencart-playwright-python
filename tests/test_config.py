import json

import pytest

from config import build_url, get_base_url


def configure_settings_file(tmp_path, monkeypatch, settings):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps(settings),
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENCART_CREDENTIALS_FILE", str(settings_path))
    return settings_path


def test_base_url_is_loaded_from_settings_file(tmp_path, monkeypatch):
    configure_settings_file(
        tmp_path,
        monkeypatch,
        {"base_url": "https://shop.example/store/"},
    )
    monkeypatch.delenv("OPENCART_BASE_URL", raising=False)

    assert get_base_url() == "https://shop.example/store/"
    assert build_url("/index.php?route=common/home") == (
        "https://shop.example/store/index.php?route=common/home"
    )


def test_environment_base_url_overrides_settings_file(tmp_path, monkeypatch):
    configure_settings_file(
        tmp_path,
        monkeypatch,
        {"base_url": "https://shop.example/store/"},
    )
    monkeypatch.setenv("OPENCART_BASE_URL", "https://staging.example/opencart")

    assert get_base_url() == "https://staging.example/opencart/"
    assert build_url("/index.php?route=common/home") == (
        "https://staging.example/opencart/index.php?route=common/home"
    )


def test_named_environment_uses_its_profile(tmp_path, monkeypatch):
    configure_settings_file(
        tmp_path,
        monkeypatch,
        {
            "environments": {
                "qa": {"base_url": "https://qa.example.com/store/"},
                "staging": {"base_url": "https://staging.example.com/store/"},
            }
        },
    )
    monkeypatch.setenv("OPENCART_ENV", "staging")
    monkeypatch.delenv("OPENCART_BASE_URL", raising=False)

    assert get_base_url() == "https://staging.example.com/store/"


def test_named_environment_requires_a_profile(tmp_path, monkeypatch):
    configure_settings_file(
        tmp_path,
        monkeypatch,
        {"environments": {"qa": {"base_url": "https://qa.example.com/"}}},
    )
    monkeypatch.setenv("OPENCART_ENV", "production")
    monkeypatch.delenv("OPENCART_BASE_URL", raising=False)

    with pytest.raises(ValueError, match="No configuration found"):
        get_base_url()


def test_non_qa_environment_does_not_use_default_qa_url(tmp_path, monkeypatch):
    configure_settings_file(
        tmp_path,
        monkeypatch,
        {"environments": {"qa": {"base_url": "https://qa.example.com/"}}},
    )
    monkeypatch.setenv("OPENCART_ENV", "uat")
    monkeypatch.delenv("OPENCART_BASE_URL", raising=False)

    with pytest.raises(ValueError, match="No configuration found|No base_url configured"):
        get_base_url()


def test_base_url_rejects_invalid_scheme(monkeypatch):
    monkeypatch.setenv("OPENCART_BASE_URL", "ftp://shop.example")

    with pytest.raises(ValueError, match="http:// or https://"):
        get_base_url()
