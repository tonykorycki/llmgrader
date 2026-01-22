import shutil
import zipfile
from pathlib import Path
import sys

def main():
    # Current working directory (unitX/prob)
    cwd = Path.cwd()
    schema_path = cwd / "grade_schema.xml"

    if not schema_path.exists():
        print("Error: grade_schema.xml not found in current directory.")
        sys.exit(1)

    # Locate the template directory inside the llmgrader package
    try:
        import llmgrader
    except ImportError:
        print("Error: llmgrader package not found. Is it installed?")
        sys.exit(1)

    template_dir = Path(llmgrader.__file__).parent / "gradescope"

    if not template_dir.exists():
        print(f"Error: Gradescope template directory not found at {template_dir}")
        sys.exit(1)

    # Create autograder/ folder in the current directory
    out_dir = cwd / "autograder"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir()

    # Copy template files
    template_files = ["autograde.py", "run_autograder", "requirements.txt", "setup.sh"]
    for fname in template_files:
        src = template_dir / fname
        dst = out_dir / fname
        if not src.exists():
            print(f"Error: required template file missing: {src}")
            sys.exit(1)

        shutil.copy(src, dst)

    # Ensure run_autograder is executable inside the zip
    run_file = out_dir / "run_autograder"
    if run_file.exists():
        run_file.chmod(0o755)


    # Copy the local grade schema
    shutil.copy(schema_path, out_dir / "grade_schema.xml")

    # Create autograder.zip
    zip_path = cwd / "autograder.zip"
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for path in out_dir.rglob("*"):
            # Write paths relative to autograder_dir so they appear at ZIP root
            z.write(path, path.relative_to(out_dir))

    print(f"Created autograder.zip in {cwd}")