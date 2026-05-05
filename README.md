# ayon-autolists

An AYON service addon that listens to newly created version events to automatically create new entity lists from.

## Setup
- get the zip archive or build your own
- install the addon to your AYON instance
- run the ash service
    - image is provided via DockerHub and will be downloaded if not built locally
- initialize the addon settings
    - this addon defaults to being disabled
    - either enable globally or only specific projects via AYON's "Project Settings"
