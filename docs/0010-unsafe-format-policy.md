# ADR 0010: Unsafe Format Policy

## Status
Accepted

## Context
Pickle (`.pkl`), `joblib`, and `PyTorch` (`.pt`) files are notoriously unsafe as they can execute arbitrary code upon unpickling. ONNX and SafeTensors are safer alternatives.

## Decision
1. **Warning**: Uploading `.pkl` or `.joblib` will flag the model with an `is_unsafe=True` flag in the DB.
2. **Execution Boundary**: Unsafe models MUST be executed within the Sandbox. If the Sandbox is unavailable (e.g. Docker is down in Prod), execution will be refused. (In local dev, the subprocess fallback will execute it, assuming the developer trusts their own files).
3. **Encouraged Formats**: The platform will explicitly encourage ONNX formats.

## Consequences
- Requires parsing file extensions during upload.
