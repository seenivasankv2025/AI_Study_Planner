import sqlite3

DB_NAME = "planner.db"


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():
    return sqlite3.connect(DB_NAME)


# --------------------------------------------------
# CREATE / UPDATE DATABASE
# --------------------------------------------------

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    # SUBJECTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            weakness TEXT NOT NULL,
            topics TEXT DEFAULT ''
        )
    """)

    # --------------------------------------------------
    # Migration support:
    # If old subjects table does not have "topics",
    # automatically add it.
    # --------------------------------------------------

    cursor.execute("PRAGMA table_info(subjects)")
    columns = [column[1] for column in cursor.fetchall()]

    if "topics" not in columns:
        cursor.execute("""
            ALTER TABLE subjects
            ADD COLUMN topics TEXT DEFAULT ''
        """)

    # TASKS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            task TEXT NOT NULL,
            study_date TEXT NOT NULL,
            duration REAL NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# ADD SUBJECT
# --------------------------------------------------

def add_subject(subject_name, exam_date, weakness, topics):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subjects (
            subject_name,
            exam_date,
            weakness,
            topics
        )
        VALUES (?, ?, ?, ?)
    """, (
        subject_name,
        exam_date,
        weakness,
        topics
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------
# GET ALL SUBJECTS
# --------------------------------------------------

def get_subjects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            subject_name,
            exam_date,
            weakness,
            topics
        FROM subjects
        ORDER BY exam_date ASC
    """)

    subjects = cursor.fetchall()

    conn.close()

    return subjects


# --------------------------------------------------
# DELETE SUBJECT
# --------------------------------------------------

def delete_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM subjects
        WHERE id = ?
    """, (subject_id,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# ADD TASK
# --------------------------------------------------

def add_task(subject, task, study_date, duration):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (
            subject,
            task,
            study_date,
            duration,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        subject,
        task,
        study_date,
        duration,
        "Pending"
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------
# GET ALL TASKS
# --------------------------------------------------

def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            subject,
            task,
            study_date,
            duration,
            status
        FROM tasks
        ORDER BY study_date ASC, id ASC
    """)

    tasks = cursor.fetchall()

    conn.close()

    return tasks


# --------------------------------------------------
# GET TODAY'S TASKS
# --------------------------------------------------

def get_today_tasks(today):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            subject,
            task,
            study_date,
            duration,
            status
        FROM tasks
        WHERE study_date = ?
        ORDER BY id ASC
    """, (today,))

    tasks = cursor.fetchall()

    conn.close()

    return tasks


# --------------------------------------------------
# COMPLETE TASK
# --------------------------------------------------

def mark_task_completed(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# MARK PENDING
# --------------------------------------------------

def mark_task_pending(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = 'Pending'
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# DELETE TASK
# --------------------------------------------------

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# DELETE TODAY'S PENDING GENERATED PLAN
# --------------------------------------------------

def delete_today_generated_tasks(study_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE study_date = ?
        AND status = 'Pending'
    """, (study_date,))

    conn.commit()
    conn.close()


# --------------------------------------------------
# PROGRESS
# --------------------------------------------------

def calculate_progress():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
    """)

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'Completed'
    """)

    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return round(
        (completed / total) * 100,
        2
    )


# --------------------------------------------------
# TOTAL TASKS
# --------------------------------------------------

def get_total_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# --------------------------------------------------
# COMPLETED TASK COUNT
# --------------------------------------------------

def get_completed_tasks_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'Completed'
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


# --------------------------------------------------
# PENDING TASK COUNT
# --------------------------------------------------

def get_pending_tasks_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'Pending'
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count