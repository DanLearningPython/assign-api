import json


def courses_to_json(courses):

    json_result = []

    for course in courses:
        tmp = {
            'id' : course.id,
            'course_name': course.course_name,
            'semester': course.semester_id,
        }
        json_result.append(tmp.copy())

    return (json_result)