from flask import Flask
from llmgrader.routes.api import APIController
from llmgrader.services.grader import Grader
import secrets

def create_app(
        scratch_dir : str ="scratch",
        soln_pkg : str | None = None) -> Flask:
    """
    Creates and configures the Flask application.
    
    Parameters
    ----------
    scratch_dir: str
        Path to the scratch directory for temporary files.
    soln_pkg: str | None
        Path to solution package (if testing locally).
    """
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    grader = Grader(
        scratch_dir=scratch_dir,
        soln_pkg=soln_pkg)
    controller = APIController(grader)
    controller.register(app)

    return app