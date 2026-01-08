# GraderChat

GraderChat is a lightweight Flask-based chatbot designed to help with autograding engineering problems using large language models. 
The project is just me playing around for now.  So don't take anything too serious.  It is more for my own education.

## Project Status

The current version includes:

- A Python package structure (graderchat/)
- A minimal Flask application factory
- Basic routing and template scaffolding
- Initial documentation structure for GitHub Pages

I am going to add new features.

- Chat interface for interacting with an LLM
- Autograding pipeline using reference solutions and grading notes
- OpenAI integration
- Front-end UI for question selection, chat history, and grading feedback

## Goals

The long-term goal of GraderChat is to provide:

- A clean, extensible Flask interface for student interaction
- A modular grading backend powered by LLMs
- A reproducible research platform for studying LLM-based grading
- A Python package that can be imported into other tools or notebooks

## Installation (Development Mode)

Clone the repository and install in editable mode:

```bash
pip install -e .
```

Run the development server:

```
python run.py
```

Then open:
```
http://127.0.0.1:5000/
```
## Documentation

Documentation is being built in the `docs/ ` folder and will be published via GitHub Pages.

More details will be added as the project evolves.