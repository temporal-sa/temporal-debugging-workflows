import asyncio
import os
from myclient import get_client
import uuid
import sys

async def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    id = str(uuid.uuid4().int)[:6] 
    scenario=sys.argv[1]
    print(f"Scenario is {scenario}")

    client = await get_client()

    await client.execute_workflow(
        "Debug"+scenario,
        id=f'debug-{id}',
        task_queue=os.getenv("TEMPORAL_TASK_QUEUE"),
    )    


if __name__ == "__main__":
    asyncio.run(main())