from ayon_server.settings import (
    SettingsField,
    BaseSettingsModel,
)


class ListProfileSettings(BaseSettingsModel):
    name: str = SettingsField(default="", label="List Name")    
    schedule: str = SettingsField(
        default="daily",
        label="Schedule",
        enum_resolver=lambda: ["daily", "weekly"],
    )
    product_names: list[str] = SettingsField(
        default_factory=list,
        title="Product name filter",
    )


class AutoListsSettings(BaseSettingsModel):
    """Settings for most standalone in-house tools"""
    enabled: bool = SettingsField(default=False, label="Enabled")
    list_settings: list[ListProfileSettings] = SettingsField(default=[])


DEFAULT_VALUES = {}
