from ayon_server.settings import (
    SettingsField,
    BaseSettingsModel,
)


class ListProfileSettings(BaseSettingsModel):
    list_folder_name: str = SettingsField(
        default="",
        label="List Folder Name",
        description="CURRENTLY NOT IMPLEMENTED! Name of the folder to place the list in. Can be used to group lists. E.g. 'Auto-Lists/Filter Name'",
    )
    product_names: list[str] = SettingsField(
        default_factory=list,
        label="Product name filter",
        description="List of product names to filter versions by. Only versions matching these product names will be included in the list.",
    )


class AutoListsSettings(BaseSettingsModel):
    """Settings for most standalone in-house tools"""
    enabled: bool = SettingsField(default=False, label="Enabled")
    list_settings: list[ListProfileSettings] = SettingsField(default=[])


DEFAULT_VALUES = {}
