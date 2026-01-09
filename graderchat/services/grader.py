from graderchat.services.parselatex import parse_latex_soln

class Grader:
    def grade(self, question, solution):
        return {
            "status": "correct",   # dummy
            "explanation": "This is a placeholder."
        }
    
    def load_solution_file(self, text):

        # Parse the latex solution file
        items = parse_latex_soln(text)

        quest_list = [item.get("question", "") for item in items]
        soln_list = [item.get("solution", "") for item in items]
        grading_notes_list = [item.get("grading", "") for item in items]
        resp = {
            "num_questions": len(items),
            "questions": quest_list,
            "solutions": soln_list,
            "grading_notes": grading_notes_list
        }
        print("Loaded solution file with %d items." % len(items))
    
    
        # You don’t need to return anything yet
        return resp
