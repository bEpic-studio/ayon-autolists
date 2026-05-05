from ayon_server.settings import (
    SettingsField,
    BaseSettingsModel,
)


class ListProfileSettings(BaseSettingsModel):
    name: str = SettingsField(
        default="",
        title="List Name",
        description="Name of the list to be created. Will be auto-appended with `{YYYY}-{MM}-{DD}_`.",
    )
    list_folder_name: str = SettingsField(
        default="",
        title="List Folder Name",
        description="Currently not implemented as it depends on ayon-powerpack. Name of the folder to place the list in. Can be used to group lists, e.g. 'Auto-Lists/Filter Name'.",
        disabled=True,
    )
    product_names: list[str] = SettingsField(
        default_factory=list,
        label="Product name filter",
        description="List of product names to filter versions by. Only versions matching these product names will be included in the list.",
    )
    cutoff_hour: int = SettingsField(
        default=20,
        label="Cutoff Hour",
        description="Hour of the day (0-23) to use as cutoff for determining the date in the list name. Versions created after this hour will be considered as created on the next day.",
    )
    combine_weekend: bool = SettingsField(
        default=True,
        label="Combine Weekend",
        description="Whether to combine versions created on weekends. If false, versions created on Saturday or Sunday will be considered as created on the following Monday.",
    )


class AutoListsSettings(BaseSettingsModel):
    """Settings for most standalone in-house tools"""

    enabled: bool = SettingsField(default=False, label="Enabled")
    list_settings: list[ListProfileSettings] = SettingsField(default=[])


DEFAULT_VALUES = {}
