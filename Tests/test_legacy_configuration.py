"""Behavioral checks for externalized configuration; no database/network access."""

import importlib.util
import os
from pathlib import Path
import secrets
import subprocess
import sys
import unittest
from unittest.mock import patch, MagicMock

ROOT = Path(__file__).resolve().parents[1]


def load_auth():
    spec = importlib.util.spec_from_file_location("legacy_auth_check", ROOT / "utiils/auth.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LegacyConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.environment = {
            "FLASK_SECRET_KEY": secrets.token_urlsafe(32),
            "JWT_SECRET_KEY": secrets.token_urlsafe(32),
            "MYSQL_HOST": "127.0.0.1",
            "MYSQL_USER": "demo-user",
            "MYSQL_PASSWORD": secrets.token_urlsafe(32),
            "MYSQL_DATABASE": "petland_demo",
        }

    def test_missing_or_empty_session_key_fails_startup(self):
        for value in [None, ""]:
            env = dict(os.environ, **self.environment)
            env.pop("FLASK_SECRET_KEY")
            if value is not None:
                env["FLASK_SECRET_KEY"] = value
            result = subprocess.run([sys.executable, "-c", "import app"], cwd=ROOT, env=env, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(b"FLASK_SECRET_KEY" in result.stderr)

    def test_missing_or_empty_jwt_key_fails_import(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(KeyError):
                load_auth()
            os.environ["JWT_SECRET_KEY"] = ""
            with self.assertRaises(RuntimeError):
                load_auth()

    def test_session_configuration_and_public_pages(self):
        with patch.dict(os.environ, self.environment):
            from app import app
            self.assertTrue(app.secret_key == self.environment["FLASK_SECRET_KEY"])
            with app.test_client() as client:
                for route in ["/api/tela_login", "/api/tela_cadastro", "/api/telalogin_funcionario"]:
                    self.assertEqual(client.get(route).status_code, 200, route)
                response = client.get("/api/tela_inicial")
                self.assertEqual(response.status_code, 302)
                self.assertIn("/api/tela_login", response.headers["Location"])

    def test_jwt_roundtrip_and_changed_key_rejection(self):
        with patch.dict(os.environ, self.environment):
            auth = load_auth()
            token = auth.gerar_token("00000000000", "cliente")
            self.assertEqual(auth.verificar_token(token)["tipo_usuario"], "cliente")
            auth.SECRET_KEY = secrets.token_urlsafe(32)
            self.assertIsNone(auth.verificar_token(token))
            self.assertIsNone(auth.verificar_token("invalid-test-token"))

    def test_both_mysql_paths_use_environment(self):
        with patch.dict(os.environ, self.environment):
            import config.database as database
            auth = load_auth()
            for connect in [database.create_connection, auth.get_db_connection]:
                with patch("mysql.connector.connect", return_value=MagicMock()) as mock:
                    connect()
                    kwargs = mock.call_args.kwargs
                    self.assertTrue(kwargs == {"host": self.environment["MYSQL_HOST"], "user": self.environment["MYSQL_USER"], "password": self.environment["MYSQL_PASSWORD"], "database": self.environment["MYSQL_DATABASE"]}, "MySQL configuration must come from the environment")

    def test_missing_mysql_password_never_attempts_connection(self):
        with patch.dict(os.environ, self.environment):
            os.environ.pop("MYSQL_PASSWORD")
            import config.database as database
            auth = load_auth()
            for connect in [database.create_connection, auth.get_db_connection]:
                with patch("mysql.connector.connect") as mock:
                    with self.assertRaises(KeyError):
                        connect()
                    mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
