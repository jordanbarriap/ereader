from django.shortcuts import render

# Create your views here.
def get_recommendations(request,search_string,domain):
    course_json = Course.objects.get(id=course_id)
    return render(request, 'reader.html', {"course":course_json})