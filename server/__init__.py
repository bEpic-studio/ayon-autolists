from typing import Type

from ayon_server.addons import BaseServerAddon

from .settings import AutoListsSettings, DEFAULT_VALUES


class ExampleAddon(BaseServerAddon):
    settings_model: Type[AutoListsSettings] = AutoListsSettings

    frontend_scopes: dict[str, dict[str, str]] = {"settings": {}}

    def initialize(self):
        pass

    async def get_default_settings(self):
        settings_model_cls = self.get_settings_model()
        return settings_model_cls(**DEFAULT_VALUES)

    async def setup(self):
        pass
