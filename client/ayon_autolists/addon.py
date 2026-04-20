from pathlib import Path

from ayon_core.addon import AYONAddon, IPluginPaths

from .version import __version__


ADDON_ROOT: Path = Path(__file__).parent
ADDON_NAME: str = "autolists"
ADDON_LABEL: str = "Auto Lists"
ADDON_VERSION: str = __version__


class AutoListsAddon(AYONAddon, IPluginPaths):
    name: str = ADDON_NAME
    label: str = ADDON_LABEL
    version: str = __version__
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def initialize(self, settings):
        """Initialization of module."""
        self.enabled = True
        self.settings = settings

    def get_plugin_paths(self):
        return {
            "publish": (ADDON_ROOT / "plugins" / "publish").as_posix(),
        }

    def get_launch_hook_paths(self, app):
        return [str(ADDON_ROOT / "hooks")]

    # ITrayAddon
    def tray_init(self):
        """Tray init."""
        pass

    def tray_start(self):
        """Tray start."""
        pass

    def tray_exit(self):
        """Tray exit."""
        return
