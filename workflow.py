from datetime import timedelta
from typing import Sequence, Any
from temporalio import workflow
from temporalio.common import RawValue

with workflow.unsafe.imports_passed_through():
    from activities import DebugActivities

@workflow.defn(dynamic=True)
class DebugWorkflow:

    BUG = "DebugRecoverableFailure"
    
    def __init__(self) -> None:
        self.retry_policy = DebugActivities.retry_policy

    @workflow.run
    async def run(self, args: Sequence[RawValue]) -> Any:      
        workflow_type = workflow.info().workflow_type
        workflow.logger.info(f"Dynamic workflow started, type = {workflow_type}")

        await workflow.execute_activity(
            DebugActivities.Activity1,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=self.retry_policy             
        )

        await workflow.execute_activity(
            DebugActivities.Activity2,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=self.retry_policy                
        )

        await workflow.execute_activity(
            DebugActivities.FailingActivity,
            workflow_type,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=self.retry_policy                 
        )

        if self.BUG == workflow_type:
            # Simulate bug
            raise RuntimeError("Simulated bug - fix me!")
            pass

        await workflow.execute_activity(
            DebugActivities.Activity3,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=self.retry_policy                 
        )