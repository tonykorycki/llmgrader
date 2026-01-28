from flask import Flask
from llmgrader.routes.api import APIController
from llmgrader.services.grader import Grader

def create_app(
        scratch_dir : str ="scratch",
        local_repo : str | None = None) -> Flask:
    """
    Creates and configures the Flask application.
    
    Parameters
    ----------
    scratch_dir: str
        Path to the scratch directory for temporary files.
    local_repo: str | None
        Local repository path for questions (if testing locally).
    """
    app = Flask(__name__)

    grader = Grader(
        scratch_dir=scratch_dir,
        local_repo=local_repo)
    controller = APIController(grader)
    controller.register(app)

    return app