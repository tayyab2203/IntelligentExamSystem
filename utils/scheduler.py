def allocate_study_time(student_profile):
    topics = student_profile["topics"]
    total_days = (student_profile["exam_date"] - student_profile["current_date"]).days
    daily_hours = student_profile["daily_study_hours"]
    total_available_hours = max(total_days * daily_hours, 1)

    total_priority = sum(t["priority"] for t in topics if t["priority"] > 0)

    for topic in topics:
        if topic["priority"] == 0 or total_priority == 0:
            topic["allocated_hours"] = 0
        else:
            share = topic["priority"] / total_priority
            topic["allocated_hours"] = round(share * total_available_hours, 2)

    return topics