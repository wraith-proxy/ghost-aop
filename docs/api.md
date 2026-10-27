<a id="__init__"></a>

# \_\_init\_\_

<a id="aspects"></a>

# aspects

<a id="aspects.TransientError"></a>

## TransientError Objects

```python
class TransientError(Exception)
```

Retriable failure. Network blips, temporary unavailability, that sort of thing.

<a id="aspects.SchemaValidationError"></a>

## SchemaValidationError Objects

```python
class SchemaValidationError(Exception)
```

Output schema didn't match what we expected. Someone changed something.

<a id="aspects.log_execution"></a>

#### log\_execution

```python
@aspectlib.Aspect
def log_execution(*args, **kwargs)
```

Logs entry, exit, and elapsed time for any stage.execute() call.

<a id="aspects.retry"></a>

#### retry

```python
@aspectlib.Aspect
def retry(*args, **kwargs)
```

Retries on TransientError up to 3 times before giving up.

<a id="aspects.audit_trail"></a>

#### audit\_trail

```python
@aspectlib.Aspect
def audit_trail(*args, **kwargs)
```

Records input/output lineage after successful execution.

<a id="stages"></a>

# stages

<a id="stages.ExtractStage"></a>

## ExtractStage Objects

```python
class ExtractStage()
```

Validates and passes through the raw batch. In reality: fetch from source.

<a id="stages.TransformStage"></a>

## TransformStage Objects

```python
class TransformStage()
```

Applies business rules and produces a ProcessedBatch.

<a id="stages.LoadStage"></a>

## LoadStage Objects

```python
class LoadStage()
```

Writes to the sink. Here we just return the batch to keep things simple.

<a id="models"></a>

# models

<a id="main"></a>

# main

<a id="pipeline"></a>

# pipeline

<a id="pipeline.aspects"></a>

# pipeline.aspects

<a id="pipeline.aspects.TransientError"></a>

## TransientError Objects

```python
class TransientError(Exception)
```

Retriable failure. Network blips, temporary unavailability, that sort of thing.

<a id="pipeline.aspects.SchemaValidationError"></a>

## SchemaValidationError Objects

```python
class SchemaValidationError(Exception)
```

Output schema didn't match what we expected. Someone changed something.

<a id="pipeline.aspects.log_execution"></a>

#### log\_execution

```python
@aspectlib.Aspect
def log_execution(*args, **kwargs)
```

Logs entry, exit, and elapsed time for any stage.execute() call.

<a id="pipeline.aspects.retry"></a>

#### retry

```python
@aspectlib.Aspect
def retry(*args, **kwargs)
```

Retries on TransientError up to 3 times before giving up.

<a id="pipeline.aspects.audit_trail"></a>

#### audit\_trail

```python
@aspectlib.Aspect
def audit_trail(*args, **kwargs)
```

Records input/output lineage after successful execution.

<a id="pipeline.stages"></a>

# pipeline.stages

<a id="pipeline.stages.ExtractStage"></a>

## ExtractStage Objects

```python
class ExtractStage()
```

Validates and passes through the raw batch. In reality: fetch from source.

<a id="pipeline.stages.TransformStage"></a>

## TransformStage Objects

```python
class TransformStage()
```

Applies business rules and produces a ProcessedBatch.

<a id="pipeline.stages.LoadStage"></a>

## LoadStage Objects

```python
class LoadStage()
```

Writes to the sink. Here we just return the batch to keep things simple.

<a id="pipeline.models"></a>

# pipeline.models
