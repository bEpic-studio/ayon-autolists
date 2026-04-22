name = "autolists"
title = "Auto Lists"
version = "0.0.1-dev"

services = {
    "AutoListsProcessor": {"image": f"bepic/ayon-autolists-processor:{version}"},
}

plugin_for = ["ayon_server"]
build_command = ""
