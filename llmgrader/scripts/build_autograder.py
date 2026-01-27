import shutil
import zipfile
from pathlib import Path
import sys
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Build a Gradescope autograder zip file.'
    )
    parser.add_argument(
        '--schema',
        type=str,
        default=None,
        help='Path to the XML schema file (e.g., unit1_basic_logic.xml). If not specified, searches for an XML file in the current directory.'
    )
    args = parser.parse_args()

    # Current working directory (unitX/prob)
    cwd = Path.cwd()
    
    # Determine schema path
    if args.schema:
        schema_path = Path(args.schema)
        if not schema_path.is_absolute():
            schema_path = cwd / schema_path
        
        if not schema_path.exists():
            print(f"Error: Specified schema file not found: {schema_path}")
            sys.exit(1)
    else:
        # Find XML files in current directory
        xml_files = list(cwd.glob("*.xml"))
        
        if len(xml_files) == 0:
            print("Error: No XML files found in current directory.")
            print("Please specify a schema file with --schema option.")
            sys.exit(1)
        elif len(xml_files) > 1:
            print("Error: Multiple XML files found in current directory:")
            for f in xml_files:
                print(f"  - {f.name}")
            print("Please specify which one to use with --schema option.")
            sys.exit(1)
        
        schema_path = xml_files[0]
        print(f"Using schema file: {schema_path.name}")

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