from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from datetime import datetime

from agent import generate_study_plan

from tools import (
    calculate_days_left,
    calculate_priority,
    priority_label
)

from database import (
    create_database,

    add_subject,
    get_subjects,
    delete_subject,

    add_task,
    get_tasks,
    get_today_tasks,
    mark_task_completed,
    mark_task_pending,
    delete_task,
    delete_today_generated_tasks,

    calculate_progress,
    get_total_tasks,
    get_completed_tasks_count,
    get_pending_tasks_count
)


app = Flask(__name__)


# --------------------------------------------------
# CREATE DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    subjects = get_subjects()

    subject_details = []


    # --------------------------------------------------
    # SUBJECT PRIORITY ANALYSIS
    # --------------------------------------------------

    for subject in subjects:

        subject_id = subject[0]
        subject_name = subject[1]
        exam_date = subject[2]
        weakness = subject[3]
        topics = subject[4]

        days_left = calculate_days_left(
            exam_date
        )

        priority_score = calculate_priority(
            days_left,
            weakness
        )

        priority = priority_label(
            priority_score
        )


        subject_details.append({

            "id":
                subject_id,

            "name":
                subject_name,

            "exam_date":
                exam_date,

            "weakness":
                weakness,

            "topics":
                topics,

            "days_left":
                days_left,

            "priority_score":
                priority_score,

            "priority":
                priority

        })


    tasks = get_tasks()

    today_tasks = get_today_tasks(
        today
    )

    progress = calculate_progress()

    total_tasks = get_total_tasks()

    completed_tasks = (
        get_completed_tasks_count()
    )

    pending_tasks = (
        get_pending_tasks_count()
    )


    return render_template(

        "index.html",

        subjects=subjects,

        subject_details=subject_details,

        tasks=tasks,

        today_tasks=today_tasks,

        progress=progress,

        total_tasks=total_tasks,

        completed_tasks=completed_tasks,

        pending_tasks=pending_tasks,

        today=today
    )


# --------------------------------------------------
# ADD MULTIPLE SUBJECTS
# --------------------------------------------------

@app.route(
    "/add-subjects",
    methods=["POST"]
)
def add_subjects():

    subject_names = request.form.getlist(
        "subject[]"
    )

    exam_dates = request.form.getlist(
        "exam_date[]"
    )

    weakness_levels = request.form.getlist(
        "weakness[]"
    )

    topics_list = request.form.getlist(
        "topics[]"
    )


    for i in range(
        len(subject_names)
    ):

        subject_name = (
            subject_names[i].strip()
        )

        if subject_name == "":
            continue


        exam_date = exam_dates[i]

        weakness = weakness_levels[i]

        topics = topics_list[i].strip()


        add_subject(
            subject_name,
            exam_date,
            weakness,
            topics
        )


    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# DELETE SUBJECT
# --------------------------------------------------

@app.route(
    "/delete-subject/<int:subject_id>"
)
def remove_subject(subject_id):

    delete_subject(
        subject_id
    )

    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# GENERATE STUDY PLAN
# --------------------------------------------------

@app.route(
    "/generate-plan",
    methods=["POST"]
)
def generate_plan():

    available_hours = float(
        request.form[
            "available_hours"
        ]
    )


    subjects = get_subjects()


    if not subjects:

        return redirect(
            url_for("home")
        )


    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    # Remove previous pending generated plan
    # but keep completed tasks
    delete_today_generated_tasks(
        today
    )


    # --------------------------------------------------
    # CALL AGENT
    # --------------------------------------------------

    study_plan = generate_study_plan(
        subjects,
        available_hours
    )


    # --------------------------------------------------
    # SAVE AGENT PLAN
    # --------------------------------------------------

    for item in study_plan:

        add_task(
            item["subject"],
            item["task"],
            today,
            item["duration"]
        )


    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# ADD TASK MANUALLY
# --------------------------------------------------

@app.route(
    "/add-task",
    methods=["POST"]
)
def add_new_task():

    subject = request.form[
        "subject"
    ]

    task = request.form[
        "task"
    ]

    study_date = request.form[
        "study_date"
    ]

    duration = float(
        request.form[
            "duration"
        ]
    )


    add_task(
        subject,
        task,
        study_date,
        duration
    )


    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# COMPLETE TASK
# --------------------------------------------------

@app.route(
    "/complete/<int:task_id>"
)
def complete_task(task_id):

    mark_task_completed(
        task_id
    )

    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# MARK TASK PENDING
# --------------------------------------------------

@app.route(
    "/pending/<int:task_id>"
)
def pending_task(task_id):

    mark_task_pending(
        task_id
    )

    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# DELETE TASK
# --------------------------------------------------

@app.route(
    "/delete/<int:task_id>"
)
def remove_task(task_id):

    delete_task(
        task_id
    )

    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# RUN FLASK
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )