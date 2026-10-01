from datetime import datetime


# --------------------------------------------------
# DAYS LEFT FOR EXAM
# --------------------------------------------------

def calculate_days_left(exam_date):

    exam = datetime.strptime(
        exam_date,
        "%Y-%m-%d"
    )

    today = datetime.now()

    days_left = (
        exam.date() - today.date()
    ).days

    return max(days_left, 0)


# --------------------------------------------------
# PRIORITY SCORE
# --------------------------------------------------

def calculate_priority(days_left, weakness):

    score = 0

    # Weakness score
    if weakness.lower() == "high":
        score += 3

    elif weakness.lower() == "medium":
        score += 2

    else:
        score += 1


    # Exam urgency score
    if days_left <= 3:
        score += 4

    elif days_left <= 7:
        score += 3

    elif days_left <= 14:
        score += 2

    else:
        score += 1


    return score


# --------------------------------------------------
# PRIORITY LABEL
# --------------------------------------------------

def priority_label(score):

    if score >= 6:
        return "High"

    elif score >= 4:
        return "Medium"

    return "Low"


# --------------------------------------------------
# SPLIT TOPICS
# --------------------------------------------------

def split_topics(topics_text):

    if not topics_text:
        return []

    topics = []

    for topic in topics_text.split(","):

        cleaned = topic.strip()

        if cleaned:
            topics.append(cleaned)

    return topics