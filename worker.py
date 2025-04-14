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
            activities.Activity4,
            # uncomment the line to resolve pending activities
            # activities.Activity5,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())