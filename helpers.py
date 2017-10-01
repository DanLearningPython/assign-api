import json


def courses_to_json(results):

    json_result = []

    for result in results:
        #print (vars(course))
        #view_obj_structure(result)
        course = result.Course
        semester = result.Semester
        tmp = {
            'id' : course.id,
            'course_name': course.course_name,
            'semester': [
                semester.id,
                semester.season,
                semester.year
            ]
        }
        json_result.append(tmp.copy())

    return json_result


def view_obj_structure(object):
    for attr in dir(object):
        print(attr, getattr(object, attr))