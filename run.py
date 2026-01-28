from llmgrader.app import create_app

import os
import argparse

# Default parameters
scratch_dir = os.path.join(os.getcwd(), "scratch")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--local_repo", type=str, default=None,
                        help="Local repository path for questions (if testing locally)")
    args = parser.parse_args()
    local_repo = args.local_repo

    # Create the Flask app
    app = create_app(
        scratch_dir=scratch_dir,
        local_repo=local_repo
    )

    # Run locally only
    app.run(debug=True, use_reloader=False)

else:
    # Render imports this branch
    app = create_app(
        scratch_dir=scratch_dir
    )