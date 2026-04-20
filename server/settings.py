from ayon_server.settings import (
    SettingsField,
    BaseSettingsModel,
    task_types_enum
)

"""
- enabled
- ListSettings (list of settings for each list)
    - name (shall allow anatomy keys)
    - schedule: Daily/Weekly
    - Filter Profile:
        - product name (shall accept regex)
        - product type
        - statuses
        - folder path (shall accept regex) (maybe multiple paths?)
        - task type?
"""

# TODO: implement product types enum


class FilterProfileSettings(BaseSettingsModel):
    product_name: str = SettingsField(
        default="",
        title="Product name filter"
    )
    product_type: str = SettingsField(
        default="",
        title="Product type filter",
        # enum_resolver=task_types_enum
    )
    statuses: list[str] = SettingsField(
        default_factory=list,
        title="Statuses filter",
        enum_resolver=task_types_enum
    )
    folder_path: str = SettingsField(
        default="",
        title="Folder path filter"
    )
    task_types: list[str] = SettingsField(
        default_factory=list,
        title="Task types filter",
        enum_resolver=task_types_enum
    )


class ListProfileSettings(BaseSettingsModel):
    name: str = SettingsField(default="", label="List Name")    
    schedule: str = SettingsField(
        default="daily",
        label="Schedule",
        enum_resolver=lambda: ["daily", "weekly"],
    )
    filter_profile: FilterProfileSettings = SettingsField(
        default_factory=FilterProfileSettings,
        label="Filter Profile",
    )


class AutoListsSettings(BaseSettingsModel):
    """Settings for most standalone in-house tools"""
    enabled: bool = SettingsField(default=False, label="Enabled")
    list_settings: list[ListProfileSettings] = SettingsField(default=[])


DEFAULT_VALUES = {}
