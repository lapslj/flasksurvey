from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension #bring in DTE
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret" #define something

debug = DebugToolbarExtension(app) #define debug fn
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False #turns off debugging intercepts

RESPONSES=[]

@app.route('/',methods=["GET"])
def homepage():
    """Homepage."""
    survey_title=satisfaction_survey.title
    survey_instructions=satisfaction_survey.instructions
    return render_template("homepage.html",title=survey_title,content=survey_instructions)

@app.route("/newsurvey",methods=["POST"])
def new_survey():
    """Clear session and start new survey"""
    RESPONSES.clear()
    session["responses"] = []
    return redirect("/questions/0")

@app.route('/questions/<int:num>', methods=["GET"])
def questions(num):
    """Questions pages."""
    #Check to make sure we're at the right number
    qnext = len(RESPONSES)
    survey_length = len(satisfaction_survey.questions)

        
    if num != qnext:
        flash("Invalid URL entered")
        if survey_length == qnext:
            return redirect("/complete")
        else:
            return redirect(f"/questions/{qnext}")
    else:
        question_header=f"Question {num + 1}"
        question_text=satisfaction_survey.questions[num].question
        choices=satisfaction_survey.questions[num].choices
        return render_template("questions.html",title=question_header,question_text=question_text,choices=choices)

@app.route("/answer", methods=["POST"])
def new_answer():
    """Add response to the list."""
    resp = request.form["response"]
    RESPONSES.append(resp)
    session["responses"] = RESPONSES
    #check and see if length of responses = length of survey
    print(RESPONSES)
    survey_length = len(satisfaction_survey.questions)
    qnext = len(RESPONSES)
    if survey_length == qnext:
        return redirect("/complete")
    else:
        return redirect(f"/questions/{qnext}")

@app.route("/complete")
def complete():
    """Send to survey-complete page."""
    return render_template("/complete.html",title="Thank you!")

@app.before_request
def print_responses():
    """For every single request that comes in, print out responses so far (prints to terminal)"""
    print("*********RESPONSES SO FAR************")
    print(RESPONSES)
    print("*********************")
