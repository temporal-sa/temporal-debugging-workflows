import asyncio
from temporalio.worker import Worker
import os

from activities import DebugActivities

from myclient import get_worker_client
from workflow import DebugWorkflow


async def main():
    client = await get_worker_client()

    activities = DebugActivities()

    worker = Worker(
        client,
        task_queue=os.getenv("TEMPORAL_TASK_QUEUE"),
        workflows=[DebugWorkflow],
        activities=[
            activities.Activity1,
            activities.Activity2,
            activities.Activity3,
            activities.FailingActivity,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())