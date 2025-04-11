# temporal-debugging-workflows
This repository simulates various failures in Temporal for the purpose of learning basic Workflow debugging.

## Install
Requires [Poetry](https://python-poetry.org/) to manage dependencies.

1. `python -m venv venv`

2. `source venv/bin/activate`

3. `poetry install`


## Start Worker
```bash
$ poetry run python worker.py
```

## Run Workflows
### Happy Path
```bash
$ poetry run python starter.py HappyPath
```

### API Failure
```bash
$ poetry run python starter.py APIFailure
```

### NonRecoverable Failure
```bash
$ poetry run python starter.py NonRecoverableFailure
```

### Recoverable Failure
```bash
$ poetry run python starter.py RecoverableFailure
```
