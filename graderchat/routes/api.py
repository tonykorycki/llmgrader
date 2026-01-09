print("LOADING api.py FROM:", __file__)

from flask import Blueprint, request, jsonify
from flask import render_template



class APIController:
    def __init__(self, llm_client, grader):
        self.llm_client = llm_client
        self.grader = grader

    def register(self, app):
        bp = Blueprint("api", __name__)

        @bp.get("/")
        def home():
            return render_template("index.html")

        @bp.post("/chat")
        def chat():
            data = request.json
            msg = data.get("message", "")
            reply = self.llm_client.chat(msg)
            return jsonify({"reply": reply})

        @bp.post("/grade")
        def grade():
            data = request.json
            q = data.get("question", "")
            s = data.get("solution", "")
            result = self.grader.grade(q, s)
            return jsonify(result)
        
        @bp.post("/load_file")
        def load_file():
            file = request.files.get("file")
            if not file:
                return jsonify({"error": "No file uploaded"}), 400

            text = file.read().decode("utf-8")

            # Call your grader (which will print something)
            parsed = self.grader.load_solution_file(text)

            # For now, just return a simple response
            return jsonify(parsed)


        app.register_blueprint(bp)