# Architecture Overview

LLM Grader is structured as a Python package with a Flask interface.

## Key Components

### Application Factory
llmgrader/app.py defines create_app(), which initializes the Flask app and registers blueprints.

### Routes
llmgrader/routes/ contains modular route handlers.

### Services
llmgrader/services/ will contain the OpenAI client, grading logic, and prompt builders.

### Templates and Static Files
llmgrader/templates/ contains Jinja2 templates.
llmgrader/static/ contains CSS and JavaScript assets.
