from datetime import timedelta
from typing import Sequence, Any
from temporalio import workflow
from temporalio.common import RawValue
import asyncio
import time

with workflow.unsafe.imports_passed_through():
    from activities import DebugActivities

@workflow.defn(dynamic=True, sandboxed=False)
class DebugWorkflow:

    BUG = "DebugRecoverableFailure"
    NDE = "DebugNDE"
    PENDING_ACTIVITY = "DebugPendingActivity"
    DEADLOCK = "DebugDeadlock"
    TIMEOUT = "DebugTimeout"
    
    def __init__(self) -> None:
        self.retry_policy = DebugActivities.retry_policy

    @workflow.run
    async def run(self, args: Sequence[RawValue]) -> Any:      
        workflow_type = workflow.info().workflow_type
        workflow.logger.info(f"Dynamic workflow started, type = {workflow_type}")

        if self.NDE == workflow_type:        
            await workflow.execute_activity(
                # Switch Activities during workflow run to cause NDE
                DebugActivities.Activity1,
                # DebugActivities.Activity3,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=self.retry_policy                 
            )

            await asyncio.sleep(30)
            
        elif self.PENDING_ACTIVITY == workflow_type:
            await workflow.execute_activity(
                DebugActivities.Activity5,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=self.retry_policy
            )

        elif self.TIMEOUT == workflow_type:
            await workflow.execute_activity(
                DebugActivities.Activity6,
                # change to fix
                # the next line is too short of a timeout
                # so comment this out to fix and uncomment
                # out the following line
                start_to_close_timeout=timedelta(seconds=2),
                # use this to fix the error
                # start_to_close_timeout=timedelta(seconds=60),
                retry_policy=self.retry_policy
            )

        else:
            await workflow.execute_activity(
                DebugActivities.Activity1,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=self.retry_policy             
            )

            await workflow.execute_activity(
                DebugActivities.Activity2,
                workflow_type,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=self.retry_policy                
            )

            await workflow.execute_activity(
                DebugActivities.Activity3,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=self.retry_policy                 
            )

            if self.DEADLOCK == workflow_type:
                # Simulate deadlock
                # Deadlock detector will by default fail workflow task if anything blocks more than 2 seconds.
                time.sleep(5)
                pass

            if self.BUG == workflow_type:
                # Simulate bug
                raise RuntimeError("Simulated bug - fix me!")
                pass

            await workflow.execute_activity(
                DebugActivities.Activity4,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=self.retry_policy                 
            )