# Mathodian Architecture Overview

## 1. High-Level Structure

- **Frontend**: Single Page Application (SPA) using HTML, CSS, and JS (vanilla or with a minimal framework if needed).
- **Backend**: Python Flask app exposing a REST API for mathematical operations.
- **Math Operations**: Each operation is a separate Python module, auto-discovered and registered at startup.
- **Input Models**: Parameter types (Scalar, Vector, Matrix, etc.) are modeled as classes for validation and serialization.

## 2. Directory Layout

```
/mathodian
  /api
    __init__.py
    operation_registry.py
    /operations
      __init__.py
      cubic_polynomial.py
      linear_system.py
      combinatorics.py
  /models
    __init__.py
    parameters.py
  /static
    /js
      main.js
    /css
      style.css
  /templates
    base.html
    index.html
    operation.html
  app.py
/docs
  architecture.md
```

## 3. Operation Registration

- Each operation is a class with metadata (name, description, input schema, etc.).
- Operations are auto-registered via a registry pattern using Python’s importlib and introspection.
- No `if/elif` chains for operation selection.

## 4. API

- `/api/operations`: List all available operations (for frontend menu).
- `/api/operations/<operation_id>`: Get operation metadata (input form schema).
- `/api/operations/<operation_id>/calculate`: POST endpoint to perform calculation.

## 5. Frontend

- Loads available operations via API.
- Renders dynamic forms based on operation input schema.
- Submits calculation requests via AJAX, displays results attractively.

## 6. Extensibility

- New operations = new Python files in `/api/operations/`.
- No core code changes required for new operations.

## 7. Input Parameter Modeling

- Parameter types: Scalar, Vector, Matrix, etc.
- Each operation declares its required parameters and types.
- Frontend renders appropriate input widgets.

## 8. Production Readiness

- Flask app is structured for easy adaptation to WSGI servers (gunicorn, uwsgi).
- Static assets separated for CDN or Nginx serving.
- Containerization-ready structure.