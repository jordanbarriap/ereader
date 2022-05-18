from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core import serializers

from django.core.serializers.json import DjangoJSONEncoder

from reader.models import *
from quiz import models as quiz_models

from django.db import connection
from django.db.models import Count

from django.conf import settings
from django.contrib.auth import login

import ast

#Global variables
user_id = 0
group_id = 0
course_id = 0
num_students = 0

section_pages_info = []

def home(request):
    global user_id
    if request.user.is_authenticated:
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
    global user_id, group_id, num_students, read_pages_dict, group_read_pages_dict, quizzes_correct_dict, quizzes_incorrect_dict, group_quizzes_correct_dict, group_quizzes_incorrect_dict
    group_id = url_group_id
    course_id = Group.objects.only("course").get(id=group_id).course.id
    if request.user.is_authenticated:
        user_id = request.user.id
        try:
            last_page_read = ReadingLog.objects.values().filter(user__id=user_id, group__id=group_id, action="page-load").latest("datetime")

            last_page_read["datetime"] = str(last_page_read["datetime"])
            last_page_read["zoom"] = float(last_page_read["zoom"])
        except ReadingLog.DoesNotExist:
            last_page_read = {}

        course_json = Course.objects.get(id=course_id)

        num_students = Group.objects.get(id= group_id).students.count()
        hierarchical_structure = course_json.course_structure

        read_pages_dict = {}
        group_read_pages_dict = {}

        read_pages_queryset = ReadingLog.objects.raw("SELECT id, user_id, section, page FROM reader_readinglog WHERE action='page-load' AND user_id="+str(user_id)+" AND group_id='"+group_id+"' GROUP BY id, user_id, section, page;")

        for section_page in read_pages_queryset:
            section = section_page.section
            page = int(section_page.page)
            if section not in read_pages_dict.keys():
                read_pages_dict[section] = [page]
            else:
                read_pages_dict[section].append(page)

        group_read_pages_queryset = ReadingLog.objects.raw(
            "SELECT id, user_id, section, page FROM reader_readinglog WHERE action='page-load' AND user_id<>" + str(
                user_id) + " AND group_id='" + group_id + "' GROUP BY id, user_id, section, page;")

        for section_page in group_read_pages_queryset:
            section = section_page.section
            page = int(section_page.page)
            if section not in group_read_pages_dict.keys():
                group_read_pages_dict[section] = [page]
            else:
                group_read_pages_dict[section].append(page)

        quizzes_correct_queryset = quiz_models.AnswerLog.objects.raw("SELECT id, quiz_id, question_id FROM quiz_answerlog WHERE user_id="+str(user_id)+" AND group_id='"+group_id+"' AND submitted=1 AND correct=1;")
        quizzes_correct_dict = {}

        for quiz_attempt in quizzes_correct_queryset:
            quiz = quiz_attempt.quiz_id
            question = quiz_attempt.question_id
            if quiz not in quizzes_correct_dict.keys():
                quizzes_correct_dict[quiz] = [question]
            else:
                quizzes_correct_dict[quiz].append(question)

        quizzes_incorrect_queryset = quiz_models.AnswerLog.objects.raw(
            "SELECT id, quiz_id, question_id FROM quiz_answerlog WHERE user_id=" + str(
                user_id) + " AND group_id='" + group_id + "' AND submitted=1 AND correct=0;")
        quizzes_incorrect_dict = {}

        for quiz_attempt in quizzes_incorrect_queryset:
            quiz = quiz_attempt.quiz_id
            question = quiz_attempt.question_id
            if quiz not in quizzes_incorrect_dict.keys():
                quizzes_incorrect_dict[quiz] = [question]
            else:
                quizzes_incorrect_dict[quiz].append(question)


        group_quizzes_correct_queryset = quiz_models.AnswerLog.objects.raw(
            "SELECT id, quiz_id, question_id FROM quiz_answerlog WHERE user_id<>" + str(
                user_id) + " AND group_id='" + group_id + "' AND submitted=1 AND correct=1;")
        group_quizzes_correct_dict = {}

        for quiz_attempt in group_quizzes_correct_queryset:
            quiz = quiz_attempt.quiz_id
            question = quiz_attempt.question_id
            if quiz not in group_quizzes_correct_dict.keys():
                group_quizzes_correct_dict[quiz] = [question]
            else:
                group_quizzes_correct_dict[quiz].append(question)

        group_quizzes_incorrect_queryset = quiz_models.AnswerLog.objects.raw(
            "SELECT id, quiz_id, question_id FROM quiz_answerlog WHERE user_id<>" + str(
                user_id) + " AND group_id='" + group_id + "' AND submitted=1 AND correct=0;")
        group_quizzes_incorrect_dict = {}

        for quiz_attempt in group_quizzes_incorrect_queryset:
            quiz = quiz_attempt.quiz_id
            question = quiz_attempt.question_id
            if quiz not in group_quizzes_incorrect_dict.keys():
                group_quizzes_incorrect_dict[quiz] = [question]
            else:
                group_quizzes_incorrect_dict[quiz].append(question)

        calculate_reading_progress(hierarchical_structure)

        final_json = {"group":group_id, "course":{"id":course_json.id, "name": course_json.name}, "course_hierarchical": hierarchical_structure, "last_page_read": last_page_read}
        final_json_wo_unicode = json.dumps(final_json)
        final_json_dict = ast.literal_eval(final_json_wo_unicode)
        return render(request, "reader.html", final_json_dict)

def load_course_with_section_id(request,url_course_id,url_section_id):
    global user_id, group_id, course_id, num_students, read_pages_dict, group_read_pages_dict, quizzes_correct_dict, quizzes_incorrect_dict, group_quizzes_correct_dict, group_quizzes_incorrect_dict
#     #group_id = url_group_id
#     #course_id = Group.objects.only("course").get(id=group_id).course.id
    
    group_id = request.GET.get('grp')
    course_id = url_course_id
    section_id = url_section_id
    username = request.GET.get('usr')
    cid = request.GET.get('cid')
    sid = request.GET.get('sid')

    #Force login without using password
    user = User.objects.get(username=username)
    user_id = user.id
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request,user)

    try:
    #       #last_page_read = ReadingLog.objects.values().filter(user__id=user_id, group__id=group_id, action="page-load",section=section_id).latest("datetime")
    #       #TO-DO: do not forget to add group_id to the query
          last_page_read = ReadingLog.objects.values().filter(user__id=user_id, action="page-load",section=section_id).latest("datetime")
          last_page_read["datetime"] = str(last_page_read["datetime"])
          last_page_read["zoom"] = float(last_page_read["zoom"])

    except ReadingLog.DoesNotExist:
          last_page_read = {}

    course_json = Course.objects.get(id=course_id)

    #num_students = Group.objects.get(id= group_id).students.count()
    hierarchical_structure = course_json.course_structure

    read_pages_dict = {}
    group_read_pages_dict = {}

    read_pages_queryset = ReadingLog.objects.raw("SELECT id, user_id, section, page FROM reader_readinglog WHERE action='page-load' AND user_id="+str(user_id)+" AND group_id='"+group_id+"' GROUP BY id, user_id, section, page;")

    for section_page in read_pages_queryset:
        section = section_page.section
        page = int(section_page.page)
        if section not in read_pages_dict.keys():
            read_pages_dict[section] = [page]
        else:
            read_pages_dict[section].append(page)

    group_read_pages_queryset = ReadingLog.objects.raw(
        "SELECT id, user_id, section, page FROM reader_readinglog WHERE action='page-load' AND user_id<>" + str(
            user_id) + " AND group_id='" + group_id + "' GROUP BY id, user_id, section, page;")

    for section_page in group_read_pages_queryset:
        section = section_page.section
        page = int(section_page.page)
        if section not in group_read_pages_dict.keys():
            group_read_pages_dict[section] = [page]
        else:
            group_read_pages_dict[section].append(page)

    calculate_reading_progress_no_quiz(hierarchical_structure)

    final_json = {"group":group_id, "course":{"id":course_json.id, "name": course_json.name}, "course_hierarchical": hierarchical_structure, "last_page_read": last_page_read, "section_id":section_id, "cid": cid, "sid":sid ,"username": username}
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


def calculate_reading_progress_no_quiz(node):
    if "children" not in node:
        num_pages = get_number_of_pages(node)
        read_pages = get_number_of_read_pages(node)
        group_read_pages = get_number_of_group_read_pages(node)
        set_number_of_pages(node,num_pages)
        set_number_of_read_pages(node, read_pages)
        set_number_of_group_read_pages(node, group_read_pages)
        #set_quiz(node)
        return num_pages, read_pages, group_read_pages
    else:
        if has_pages(node):
            subsections_num_pages, subsections_read_pages, subsections_group_read_pages = calculate_subsections_reading_progress_no_quiz(node["children"])
            num_pages = get_number_of_pages(node) + subsections_num_pages
            read_pages = list(set(get_number_of_read_pages(node) + subsections_read_pages))
            group_read_pages = get_number_of_group_read_pages(node) + subsections_group_read_pages
            set_number_of_pages(node,num_pages)
            set_number_of_read_pages(node,read_pages)
            set_number_of_group_read_pages(node, group_read_pages)
            #set_quiz(node)
            return num_pages, read_pages, group_read_pages
        else:
            num_pages, read_pages, group_read_pages = calculate_subsections_reading_progress_no_quiz(node["children"])
            set_number_of_pages(node,num_pages)
            set_number_of_read_pages(node, read_pages)
            set_number_of_group_read_pages(node, group_read_pages)
            #set_quiz(node)
            return num_pages, read_pages, group_read_pages


def calculate_subsections_reading_progress_no_quiz(subsections):
    total_pages = 0
    read_pages = []
    group_read_pages = 0
    for subsection in subsections:
        subsection_total_pages, subsection_read_pages, subsection_group_read_pages = calculate_reading_progress_no_quiz(subsection)
        total_pages = total_pages + subsection_total_pages
        read_pages = list(set(read_pages + subsection_read_pages))
        group_read_pages = group_read_pages + subsection_group_read_pages
    return total_pages, read_pages, group_read_pages


def get_number_of_pages(node):
    spage = int(node["spage"])
    epage = int(node["epage"])
    return epage - spage + 1


def get_number_of_read_pages(node):
    global user_id, group_id, read_pages_dict
    section_id = node["id"]
    #read_pages = ReadingLog.objects.values_list('page', flat=True).filter(user__id=user_id, group__id=group_id, section=section_id, action="page-load").distinct()
    #read_pages = list(read_pages)
    read_pages = []
    if section_id in read_pages_dict.keys():
        read_pages = read_pages_dict[section_id]
    return read_pages


def get_number_of_group_read_pages(node):
    global user_id, group_id, num_students, group_read_pages_dict
    section_id = node["id"]
    #tuples_student_and_page_read = ReadingLog.objects.values_list('user__id', 'page').exclude(user__id=user_id).filter(group__id=group_id, section=section_id, action="page-load").distinct().count()
    group_read_pages = 0
    if section_id in group_read_pages_dict.keys():
        if(num_students>1):
            tuples_student_and_page_read = len(group_read_pages_dict[section_id])
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
    global user_id, group_id, quizzes_correct_dict, quizzes_incorrect_dict, group_quizzes_correct_dict, group_quizzes_incorrect_dict
    section_id = node["id"]
    try:
        quiz= quiz_models.Quiz.objects.get(course_section=section_id)
        quiz_name = quiz.name
        quiz_id = quiz.id
        # corrects = quiz_models.AnswerLog.objects.filter(user=user_id, group=group_id, quiz= quiz.id, submitted=True, correct=True).count()
        # incorrects = quiz_models.AnswerLog.objects.filter(user=user_id, group=group_id, quiz=quiz.id, submitted=True,
        #                                                 correct=False).count()
        # corrects_group = quiz_models.AnswerLog.objects.exclude(user__id=user_id).filter(group=group_id, quiz=quiz.id, submitted=True,
        #                                                 correct=True).count()
        # incorrects_group = quiz_models.AnswerLog.objects.exclude(user__id=user_id).filter(group=group_id, quiz=quiz.id, submitted=True,
        #                                                   correct=False).count()
        corrects = 0
        incorrects = 0
        corrects_group = 0
        incorrects_group = 0
        if quiz_id in quizzes_correct_dict.keys():
            corrects = len(quizzes_correct_dict[quiz_id])
        if quiz_id in quizzes_incorrect_dict.keys():
            incorrects = len(quizzes_incorrect_dict[quiz_id])
        if quiz_id in group_quizzes_correct_dict.keys():
            corrects_group = len(group_quizzes_correct_dict[quiz_id])
        if quiz_id in group_quizzes_incorrect_dict.keys():
            incorrects_group = len(group_quizzes_incorrect_dict[quiz_id])
        node["quiz"] = {"name": quiz_name, "corrects":corrects, "incorrects": incorrects, "corrects_group":corrects_group, "incorrects_group":incorrects_group}
    except quiz_models.Quiz.DoesNotExist:
        quiz = None


def calculate_sections_with_pages(node, level):
    global section_pages_info
    if "children" not in node:
        num_pages = get_number_of_pages(node)
        section_id = [node["id"]]
        # if level==1:
        #     print section_id
        #     print str(num_pages) + " (level: " + str(level) + ")"
        return num_pages, section_id
    else:
        if has_pages(node):
            subsections_num_pages, subsections_section_ids = calculate_subsections_with_pages(node["children"], level)
            num_pages = get_number_of_pages(node) + subsections_num_pages
            section_id = [node["id"]] + subsections_section_ids
            # if level==1:
            #     print section_id
            #     print str(num_pages) + " (level: " + str(level) + ")"
            return num_pages, section_id
        else:
            num_pages, section_id = calculate_subsections_with_pages(node["children"], level)
            if level==1:
                # print "section id: "+node["id"]
                # print section_id
                # print str(num_pages) + " (level: " + str(level) + ")"
                section_pages_info.append({"id": node["id"], "name": node["title"], "subsections": section_id, "pages": num_pages})
            return num_pages, section_id


def calculate_subsections_with_pages(subsections, level):
    total_pages = 0
    section_id = []
    for subsection in subsections:
        subsection_total_pages, subsection_section_ids = calculate_sections_with_pages(subsection, level+1)
        total_pages = total_pages + subsection_total_pages
        section_id = section_id + subsection_section_ids
    return total_pages, section_id


