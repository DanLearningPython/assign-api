import json
import datetime


def courses_to_json(results):

    json_result = []

    for course in results:
        #print (vars(course))

        semester = course.semester
        assignments = []

        #view_obj_structure(course)

        print(course.assignments)
        for assignment in course.assignments:
            tmp_assignment = assignment_to_json(assignment)
            assignments.append(tmp_assignment.copy())

        tmp = {
            'id' : course.id,
            'course_name': course.course_name,
            'semester': {
                'id': semester.id,
                'season': semester.season,
                'year': semester.year
            },
            'assignments' : assignments
        }
        json_result.append(tmp.copy())

    return json_result


def assignment_to_json(assignment):

    tmp = {
        'id': assignment.id,
        'name': assignment.name,
        'description' : assignment.description,
        'due_date' : assignment.due_date.strftime("%Y-%m-%d %H:%M:%S"),
        'use_date_control' : assignment.use_date_control,
        'group_submission' : assignment.group_submission,
        'students_per_group_min' : assignment.students_per_group_min,
        'students_per_group_max' : assignment.students_per_group_max,
        'submission_enabled' : assignment.submission_enabled,
        'access_enabled' : assignment.access_enabled,
        'access_open_date' : assignment.access_open_date,
        'access_close_date': assignment.access_close_date,
        'submission_open_date': assignment.submission_open_date,
        'submission_close_date': assignment.submission_close_date,
        'submission_attempts_max' : assignment.submission_attempts_max,
        'allow_not_done' : assignment.allow_not_done,
        'script_enabled' : assignment.script_enabled
    }

    return tmp


def view_obj_structure(object):
    for attr in dir(object):
        print(attr, getattr(object, attr))


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}', must be in %Y-%m-%d %H:%M:%S format.".format(s)
        raise ValueError(msg)