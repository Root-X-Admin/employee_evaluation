from flask import render_template, request
from models import db, Evaluation

def evaluate_employee(attendance, tasks, teamwork, deadlines):
    # Fuzzy Logic Scoring
    attendance_score = attendance / 100
    tasks_score = tasks / 100
    teamwork_score = teamwork / 10
    deadlines_score = deadlines / 100

    final_score = (attendance_score + tasks_score + teamwork_score + deadlines_score) / 4

    # Evaluation based on fuzzy ranges
    if final_score >= 0.85:
        result = "Excellent"
    elif final_score >= 0.7:
        result = "Good"
    elif final_score >= 0.5:
        result = "Average"
    else:
        result = "Needs Improvement"

    # Explainable Reasoning
    explanation = f"""Because:
    - Attendance was {attendance}%.
    - Tasks completion was {tasks}%.
    - Teamwork was {teamwork}/10.
    - Deadlines met was {deadlines}%.
    Final Score: {final_score:.2f}
    The system evaluated: {result}."""

    # Auto Suggestion Logic
    factors = {
        "Attendance": attendance_score,
        "Tasks Completion": tasks_score,
        "Teamwork": teamwork_score,
        "Deadlines Met": deadlines_score
    }
    weakest = min(factors, key=factors.get)
    suggestion = f"Suggested Focus: Improve {weakest} for better performance."

    return result, explanation, suggestion

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/evaluate', methods=['POST'])
    def evaluate():
        name = request.form['name']
        attendance = float(request.form['attendance'])
        tasks = float(request.form['tasks'])
        teamwork = float(request.form['teamwork'])
        deadlines = float(request.form['deadlines'])

        result, explanation, suggestion = evaluate_employee(attendance, tasks, teamwork, deadlines)

        new_eval = Evaluation(
            employee_name=name,
            attendance=attendance,
            tasks=tasks,
            teamwork=teamwork,
            deadlines=deadlines,
            result=result,
            explanation=explanation,
            suggestion=suggestion
        )
        db.session.add(new_eval)
        db.session.commit()

        return render_template('result.html', result=result, explanation=explanation, suggestion=suggestion, employee_name=name)

    @app.route('/history')
    def history():
        evaluations = Evaluation.query.order_by(Evaluation.timestamp.desc()).all()
        return render_template('history.html', evaluations=evaluations)
