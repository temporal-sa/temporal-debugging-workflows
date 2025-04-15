# temporal-debugging-workflows
This repository simulates various failures in Temporal for the purpose of learning basic Workflow debugging.

## Install
Requires [Poetry](https://python-poetry.org/) to manage dependencies.

1. `python -m venv venv`

2. `source venv/bin/activate`

3. `poetry install`


## Set Cloud Environment

Copy the setcloudenv.sh.example to setcloudenv.sh
```bash
cp setcloudenv.sh.example setcloudenv.sh
```

Edit setcloudenv.sh to match your Temporal Cloud account:

```bash
export TEMPORAL_HOST_URL=<namespace>.<accountId>.tmprl.cloud:7233
export TEMPORAL_NAMESPACE=<namespace>.<accountId>
export TEMPORAL_MTLS_TLS_CERT=/path/to/tls/cert.pem
export TEMPORAL_MTLS_TLS_KEY=/path/to/tls/client.key
export TEMPORAL_WORKER_METRICS_PORT=8888
export TEMPORAL_TASK_QUEUE=DebugTaskQueue
```

## Start Worker
In a new terminal window, set up the virtual environment:

```bash
./setvenv.sh
```

### Start the worker
```bash
$ ./startcloudworker.sh 
```

## Run Workflows
In a new terminal window, set up the virtual environment:

```bash
./setvenv.sh
```

### Happy Path
This scenario runs successfully without any issues

```bash
$ ./startcloudwf.sh HappyPath
```

### Misconfigured Task Queue
This scenario demonstrates what happens when the task queue for the worker has a typo. 
If you are running existing workers, stop them first.

```bash
$ ./startcloudwf.sh HappyPath
```

In another terminal, start the misconfigured worker:
```bash
$ ./startmisconfigcloudworker.sh HappyPath
```

Then kill this worker and start the regular one.
```bash
$ ./startcloudworker.sh
```

### Pending Activities
Shows what happens when an activity has not be registered.

```bash
$ /startcloudwf.sh PendingActivity
```

Once the workflow has started, kill the worker, open worker.py and uncomment Activity5
Restart the worker and the workflow will continue

### API Failure
This scenario purposefully causes an activity to retry, simulating that the API is down. It succeeds on the 5th attempt. 
```bash
$ /startcloudwf.sh APIFailure
```

### NonRecoverable Failure
This scenario fails the workflow due to a business reason. Sets the retryable to false.

```bash
$ /startcloudwf.sh NonRecoverableFailure
```

### Activity Timeouts 
This scenario fails to complete because the start_to_close timeout for an activity is
shorter than the time the activity completes.

```bash
$ /startcloudwf.sh Timeout
```

Stop the worker. 
Change start_to_close_timeout in workflow.py (> 5 seconds)
Start the worker.
Notice that the problem still is there. This is because Temporal Server is managing the timeouts.
Terminate the workflow.
Reset the workflow

### Recoverable Failure
Demonstrates a bug in the code that raises an exception. 

```bash
$ /startcloudwf.sh RecoverableFailure
```
Kill the worker.
Fix the code by commenting out line # 65 where the exception is raised
Restart the worker

### NDE Failure
Demonstrates a non-determinism error.

```bash
$ /startcloudwf.sh NDE
```

Once you start workflow CTRL-C worker and comment out/change Activity from Activity1 to Activity2. Upon starting worker you will observe NDE.

Reset Workflow to first workflow task.



### Potential Deadlock Detected
Shows what happens when a workflow task takes longer than 2 seconds

```bash
$ /startcloudwf.sh Deadlock
```

Stop the worker and comment out the sleep in the workflow.py (Line 67). 
Restart the worker and the workflow will continue
