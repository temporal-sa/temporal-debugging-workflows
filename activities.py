import asyncio
from temporalio import activity
from temporalio.exceptions import ApplicationError
import logging
from temporalio.common import RetryPolicy
from datetime import timedelta
logging.basicConfig(level=logging.INFO)

class DebugActivities:
    ERROR_CHARGE_API_UNAVAILABLE = "DebugAPIFailure"
    ERROR_INVALID_CREDIT_CARD = "DebugNonRecoverableFailure"
    retry_policy = RetryPolicy(initial_interval=timedelta(seconds=1), backoff_coefficient=2, maximum_interval=timedelta(seconds=30))

    async def simulate_external_operation(self, ms: int):
        try:
            await asyncio.sleep(ms / 1000)
        except InterruptedError as e:
            print(e.__traceback__)

    async def simulate_external_operation_charge(self, ms: int, type: str, attempt: int):
        await self.simulate_external_operation(ms / attempt)
        return type if attempt < 5 else "NoError"

    @activity.defn
    async def Activity1(self):
        activity.logger.info(f"activity 1")
        await self.simulate_external_operation(100)

    @activity.defn
    async def Activity2(self, workflow_type: str):
        activity.logger.info(f"OCR activity")
        attempt = activity.info().attempt

        # Simulate external API call
        error = await self.simulate_external_operation_charge(1000, workflow_type, attempt)
        activity.logger.info(f"Simulated call complete, type = {workflow_type}, error = {error}")
        match error:
            case DebugActivities.ERROR_CHARGE_API_UNAVAILABLE:
                # a transient error, which can be retried
                activity.logger.info(f"API unavailable, attempt = {attempt}")
                raise ApplicationError("activity failed, API unavailable")
            case DebugActivities.ERROR_INVALID_CREDIT_CARD:
                # a business error, which cannot be retried
                raise ApplicationError("activity failed, api unavailable", type="ApiError", non_retryable=True)
            case _:
                # pass through, no error
                pass

    @activity.defn
    async def Activity3(self):
        activity.logger.info(f"activity 2")
        await self.simulate_external_operation(100)

    @activity.defn
    async def Activity4(self):
        activity.logger.info(f"activity 3")
        await self.simulate_external_operation(100)

    @activity.defn
    async def Activity5(self):
        activity.logger.info(f"activity 5")
        await self.simulate_external_operation(100)