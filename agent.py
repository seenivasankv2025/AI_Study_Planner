from tools import (
    calculate_days_left,
    calculate_priority,
    priority_label,
    split_topics
)


# --------------------------------------------------
# STUDY PLANNER AGENT
# --------------------------------------------------

def generate_study_plan(subjects, available_hours):

    if not subjects:
        return []

    analyzed_subjects = []

    total_priority = 0


    # --------------------------------------------------
    # ANALYZE SUBJECTS
    # --------------------------------------------------

    for subject in subjects:

        subject_name = subject[1]
        exam_date = subject[2]
        weakness = subject[3]
        topics_text = subject[4]

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

        topics = split_topics(
            topics_text
        )

        total_priority += priority_score

        analyzed_subjects.append({

            "subject": subject_name,

            "exam_date": exam_date,

            "weakness": weakness,

            "topics": topics,

            "days_left": days_left,

            "priority_score": priority_score,

            "priority": priority

        })


    # --------------------------------------------------
    # HIGH PRIORITY FIRST
    # --------------------------------------------------

    analyzed_subjects.sort(
        key=lambda item: item["priority_score"],
        reverse=True
    )


    study_plan = []


    # --------------------------------------------------
    # DISTRIBUTE STUDY HOURS
    # --------------------------------------------------

    for subject in analyzed_subjects:

        if total_priority == 0:

            subject_hours = (
                available_hours
                / len(analyzed_subjects)
            )

        else:

            subject_hours = (
                subject["priority_score"]
                / total_priority
            ) * available_hours


        # Minimum block
        subject_hours = max(
            subject_hours,
            0.5
        )

        subject_hours = round(
            subject_hours,
            1
        )


        topics = subject["topics"]


        # --------------------------------------------------
        # IF TOPICS ARE AVAILABLE
        # --------------------------------------------------

        if topics:

            # Maximum 3 different tasks per subject/day
            selected_topics = topics[:3]

            duration_per_topic = (
                subject_hours
                / len(selected_topics)
            )

            duration_per_topic = round(
                max(duration_per_topic, 0.25),
                1
            )


            for topic in selected_topics:

                if subject["days_left"] <= 2:

                    activity = (
                        f"Final revision of {topic} "
                        f"and practice important exam questions"
                    )

                elif subject["priority"] == "High":

                    activity = (
                        f"Study {topic}, revise weak concepts "
                        f"and solve practice questions"
                    )

                elif subject["priority"] == "Medium":

                    activity = (
                        f"Study {topic} and complete "
                        f"a short revision session"
                    )

                else:

                    activity = (
                        f"Review notes for {topic} "
                        f"and revise key concepts"
                    )


                study_plan.append({

                    "subject":
                        subject["subject"],

                    "task":
                        activity,

                    "duration":
                        duration_per_topic,

                    "priority":
                        subject["priority"],

                    "days_left":
                        subject["days_left"],

                    "exam_date":
                        subject["exam_date"]

                })


        # --------------------------------------------------
        # IF NO TOPICS ENTERED
        # --------------------------------------------------

        else:

            if subject["days_left"] <= 2:

                task = (
                    "Final revision and practice "
                    "important exam questions"
                )

            elif subject["priority"] == "High":

                task = (
                    "Focus study, practice questions "
                    "and revise weak areas"
                )

            elif subject["priority"] == "Medium":

                task = (
                    "Study core concepts and "
                    "complete revision"
                )

            else:

                task = (
                    "Review notes and revise "
                    "important concepts"
                )


            study_plan.append({

                "subject":
                    subject["subject"],

                "task":
                    task,

                "duration":
                    subject_hours,

                "priority":
                    subject["priority"],

                "days_left":
                    subject["days_left"],

                "exam_date":
                    subject["exam_date"]

            })


    return study_plan