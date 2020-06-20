import functools
import os

import yaml

from pydantic import BaseSettings, SecretStr


class ReposApp(BaseSettings):
    app_id: int
    key_path: str
    endpoint: str
    webhook_secret: SecretStr

    class Config:
        env_prefix = "REPOS_"

    def flask_config(self):
        return dict(
            GITHUBAPP_ID=self.app_id,
            GITHUBAPP_ROUTE=self.endpoint,
            GITHUBAPP_SECRET=self.webhook_secret.get_secret_value(),
            GITHUBAPP_KEY=open(self.key_path, "rb").read(),
        )


class Settings(BaseSettings):
    repos_app: ReposApp


@functools.lru_cache
def load_config():
    """Carga la configuración de un archivo YAML.

    Returns:
       un objeto de tipo Settings, validado.
    """
    conffile = os.environ.get("SISYPHUS_CONF", "sisyphus.yaml")
    with open(conffile) as yml:
        return Settings(**yaml.safe_load(yml))