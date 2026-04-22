import sys
import logging
from time import sleep
import ayon_api
from socket import gethostname


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def handle_new_version_event(event, addon_settings):
    # get added version
    # if not matching filters skip and mark event as finished
    # for list_filter in addon_settings["filters"]:
    #     print(f"Applying filter: {list_filter}")

    # get event_time
    # if after 8pm consider next day
    # how to do settings for that?

    # format playlist name from settings template

    # ensure event_playlist is present
    # place playlist in folder Auto-Lists/Filter Name

    # add versions to playlist


    logger.info("Handling new version event: %s", event)
    # Simulate processing time
    sleep(2)
    logger.info("Finished processing new version event.")

class AutoListsProcessor:
    def __init__(self):
        ayon_api.init_service()
        self.svc_name = ayon_api.get_service_name()

    def start_processing(self):
        logger.info("Starting AutoLists Processor...")
        logger.debug("ayon_api module: %s", ayon_api)

        while True:
            target_event = ayon_api.enroll_event_job(
                source_topic="entity.version.created",  # maybe rather reviewable.created
                target_topic="autolists.process",
                description="Process new version for autolists",
                sender=gethostname()
            )
            if not target_event:
                logger.warning(
                    "Failed to enroll event job. Retrying in 5 seconds..."
                )
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

            try:
                self.settings = ayon_api.get_service_addon_settings()
                logger.info("Loaded service settings.")
                logger.debug("Service settings: %s", self.settings)
                logger.info(f"{target_event = }")
                logger.info(f"{source_event = }")
                handle_new_version_event(target_event, self.settings)
            except Exception as e:
                logger.exception("Error processing event: %s", e)
                ayon_api.update_event(
                    target_event["id"],
                    description=f"{e}",
                    status="failed",
                )
            else:
                logger.info("Event processed successfully.")
                success_msg = "Event processed successfully."
                ayon_api.update_event(
                    target_event["id"],
                    description=success_msg,
                    status="finished",
                )


if __name__ == "__main__":
    processor = AutoListsProcessor()
    sys.exit(processor.start_processing())
