import sys
import logging
from time import sleep
import ayon_api
from socket import gethostname

from datetime import datetime, timedelta


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger(__name__)


def handle_new_version_event(version, project, addon_settings):
    # get added version
    version["entityId"] = version["id"] # ayon_api wants entityId for adding a version to an entity list, but get_version_by_id returns id, so i copy it over
    version["product"] = ayon_api.get_product_by_id(project["name"], version["productId"])


    # if not matching filters skip and mark event as finished
    profiles_to_use = []
    for idx, profile in enumerate(addon_settings["list_settings"]):
        log.info(f"{profile = }")
        # iterate productNames and glob against version name
        for product_name_filter in profile["product_names"]:
            if version["product"]["name"] == product_name_filter:
                profiles_to_use.append(addon_settings["list_settings"][idx])
    if not profiles_to_use:
        log.info("No matching profile found for version. Skipping.")
        return

    # get event_time
    for profile_to_use in profiles_to_use:
        log.info(f"Processing profile: {profile_to_use}")
        version_created_at = datetime.fromisoformat(version["createdAt"])
        date_created = version_created_at.date()
        if version_created_at.hour >= profile_to_use["cutoff_hour"]:  # if after cutoff hour consider next day
            date_created = (version_created_at + timedelta(days=1)).date()
        if profile_to_use["combine_weekend"] and date_created.weekday() >= 5:  # if weekend consider next monday
            date_created += timedelta(days=(7 - date_created.weekday()))

        # format playlist name from settings template
        # place playlist in folder Auto-Lists/Filter Name
        list_folder_name = profile_to_use["list_folder_name"]
        list_name = f"{date_created} - {profile_to_use['name']}"

        # ensure event_playlist is present
        entity_list = None
        for existing_list in ayon_api.get_entity_lists(project["name"]):
            if existing_list["label"] == list_name:
                entity_list = existing_list
                break
        if not entity_list:
            entity_list = ayon_api.create_entity_list(project["name"], "version", label=list_name)

        # add versions to playlist
        if isinstance(entity_list, str):
            entity_list_id = entity_list
        else:
            entity_list_id = entity_list["id"]

        # i don't know why i can't use the ayon_api function.
        # after item was added to 1 list it'll be removed afterwards
        # the "normal" post works fine
        # ayon_api.update_entity_list_items(project["name"], entity_list_id, [version], mode="merge")
        ayon_api.post(
            f"/projects/{project['name']}/lists/{entity_list_id}/items",
            entityId=version["entityId"],
        )
        log.info(f"Added version '{version['id']}' to list '{list_name}' (ID: {entity_list_id}).")


class AutoListsProcessor:
    def __init__(self):
        ayon_api.init_service()
        self.svc_name = ayon_api.get_service_name()

    def start_processing(self):
        log.info("Starting AutoLists Processor...")
        log.debug("ayon_api module: %s", ayon_api)

        while True:
            target_event = ayon_api.enroll_event_job(
                source_topic="entity.version.created",  # maybe rather reviewable.created
                target_topic="autolists.process",
                description="Process new version for autolists",
                sender=gethostname(),
            )
            if not target_event:
                log.warning("Failed to enroll event job. Retrying in 5 seconds...")
                sleep(5)
                continue

            target_event = ayon_api.get_event(target_event["id"])
            source_event = ayon_api.get_event(target_event["dependsOn"])

            project = ayon_api.get_project(source_event["project"])
            if not project:
                errmsg = f"Project '{source_event['project']}' not found."
                raise RuntimeError(errmsg)
            ayon_api.update_event(
                target_event["id"],
                project_name=project["name"],
            )

            self.settings = ayon_api.get_service_addon_settings(project["name"])
            if not self.settings["enabled"]:
                log.info("Service is disabled in settings. Marking event as finished and skipping.")
                ayon_api.update_event(
                    target_event["id"],
                    description="Service is disabled in settings. Skipping.",
                    status="finished",
                )
                continue

            version = ayon_api.get_version_by_id(
                project["name"],
                source_event["summary"]["entityId"],
                fields=["taskId", "createdAt", "productId"],
            )
            if not version:
                errmsg = f"Version with ID '{source_event['summary']['entityId']}' not found in project '{project['name']}'."
                raise RuntimeError(errmsg)
            log.info(f"{version = }")
            # 2026-04-22 10:56:22,533 INFO [__main__] version = {'data': {}, 'tags': [], 'productId': 'e32465643e3911f1a0f716cc399bfb9b', 'status': 'Pending review', 'createdAt': '2026-04-22T12:56:17.0026-04-22T12:56:17.336462+02:00', 'allAttrib': '{}', 'id': 'e32a8fb63e3911f1a0f716cc399bfb9b', 'attrib': {}}

            try:
                # self.settings = {'enabled': True, 'list_settings': [{'name': 'playlist_parent_folder_name', 'schedule': 'daily', 'filter_profile': {'variants': ['Main'], 'task_types': ['Comp']}}]}
                log.info("Loaded service settings.")
                log.info(f"{target_event = }")
                log.info(f"{source_event = }")
                log.info(f"{self.settings = }")
                handle_new_version_event(
                    version,
                    project,
                    self.settings,
                )
            except Exception as e:
                log.exception("Error processing event: %s", e)
                ayon_api.update_event(
                    target_event["id"],
                    description=f"{e}",
                    status="failed",
                )
            else:
                log.info("Event processed successfully.")
                success_msg = "Event processed successfully."
                ayon_api.update_event(
                    target_event["id"],
                    description=success_msg,
                    status="finished",
                )


if __name__ == "__main__":
    processor = AutoListsProcessor()
    sys.exit(processor.start_processing())
