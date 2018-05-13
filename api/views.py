from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import (HttpResponse,
                         HttpResponseForbidden,
                         HttpResponseBadRequest)
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.core import serializers

from annotator import models as annotator_models

from quiz import models as quiz_models

from reader import models as reader_models
from reader import views as reader_views

from django.contrib.auth.models import User

import json
import csv

from api import serializers


############################### Annotator API views ###############################

class JSONResponse(HttpResponse):
    """
    An ``HttpResponse`` that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)

def root(request):
    if request.method == "GET":
        return JSONResponse({"name": getattr(settings,
                                             "ANNOTATOR_NAME",
                                             "django-annotator-store"),
                             "version": annotator.__version__})
    else:
        return HttpResponseForbidden()


@csrf_exempt
def index_create(request):
    if request.method == "GET":
        annotations = annotator_models.Annotation.objects.all()
        serializer = serializers.AnnotationSerializer(annotations, many=True)
        return JSONResponse(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = serializers.AnnotationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = HttpResponse(status=303)
            response["Location"] = reverse("read_update_delete",
                                           kwargs={"pk": serializer.data["id"]})
            return response
        else:
            return HttpResponseBadRequest(content=str(serializer.errors))
    else:
        return HttpResponseForbidden()


@csrf_exempt
def read_update_delete(request, pk):
    if request.method == "GET":
        annotation = get_object_or_404(annotator_models.Annotation, pk=pk)
        serializer = serializers.AnnotationSerializer(annotation)
        return JSONResponse(serializer.data, status=200)
    elif request.method == "PUT":
        annotation = get_object_or_404(annotator_models.Annotation, pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.AnnotationSerializer(annotation, data=data)
        if serializer.is_valid():
            serializer.save()
            response = HttpResponse(status=303)
            response["Location"] = reverse("read_update_delete",
                                           kwargs={"pk": serializer.data["id"]})
            return response
        else:
            return HttpResponseBadRequest(content=str(serializer.errors))
    elif request.method == "DELETE":
        annotation = get_object_or_404(annotator_models.Annotation, pk=pk)
        annotation.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponseForbidden()


def search(request):
    if request.method == "GET":
        query = {k: v for k, v in request.GET.items()}
        annotations = annotator_models.Annotation.objects.filter(**query)
        serializer = serializers.AnnotationSerializer(annotations, many=True)
        return JSONResponse({"total": len(serializer.data), "rows": serializer.data})
    else:
        return HttpResponseForbidden()


############################### Reading Log API views ###############################
@csrf_exempt
def reading_log(request):
    """
    Add a reading log
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReadingLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return HttpResponseBadRequest(content=str(serializer.errors))
    else:
        return HttpResponseForbidden()


############################### Quiz API views ###############################
""""@csrf_exempt
def quiz(request):
    #Returning a requested quiz for an specific course section
    if request.method == 'GET':
        section_id = request.GET["section"]

        #Query the multiple choice questions associated with the section
        mcquestions = quiz_models.Quiz.objects.filter(course_section=section_id).values("mcquestions__id","mcquestions__statement","mcquestions__answers__id","mcquestions__answers__statement", "mcquestions__answers__order")
        mcquestions_json = {}
        if len(mcquestions)>0:
            for question in mcquestions:
                question_id = question["mcquestions__id"]
                if question_id not in mcquestions_json:
                    mcquestions_json[question_id]={"statement":question["mcquestions__statement"], "answers":[{"id":question["mcquestions__answers__id"], "statement":question["mcquestions__answers__statement"],  "order":question["mcquestions__answers__order"]}]}
                else:
                    mcquestions_json[question_id]["answers"].append({"id":question["mcquestions__answers__id"], "statement":question["mcquestions__answers__statement"],  "order":question["mcquestions__answers__order"]})

        #Query the textual questions associated with the section
        textualquestions = quiz_models.Quiz.objects.filter(course_section=section_id).values("textualquestions__id","textualquestions__statement")
        textualquestions_json = {}
        if len(textualquestions) > 0:
            for question in textualquestions:
                question_id = question["textualquestions__id"]
                if question_id not in textualquestions_json:
                    textualquestions_json[question_id] = {"statement": question["textualquestions__statement"]}

        return JSONResponse({"mcquestions":mcquestions_json, "textualquestions":textualquestions_json}, status=201)

    else:
        return HttpResponseForbidden()
"""

""""@csrf_exempt
def quiz(request):
    #Returning a requested quiz for an specific course section
    if request.method == 'GET':
        section_id = request.GET["section"]

        #Query the multiple choice questions associated with the section
        mcquestions = quiz_models.Quiz.objects.filter(course_section=section_id).values("mcquestions__id","mcquestions__statement","mcquestions__answers__id","mcquestions__answers__statement", "mcquestions__answers__order")
        mcquestions_json = {}
        if len(mcquestions)>0:
            for question in mcquestions:
                question_id = question["mcquestions__id"]
                if question_id not in mcquestions_json:
                    mcquestions_json[question_id]={"statement":question["mcquestions__statement"], "answers":[{"id":question["mcquestions__answers__id"], "statement":question["mcquestions__answers__statement"],  "order":question["mcquestions__answers__order"]}]}
                else:
                    mcquestions_json[question_id]["answers"].append({"id":question["mcquestions__answers__id"], "statement":question["mcquestions__answers__statement"],  "order":question["mcquestions__answers__order"]})

        #Query the textual questions associated with the section
        textualquestions = quiz_models.Quiz.objects.filter(course_section=section_id).values("textualquestions__id","textualquestions__statement")
        textualquestions_json = {}
        if len(textualquestions) > 0:
            for question in textualquestions:
                question_id = question["textualquestions__id"]
                if question_id not in textualquestions_json:
                    textualquestions_json[question_id] = {"statement": question["textualquestions__statement"]}

        return JSONResponse({"mcquestions":mcquestions_json, "textualquestions":textualquestions_json}, status=201)

    else:
        return HttpResponseForbidden()
"""

@csrf_exempt
def quiz(request):
    #Returning a requested quiz for an specific course section
    if request.method == 'GET':
        #section_id = request.GET["section"]
        section_id = request.GET["section"].split(",")  # ids of quizzes subsections
        user_id = request.GET["user"]
        #Query the multiple choice questions associated with the section
        #questions = quiz_models.Quiz.objects.filter(course_section=section_id).values("questions__id", "questions__statement", "questions__type","questions__choice__id")#,"questions__choice__statement")
        #quiz = quiz_models.Quiz.objects.get(course_section=section_id)
        quiz = quiz_models.Quiz.objects.filter(course_section__in=section_id)
        #questions = quiz_models.Question.objects.filter(quiz__course_section=section_id)
        questions = quiz_models.Question.objects.filter(quiz__course_section__in=section_id)
        choices = quiz_models.Choice.objects.filter(question__id__in=questions)
        questions_json = {}
        if len(questions)>0:
            for question in questions:
                question_id = question.id
                correct_result = quiz_models.AnswerLog.objects.filter(user=user_id, question=question_id, correct=1)
                correct = False
                previous_answer = []
                if (len(correct_result)>0):
                    previous_answer = correct_result.earliest("datetime")
                    previous_answer = previous_answer.answer
                    correct = True
                questions_json[question_id] = {"statement": question.statement, "type": question.type, "correct": correct, "previous_answer": previous_answer,
                                                   "choices": []}
        if len(choices)>0:
            for choice in choices:
                question_id = choice.question_id
                choice_json = {"id":choice.id, "statement": choice.statement}
                questions_json[question_id]["choices"].append(choice_json)

        #return JSONResponse({"quiz":quiz.id, "name": quiz.name, "questions": questions_json}, status=201)
        return JSONResponse({"quiz": section_id, "questions": questions_json}, status=201)

    else:
        return HttpResponseForbidden()

@csrf_exempt
def assess(request):
    """
    Check correctness of student answers
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data["user"]
        group_id = data["group"]
        session_id = data["session"]
        datetime = data["datetime"]
        quiz_id = data["quiz"]
        answers = data["answers"]
        assessment = []
        quiz_correctness = True
        for answer in answers:
            question_id = answer["question_id"]
            type = answer["type"]
            # Process answers from multiple-choice one-answer questions
            if type == "multiple-choice-one-answer":
                answer_id = int(answer["answer"])
                correct = True
                correct_answers = quiz_models.Question_Correct_Answer.objects.filter(question_id=question_id).values("choice_id")
                for correct_answer in correct_answers:
                    if correct_answer["choice_id"] != answer_id:
                        correct = False
                        quiz_correctness = False
                answer_log = quiz_models.AnswerLog(user=User.objects.get(id=user_id), group=reader_models.Group.objects.get(id=group_id), session=session_id, datetime=datetime, quiz=quiz_models.Quiz.objects.get(id=quiz_id), question=quiz_models.Question(id=question_id),
                                                   answer=answer_id, correct=correct, submitted=True)
                answer_log.save()

            #Process answers from multiple-choice multiple-answer questions
            if type == "multiple-choice-multiple-answer":
                answer_ids = answer["answer"]
                for i in range (0,len(answer_ids)):
                    answer_ids[i] = int(answer_ids[i])
                correct = True
                correct_answers = quiz_models.Question_Correct_Answer.objects.filter(question_id=question_id).values("choice_id")
                for correct_answer in correct_answers:
                    if correct_answer["choice_id"] not in answer_ids:
                        correct = False
                        quiz_correctness = False
                #answer_log = quiz_models.AnswerLog(user=User.objects.get(id=user_id), group=reader_models.Group.objects.get(id=group_id), session=session_id, datetime=datetime, quiz=quiz_models.Quiz.objects.get(id=quiz_id), question=quiz_models.Question(id=question_id),
                #                                   answer=answer_ids, correct=correct, submitted=True)
                answer_log = quiz_models.AnswerLog(user=User.objects.get(id=user_id),
                                                   group=reader_models.Group.objects.get(id=group_id),
                                                   session=session_id, datetime=datetime,
                                                   quiz=quiz_models.Quiz.objects.get(questions__id=question_id),
                                                   question=quiz_models.Question(id=question_id),
                                                   answer=answer_ids, correct=correct, submitted=True)
                answer_log.save()

            assessment.append({"question_id":question_id, "type": type, "correct":correct})

        return JSONResponse({"quiz_correctness":quiz_correctness, "assessment": assessment}, status=201)

    else:
        return HttpResponseForbidden()

def attempt(request):
    """
    Log when a student mark a choice in a quiz
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data["user"]
        group_id = data["group"]
        session_id = data["session"]
        datetime = data["datetime"]
        quiz_id = data["quiz"]
        question_id = data["question"]
        type = data["type"]
        answers = data["answer"]
        for answer in answers:
            if type == "multiple-choice-one-answer":
                answer_id = int(data["answer"])
                correct = True
                correct_answers = quiz_models.Question_Correct_Answer.objects.filter(question_id=question_id).values("choice_id")
                for correct_answer in correct_answers:
                    if correct_answer["choice_id"] != answer_id:
                        correct = False
                answer_log = quiz_models.AnswerLog(user=User.objects.get(id=user_id), group=reader_models.Group.objects.get(id=group_id), session=session_id, datetime=datetime, quiz=quiz_models.Quiz.objects.get(id=quiz_id), question=quiz_models.Question(id=question_id),
                                                   answer=answer_id, correct=correct,submitted=False)
                answer_log.save()
            if type == "multiple-choice-multiple-answer":
                answer_ids = answer["answer"]
                for i in range(0, len(answer_ids)):
                    answer_ids[i] = int(answer_ids[i])
                correct = True
                correct_answers = quiz_models.Question_Correct_Answer.objects.filter(question_id=question_id).values(
                    "choice_id")
                for correct_answer in correct_answers:
                    if correct_answer["choice_id"] not in answer_ids:
                        correct = False
                        quiz_correctness = False
                # answer_log = quiz_models.AnswerLog(user=User.objects.get(id=user_id), group=reader_models.Group.objects.get(id=group_id), session=session_id, datetime=datetime, quiz=quiz_models.Quiz.objects.get(id=quiz_id), question=quiz_models.Question(id=question_id),
                #                                   answer=answer_ids, correct=correct, submitted=True)
                answer_log = quiz_models.AnswerLog(user=User.objects.get(id=user_id),
                                                   group=reader_models.Group.objects.get(id=group_id),
                                                   session=session_id, datetime=datetime,
                                                   quiz=quiz_models.Quiz.objects.get(questions__id=question_id),
                                                   question=quiz_models.Question(id=question_id),
                                                   answer=answer_ids, correct=correct, submitted=False)
                answer_log.save()
        return JSONResponse({"tracked":True}, status=201)
    else:
        return HttpResponseForbidden()


@csrf_exempt
def kcs(request):
    """
    Returning a requested quiz for an specific course section
    """
    if request.method == 'GET':
        section_id = request.GET["section"]
        concepts = quiz_models.KC_Section.objects.filter(section=section_id).values("kc__name")
        concepts_json = []
        for kc in concepts:
            concepts_json.append(kc["kc__name"])
        return JSONResponse({"section":section_id, "kcs": concepts_json}, status=201)

    else:
        return HttpResponseForbidden()

@csrf_exempt
def summary(request):
    """
    Returning a requested quiz for an specific course section
    """
    if request.method == 'GET':
        group_id = request.GET["group_id"]

        course_id = reader_models.Group.objects.only("course").get(id=group_id).course.id

        course_json = reader_models.Course.objects.get(id=course_id)

        num_students = reader_models.Group.objects.get(id=group_id).students.count()

        reader_views.read_pages_dict = {}
        reader_views.group_read_pages_dict = {}
        reader_views.quizzes_correct_dict = {}
        reader_views.quizzes_incorrect_dict = {}
        reader_views.group_quizzes_correct_dict = {}
        reader_views.group_quizzes_incorrect_dict = {}

        hierarchical_structure = course_json.course_structure

        #reader_views.calculate_reading_progress(hierarchical_structure)
        reader_views.calculate_sections_with_pages(hierarchical_structure, 0)

        for section in reader_views.section_pages_info:
            name = section["name"]
            subsections = section["subsections"]
            subsections_str = "','".join(subsections)
            subsections_str = "'"+subsections_str+"'"
            print subsections_str
            # quizzes_correct_queryset = quiz_models.AnswerLog.objects.raw(
            #     "SELECT id, quiz_id, question_id FROM quiz_answerlog WHERE group_id='" + group_id + "' AND submitted=1 AND correct=1 AND section IN ("+subsections_str+");")
            # quizzes_correct_dict = {}
            #
            # for quiz_attempt in quizzes_correct_queryset:
            #     quiz = quiz_attempt.quiz_id
            #     question = quiz_attempt.question_id
            #     if quiz not in quizzes_correct_dict.keys():
            #         quizzes_correct_dict[quiz] = [question]
            #     else:
            #         quizzes_correct_dict[quiz].append(question)


        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="'+group_id+'_summary.csv"'

        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

        return response

    else:
        return HttpResponseForbidden()