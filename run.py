from llmgrader.app import create_app

import os
import argparse

# Default parameters
scratch_dir = os.path.join(os.getcwd(), "scratch")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--soln_pkg", type=str, default=None,
                        help="Path to solution package (if testing locally)")
    args = parser.parse_args()
    soln_pkg = args.soln_pkg

    # Create the Flask app
    app = create_app(
        scratch_dir=scratch_dir,
        soln_pkg=soln_pkg
    )

    # Run locally only
    app.run(debug=True, use_reloader=False)

else:
    # Render imports this branch
    app = create_app(
        scratch_dir=scratch_dir
    )