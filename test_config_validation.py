"""
Environment and Configuration Validation Tests
Ensures all required environment variables are set and accessible
"""

import pytest
import os
from src.utils.config import settings, require_database_url


class TestEnvironmentVariables:
    """Test environment variable configuration"""

    def test_database_url_set(self):
        """DATABASE_URL should be set in .env"""
        assert settings.DATABASE_URL is not None, "DATABASE_URL not set in .env"
        assert settings.DATABASE_URL.startswith("postgresql://"), "DATABASE_URL should use PostgreSQL"

    def test_app_env_is_development(self):
        """APP_ENV should be development or production"""
        assert settings.APP_ENV in ["development", "production"], f"Invalid APP_ENV: {settings.APP_ENV}"

    def test_log_level_valid(self):
        """LOG_LEVEL should be a valid logging level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert settings.LOG_LEVEL in valid_levels, f"Invalid LOG_LEVEL: {settings.LOG_LEVEL}"

    def test_api_host_set(self):
        """API_HOST should be set"""
        assert settings.APP_HOST is not None
        assert len(settings.APP_HOST) > 0

    def test_api_port_valid(self):
        """API_PORT should be a valid port number"""
        assert 1 <= settings.APP_PORT <= 65535, f"Invalid port: {settings.APP_PORT}"

    def test_cors_origins_not_empty(self):
        """ALLOWED_ORIGINS should have at least one entry"""
        origins = settings.origins_list
        assert len(origins) > 0, "ALLOWED_ORIGINS is empty"

    def test_api_prefix_set(self):
        """API_PREFIX should be set"""
        assert settings.API_PREFIX == "/api/0.1.0"

    def test_api_version_set(self):
        """API_VERSION should be set"""
        assert settings.API_VERSION == "0.1.0"


class TestDatabaseConfiguration:
    """Test database-specific configuration"""

    def test_database_url_parseable(self):
        """DATABASE_URL should be a valid PostgreSQL connection string"""
        url = settings.DATABASE_URL
        assert url is not None
        assert "postgresql://" in url or "postgres://" in url
        assert "@" in url, "DATABASE_URL should contain credentials"
        assert "/" in url.split("@")[1], "DATABASE_URL should contain database name"

    def test_require_database_url_function(self):
        """require_database_url() should return valid URL"""
        url = require_database_url()
        assert url is not None
        assert "postgresql://" in url or "postgres://" in url


class TestCORSConfiguration:
    """Test CORS configuration"""

    def test_allowed_origins_is_parseable(self):
        """ALLOWED_ORIGINS should parse to a list"""
        origins = settings.origins_list
        assert isinstance(origins, list)

    def test_allowed_methods_is_parseable(self):
        """ALLOWED_METHODS should parse to a list"""
        methods = settings.methods_list
        assert isinstance(methods, list)

    def test_allow_credentials_is_bool(self):
        """ALLOW_CREDENTIALS should be boolean"""
        assert isinstance(settings.ALLOW_CREDENTIALS, bool)


class TestApplicationSettings:
    """Test general application settings"""

    def test_settings_object_created(self):
        """Settings object should be instantiated"""
        assert settings is not None

    def test_app_title_set(self):
        """API_TITLE should be set"""
        assert settings.API_TITLE is not None
        assert len(settings.API_TITLE) > 0

    def test_app_description_set(self):
        """API_DESCRIPTION should be set"""
        assert settings.API_DESCRIPTION is not None
        assert len(settings.API_DESCRIPTION) > 0

    def test_settings_from_env_file(self):
        """Settings should load from .env file"""
        # If DATABASE_URL is set, it came from .env
        assert settings.DATABASE_URL is not None


class TestEnvironmentValidation:
    """End-to-end environment validation"""

    def test_production_config_strict(self):
        """In production, ALLOWED_ORIGINS should not be wildcard"""
        if settings.APP_ENV == "production":
            origins = settings.origins_list
            assert "*" not in origins, \
                "Production should not allow wildcard CORS origins"

    def test_development_config_permissive(self):
        """In development, ALLOWED_ORIGINS can be permissive"""
        if settings.APP_ENV == "development":
            origins = settings.origins_list
            origins_str = ",".join(origins)
            # Should allow localhost variants or wildcard
            assert "localhost" in origins_str or "127.0.0.1" in origins_str or "*" in origins_str

    def test_env_file_exists(self):
        """At least one .env file should exist"""
        assert os.path.exists(".env") or os.path.exists(".env.example"), \
            "Neither .env nor .env.example found"


class TestConfigurationIntegration:
    """Test that configuration works with FastAPI"""

    def test_origins_list_property(self):
        """origins_list property should return list"""
        origins = settings.origins_list
        assert isinstance(origins, list)
        assert all(isinstance(o, str) for o in origins)

    def test_methods_list_property(self):
        """methods_list property should return list"""
        methods = settings.methods_list
        assert isinstance(methods, list)
        assert all(isinstance(m, str) for m in methods)

    def test_headers_list_property(self):
        """headers_list property should return list"""
        headers = settings.headers_list
        assert isinstance(headers, list)
        assert all(isinstance(h, str) for h in headers)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
