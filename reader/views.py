from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core import serializers

from django.core.serializers.json import DjangoJSONEncoder

from reader.models import *
from quiz import models as quiz_models

import random

from django.db import connection
from django.db.models import Count

import ast

#Global variables
user_id = 0
group_id = 0
num_students = 0


def home(request):
    global user_id
    if request.user.is_authenticated():
        user_id = request.user.id
        group_ids_query = Group.objects.values().filter(students__id=user_id)
        group_ids = []
        for group in group_ids_query:
            group_ids.append({"id":group["id"],"name":group["name"]})
        final_json = {"groups": group_ids}
        final_json_wo_unicode = json.dumps(final_json)
        final_json_dict = ast.literal_eval(final_json_wo_unicode)
        return render(request, "home.html", final_json_dict)


def load_course(request,url_group_id):
    global user_id, group_id, num_students
    group_id = url_group_id
    course_id = Group.objects.only("course").get(id=group_id).course.id
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            last_page_read = ReadingLog.objects.values().filter(user__id=user_id, group__id=group_id, action="page-load").latest("datetime")
            #print(connection.queries[-1]["sql"])
            #print(last_page_read)
            last_page_read["datetime"] = str(last_page_read["datetime"])
            last_page_read["zoom"] = float(last_page_read["zoom"])
        except ReadingLog.DoesNotExist:
            last_page_read = {}
            #print("No reading")
        course_json = Course.objects.get(id=course_id)
        num_students = int(Group.objects.annotate(num_students=Count('students'))[0].num_students)
        hierarchical_structure = course_json.course_structure
        calculate_reading_progress(hierarchical_structure)
        final_json = {"group":group_id, "course":{"id":course_json.id, "name":course_json.name}, "course_hierarchical":hierarchical_structure,"last_page_read":last_page_read}
        final_json_wo_unicode = json.dumps(final_json)
        final_json_dict = ast.literal_eval(final_json_wo_unicode)
        return render(request, "reader.html", final_json_dict)


def calculate_reading_progress(node):
    if "children" not in node:
        num_pages = get_number_of_pages(node)
        read_pages = get_number_of_read_pages(node)
        group_read_pages = get_number_of_group_read_pages(node)
        set_number_of_pages(node,num_pages)
        set_number_of_read_pages(node, read_pages)
        set_number_of_group_read_pages(node, group_read_pages)
        set_quiz(node)
        return num_pages, read_pages, group_read_pages
    else:
        if has_pages(node):
            subsections_num_pages, subsections_read_pages, subsections_group_read_pages = calculate_subsections_reading_progress(node["children"])
            num_pages = get_number_of_pages(node) + subsections_num_pages
            read_pages = list(set(get_number_of_read_pages(node) + subsections_read_pages))
            group_read_pages = get_number_of_group_read_pages(node) + subsections_group_read_pages
            set_number_of_pages(node,num_pages)
            set_number_of_read_pages(node,read_pages)
            set_number_of_group_read_pages(node, group_read_pages)
            set_quiz(node)
            return num_pages, read_pages, group_read_pages
        else:
            num_pages, read_pages, group_read_pages = calculate_subsections_reading_progress(node["children"])
            set_number_of_pages(node,num_pages)
            set_number_of_read_pages(node, read_pages)
            set_number_of_group_read_pages(node, group_read_pages)
            set_quiz(node)
            return num_pages, read_pages, group_read_pages


def calculate_subsections_reading_progress(subsections):
    total_pages = 0
    read_pages = []
    group_read_pages = 0
    for subsection in subsections:
        subsection_total_pages, subsection_read_pages, subsection_group_read_pages = calculate_reading_progress(subsection)
        total_pages = total_pages + subsection_total_pages
        read_pages = list(set(read_pages + subsection_read_pages))
        group_read_pages = group_read_pages + subsection_group_read_pages
    return total_pages, read_pages, group_read_pages


def get_number_of_pages(node):
    spage = int(node["spage"])
    epage = int(node["epage"])
    return epage - spage + 1


def get_number_of_read_pages(node):
    global user_id, group_id
    section_id = node["id"]
    read_pages = set(
        ReadingLog.objects.values_list('page', flat=True).filter(user__id=user_id, group__id=group_id, section=section_id,
                                                                 action="page-load"))
    read_pages = list(read_pages)
    return read_pages


def get_number_of_group_read_pages(node):
    global user_id, group_id, num_students
    section_id = node["id"]
    tuples_student_and_page_read = ReadingLog.objects.values_list('user__id', 'page').exclude(user__id=user_id).filter(group__id=group_id, section=section_id, action="page-load").distinct().count()
    group_read_pages = 0
    if(num_students>1):
        group_read_pages = tuples_student_and_page_read / (num_students-1)
    return group_read_pages


def has_pages(node):
    if "spage" in node and "epage" in node and "resourceid" in node:
        return True
    else:
        return False


def set_number_of_pages(node, num_pages):
    node["num_pages"] = num_pages


def set_number_of_read_pages(node, read_pages):
    node["read_pages"] = len(read_pages)
    node["read_pages_list"] = read_pages


def set_number_of_group_read_pages(node, num_group_read_pages):
    node["group_read_pages"] = num_group_read_pages

def set_quiz(node):
    global user_id, group_id
    section_id = node["id"]
    try:
        quiz = quiz_models.Quiz.objects.get(course_section=section_id)
        corrects = quiz_models.AnswerLog.objects.filter(user=user_id, group=group_id, quiz= quiz.id, submitted=True, correct=True).count()
        incorrects = quiz_models.AnswerLog.objects.filter(user=user_id, group=group_id, quiz=quiz.id, submitted=True,
                                                        correct=False).count()
        #corrects = random.randint(0, 10)
        #incorrects = random.randint(0,10)
        corrects_group = random.randint(0,10)
        incorrects_group = random.randint(0, 10)
        node["quiz"] = {"name": quiz.name, "corrects":corrects, "incorrects": incorrects, "corrects_group":corrects_group, "incorrects_group":incorrects_group}
    except quiz_models.Quiz.DoesNotExist:
        quiz = None

