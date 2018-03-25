from django.shortcuts import render
import os
import subprocess
import json
from django.http import Http404
from django.http import HttpResponse

# Create your views here.
def get_recommendations(request,search_string,domain):
    course_json = Course.objects.get(id=course_id)
    return render(request, 'reader.html', {"course":course_json})


def panel(request):
    query = " likelihood ratio"
    topic = " information retrieval"
    # result = subprocess.check_output("java -jar search_engine.jar " + topic + query, cwd='./recommender/')
    result = subprocess.check_output(["java", "-jar", "search_engine.jar", topic, query], cwd='./recommender')

    table = json.loads(result)

    # cope with empty input
    # cope with encoding other than utf-8
    content = ""
    for key in table:
        title = table[key]['metadata']['title']
        id = table[key]['metadata']['id']
        description = table[key]['metadata']['description']
        tags = table[key]['metadata']['tags']
        if "subtitles" in table:
            subtitle = table[key]['subtitles']
        content += "<p><iframe width = '1000' height = '750' src='https://www.youtube.com/embed/" + id + "'> </iframe></p>"
    response = HttpResponse("The returned string is: " + content)

    return response
    # raise Http404("content is not yet finished")
