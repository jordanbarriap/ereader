from django.conf import settings
from django.urls import reverse
from django.http import (HttpResponse,
                         HttpResponseForbidden,
                         HttpResponseBadRequest)
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models.functions import Cast

from annotator import models as annotator_models
from quiz import models as quiz_models
from reader import models as reader_models
from reader import views as reader_views
from recommender import models as rec_models
from smart_learning_content import models as slc_models
from wiki_content import models as wiki_models
from knowledgevis import models as knowledgevis_models

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
    """
    Returning a requested quiz for an specific course section
    """
    if request.method == 'GET':
        #section_id = request.GET["section"]
        section_id = request.GET["section"].split(",")  # ids of quizzes subsections
        user_id = request.GET["user"]
        group_id = request.GET["group"]
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
                correct_result = quiz_models.AnswerLog.objects.filter(user=user_id, group=reader_models.Group.objects.get(id=group_id), question=question_id, correct=1, submitted=1)
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
                                                   answer=answer_id, correct=correct, submitted=True, marked=True)
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
                                                   answer=answer_ids, correct=correct, submitted=True, marked=True)
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
        answer_data = data["answer"].split(" ")# 0: answer id, 1: marked or unmarked
        answer = answer_data[0]
        marked = False
        if answer_data[1] == "marked":
            marked = True

        if type == "multiple-choice-one-answer" or type == "multiple-choice-multiple-answer":
            answer_id = int(answer)
            correct = False
            correct_answers = quiz_models.Question_Correct_Answer.objects.filter(question_id=question_id).values("choice_id")
            print(answer_id)
            print(correct_answers)
            for correct_answer in correct_answers:
                print(correct_answer["choice_id"])
                if correct_answer["choice_id"] == answer_id:
                    correct = True
            answer_log = quiz_models.AnswerLog(user=User.objects.get(id=user_id), group=reader_models.Group.objects.get(id=group_id), session=session_id, datetime=datetime, quiz=quiz_models.Quiz.objects.get(questions__id=question_id), question=quiz_models.Question(id=question_id),
                                               answer=answer_id, correct=correct, submitted=False, marked=marked)
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
            print(subsections_str)
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

@csrf_exempt
def recommended_videos(request):
    """
    Returning all recommended videos for an specific course section
    """
    if request.method == 'GET':
        page_id = request.GET["page"]
        method = request.GET["method"]
        user_id = request.GET["user"]
        group_id = request.GET["group"]
        section_id = request.GET["section"]
        print("page: "+page_id+" , method: "+method)

        #Generates position for introducing noise into
        user_noise_position = int(user_id)%10
        page_noise_position=int(page_id[len(page_id)-1:len(page_id)])%10
        first_noise_position=(user_noise_position+page_noise_position)%10
        second_noise_position=first_noise_position*2

        print("1st noise position: "+str(first_noise_position))
        print("2nd noise position: "+str(second_noise_position))

        similar_videos_ids = rec_models.Similarity.objects.filter(id_textual_resource=page_id, type=method,
                                                                  resource_id__length__range=(30,1200)).values("resource_id__id","value").order_by('-value')[:50]


        videos_json = []
        #TODO: add this as a parameter in the api call
        num_top_videos = 18
        top_similar_videos_ids = similar_videos_ids[:num_top_videos]

        count=0
        for video_dict in top_similar_videos_ids:
            if (count == first_noise_position or count == second_noise_position):
                index_video_noise=len(similar_videos_ids) - 1
                if(count == first_noise_position):
                    index_video_noise = index_video_noise - 1
                video_noise = similar_videos_ids[index_video_noise]
                video_id = video_noise["resource_id__id"]
                similarity_value = video_noise["value"]
                video = rec_models.Resource.objects.get(id=video_id)
                try:
                    rating_video = rec_models.Rating.objects.filter(user=user_id,
                                                                    group=reader_models.Group.objects.get(id=group_id),
                                                                    section=section_id,
                                                                    resource=rec_models.Resource(id=video_id)).latest(
                        'datetime')
                    rating = rating_video.value
                    explanation_rating = rating_video.explanation
                except rec_models.Rating.DoesNotExist:
                    rating = -1
                    explanation_rating = ""
                videos_json.append({"title": video.title, "url": video.url, "value": similarity_value, "id": video_id,
                                    "rating": rating, "explanation_rating": explanation_rating, "noise":"yes","rank":index_video_noise})


            video_id = video_dict["resource_id__id"]
            similarity_value = video_dict["value"]
            video = rec_models.Resource.objects.get(id=video_id)
            try:
                rating_video = rec_models.Rating.objects.filter(user=user_id, group=reader_models.Group.objects.get(id=group_id), section=section_id, resource=rec_models.Resource(id=video_id)).latest('datetime')
                rating = rating_video.value
                explanation_rating = rating_video.explanation
            except rec_models.Rating.DoesNotExist:
                rating = -1
                explanation_rating = ""
            videos_json.append({"title": video.title, "url": video.url, "value": similarity_value, "id":video_id, "rating":rating, "explanation_rating": explanation_rating,"noise":"no","rank":count})
            count=count+1
        return JSONResponse({"page":page_id, "recommended_videos": videos_json}, status=201)

    else:
        return HttpResponseForbidden()


@csrf_exempt
def slc_programming(request):
    """
    Input: Request object from AJAX api call in the reader.html
    Method: Utilizes the content_type, provider_id and privacy values to pull the data
            related to smart learning content from the table in ereader database.
    Returns: On successful POST request, with JSON values on activity url
    """
    if request.method == "POST":
        section_id = request.POST["section_id"]
        resource_id = request.POST["resource_id"]
        page_id = request.POST["page_id"]
        content_type = request.POST["content_type"]
        provider_id = request.POST["provider_id"]
        privacy = request.POST["privacy"]

        slc_content_sections = slc_models.SmartContentSection.objects.filter(section_id=section_id)
        
        content_provider_list = slc_models.SmartContent.objects.order_by('content_type').values('content_type','provider_id').distinct()
        
        return_json = {}

        return_json["content_providers"] = content_provider_list
        
        for row3 in slc_content_sections:
            slc_content_component = slc_models.SmartContentConcept.objects.filter(component_name = row3.concept.rstrip())
            
            for row2 in slc_content_component:
                slc_content = slc_models.SmartContent.objects.filter(content_name = row2.content_name)
                for row1 in slc_content:
                    return_json[row1.content_id] = {
                                                        "content_name": row1.content_name,
                                                        "display_name": row1.display_name,
                                                        "content_type": row1.content_type,
                                                        "component_name": row2.component_name,
                                                        "context_name":  row2.context_name,
                                                        "provider_id" : row1.provider_id,
                                                        "activity_url": row1.url
                                                    }
        return JSONResponse(return_json,status=200)
    else:
        return HttpResponseForbidden()


@csrf_exempt
def wiki_resources_content(request):
    """
    Input: GET request to retrieve Wikipedia content related to the page/section
    Method: SELECT wiki_page_url by topic_name using topics table in ereader database
            and retrieving wikipedia pages using MediaWiki API calls (or DBPedia or 
            a Knowledge Graph server setup)
    Returns: On successful POST request, with JSON values on wikipedia page urls
    """
    if request.method == "POST":
        resource_id = request.POST['resource_id']
        page_id = request.POST['page_id']

        ## returns a list of wikipedia topics by course name, section name in the book and 
        ## page number in the textbook.
        wiki_articles = []
        with open(f"./data/concepts/concepts/{resource_id}-{page_id}.txt.concept.json") as concepts_file:
            list_of_concepts_jsons = concepts_file.readlines()
            for concept_json in list_of_concepts_jsons:
                wiki_articles.append(json.loads(concept_json))
                
        """
            - Section Articles: http://scythian.exp.sis.pitt.edu/Textbook/ir/sectionkey.php?name=[Section_Name]&type=[“simple/details”]
            - Question Articles: http://scythian.exp.sis.pitt.edu/Textbook/ir/questionkey.php?name=[Question_Name]&type=[“simple/details”]

            These APIs generate two version of the results (simple/details) which can be specified in the URL
            Simple results returns a list of item with “Rank”, “Title” and “Score” properties. Detail returns the same with the addition of the article summary from wikipedia.

            Here are some examples:

            Relevant Articles for Section iir-2.1 ->    http://scythian.exp.sis.pitt.edu/Textbook/ir/sectionkey.php?name=iir-2.1&type=simple
            Relevant Articles for Question q380 ->   http://scythian.exp.sis.pitt.edu/Textbook/ir/questionkey.php?name=q380&type=detail    
        """


        ### make url call to wikipedia with the topic names
        if False: wiki_pages_list = wiki_models.WikiContent.objects.filter(topic_names=wiki_page_topic_name)

        if False: return JSONResponse({"wiki_links":[row.topic_name for row in wiki_page_topic_names]},status=200)
        return JSONResponse(wiki_articles, status=200)
    else:
        return HttpResponseForbidden()



@csrf_exempt
def concept_map(request):
    """
    Returning a requested concept map created from an specific user for an specific course section
    """
    if request.method == 'GET':
        section_id = request.GET["section"]
        user_id = request.GET["user"]

        #Get concept map produced by the user (user_id) associated with the specific section (section_id)
        concept_map_results = knowledgevis_models.ConceptMap.objects.filter(user=user_id, section=section_id)

        concept_map_json = {}
        if len(concept_map_results)>0:
            concept_map = concept_map_results.latest("datetime")
            concept_map_json["result"] = True
            concept_map_json["conceptMap"] = concept_map.structure
        else:
            concept_map_json["result"] = False

        #return JSONResponse({"quiz":quiz.id, "name": quiz.name, "questions": questions_json}, status=201)
        return JSONResponse(concept_map_json, status=201)

    else:
        return HttpResponseForbidden()

@csrf_exempt
def concept_map_log(request):
    """
    Returning a requested concept map created from an specific user for an specific course section
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        concept_map = data["conceptMap"]
        action = data["action"]
        section_id = data["section"]
        session_id = data["session"]
        user_id = data["user"]
        group_id = data["group"]
        context = data["context"]

        concept_map_log = knowledgevis_models.ConceptMappingLog(user=User.objects.get(id=user_id),
                                           group=reader_models.Group.objects.get(id=group_id),
                                           session=session_id, section= section_id,
                                           action=action, context=context)

        concept_map = knowledgevis_models.ConceptMap(user=User.objects.get(id=user_id),
                                           group=reader_models.Group.objects.get(id=group_id),
                                           session=session_id, section=section_id,
                                           structure=concept_map, context=context)

        concept_map_log.save()
        concept_map.save()
        return JSONResponse({"tracked": True}, status=201)
    else:
        return HttpResponseForbidden()

@csrf_exempt
def assignments(request):
    """
    Returning all the assignments assigned to a certain student in a group
    """
    if request.method == 'GET':
        user_id = request.GET["user"]
        group_id = request.GET["group"]
        #Get assignments that the student in the context of that group has to submit
        assignments = []
        assignments_results = reader_models.Assignment.objects.filter(user=user_id, group=reader_models.Group.objects.get(id=group_id))

        assignments_json = {}
        if len(assignments_results)>0:
            for assignment in assignments_results:
                assignments.append(model_to_dict(assignment))

        assignments_json["result"] = True
        assignments_json["assignments"] = assignments

        #return JSONResponse({"quiz":quiz.id, "name": quiz.name, "questions": questions_json}, status=201)
        return JSONResponse(assignments_json, status=201)

    else:
        return HttpResponseForbidden()

@csrf_exempt
def rate_resource(request):
    """
    Log when a student rate a recommended resource
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data["user"]
        group_id = data["group"]
        session_id = data["session"]
        section = data["section"]
        page = data["page"]
        res_id = data["res_id"]
        rating = data["rating"]
        type = data["type"]
        datetime = data["datetime"]
        explanation = data["explanation"]
        extra = data["extra"]

        rating_log = rec_models.Rating(value=rating, explanation=explanation, user=User.objects.get(id=user_id), group=reader_models.Group.objects.get(id=group_id), session=session_id, datetime=datetime, section=section, page=page, type=type, resource=rec_models.Resource(id=res_id),extra=extra)
        rating_log.save()
        return JSONResponse({"tracked":True}, status=201)
    else:
        return HttpResponseForbidden()

@csrf_exempt
def recommendations_ratings(request):
    """
       Return all the ratings a specific user have done for recommended resources of a certain section_id
       """
    if request.method == 'GET':
        user_id = request.GET["user"]
        group_id = request.GET["group"]
        section_id = request.GET["section"]

        # Get rated recommended resources
        ratings = rec_models.Rating.objects.filter(user=user_id, group=reader_models.Group.objects.get(id=group_id), section=section_id).annotate(max_date=Max('resource__rating__datetime')).filter(date=F('max_date'))

        ratings_json = {}
        if len(ratings) > 0:
            #concept_map = concept_map_results.latest("datetime")
            ratings_json["result"] = True
            #concept_map_json["conceptMap"] = concept_map.structure
        else:
            ratings_json["result"] = False

        # return JSONResponse({"quiz":quiz.id, "name": quiz.name, "questions": questions_json}, status=201)
        return JSONResponse(ratings_json, status=201)

    else:
        return HttpResponseForbidden()
