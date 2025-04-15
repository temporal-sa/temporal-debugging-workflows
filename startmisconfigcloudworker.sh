#!/bin/bash
source ./setcloudenv.sh
# this purposefully changes the name of the task queue
export export TEMPORAL_TASK_QUEUE=DebugTaskQueue3
poetry run python worker.py