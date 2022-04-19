import os
import django

from django.contrib.auth.hashers import make_password
from django.utils.timezone import datetime  # important if using timezones

import csv
import json

from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


from bs4 import BeautifulSoup

from django.db import IntegrityError

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ereader.settings")
django.setup()

from recommender import models as rec_models

def jaccard_similarity(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def extract_text_from_local_html(html_path):
    soup = BeautifulSoup(open(html_path), "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def extract_text_from_txt(txt_path):
    file = open(txt_path, "r")
    return file.read()


PATH_FOLDER_CONCEPTS = "/Users/pawsres1/Documents/educational_videos/videos"
PATH_PAGES = "/Users/pawsres1/django_apps/ereader/reader/static/resources"
PATH_SECTIONS = "/Users/pawsres1/django_apps/ereader/reader/static/resources"

books = ["iir"]
reading_id = "iir"

loaded_videos = {}

if __name__ == '__main__':

    option = input("What action do you want to perform? [1: load new videos into database (and update the existing ones), 2: calculate similarities between videos and pages, 3 calculate similarities between videos and sections]: ")

    reading_id = "iir"

    if option==1:
        for results_folder in os.listdir(PATH_FOLDER_CONCEPTS):
            #if reading_id in results_folder: #I deleted this because there are new videos from outside iir video collection
            if results_folder!=".DS_Store":
                videos_list = []
                print "Processing videos in "+results_folder+" ..."
                for video_filename in os.listdir(PATH_FOLDER_CONCEPTS+"/" + results_folder + "/"):
                    if video_filename!=".DS_Store" and "summary_video_collection" not in video_filename:
                        video_title = video_filename
                        json_video = open(PATH_FOLDER_CONCEPTS+"/" + results_folder + "/" + video_title + "/" + video_title + ".info.json")
                        data_video = json.load(json_video)
                        data_video["sections"] = [results_folder]
                        video_obj = {"type": "video", "title": data_video["fulltitle"], "url": data_video["webpage_url"], "info_json": data_video, "length": data_video["duration"]}
                        videos_list.append(video_obj)

                for video in videos_list:
                    video_exists = rec_models.Resource.objects.filter(url=video["url"]).exists()
                    if video_exists:
                        print(video["title"]+" exists")
                        db_video = rec_models.Resource.objects.get(url=video["url"])
                        video_info_json = db_video.info_json
                        section = video["info_json"]["sections"][0]
                        current_sections = video_info_json["sections"]
                        length = db_video.length
                        if length == 0:
                            print("It has 0 length")
                            db_video.length = video["length"]
                            db_video.save()
                        # if section not in current_sections:
                        #     video_info_json["sections"].append(section)
                        #     db_video.info_json = video_info_json
                        #     db_video.save()
                        # if "transcript" in video_info_json.keys():
                        #     current_transcript = video_info_json["transcript"]
                        #     if "transcript" in video["info_json"].keys():
                        #         transcript = video["info_json"]["transcript"]
                        #
                        #         if current_transcript != transcript:
                        #             video_info_json["transcript"]=transcript
                        #             db_video.info_json = video_info_json
                        #             db_video.save()
                    else:
                        try:
                            rec_models.Resource(
                                type=video["type"],
                                title=video["title"],
                                url=video["url"],
                                info_json=video["info_json"],
                                length=video["length"]
                            ).save()
                        except IntegrityError:
                            continue
    elif option==2:
        # Bring in standard stopwords
        stopWords = stopwords.words('english')

        text_pages = {}

        for book in books:
            for page in os.listdir(PATH_PAGES + "/" + book + "/"):
                print page

                # Extract the text from page
                page_text = extract_text_from_local_html(PATH_PAGES + "/" + book + "/" + page)

                print page_text
                print "################################"
                text_pages[page] = page_text

        video_set = rec_models.Resource.objects.filter(type="video")
        for video in video_set.iterator():
            print video.title
            video_json = video.info_json
            video_text = video.title
            if "transcript" in video_json.keys():
                video_text = video_text + " " + video_json["transcript"]
            else:
                video_text = video_text + " " + video_json["description"] + " " + " ".join(video_json["tags"])
            print video_text
            print "---------------------------------------"
            max_cosine_sim = 0
            max_doc_sim = ""
            for book in books:
                for page in os.listdir(PATH_PAGES+"/"+book+"/"):
                    page_id = page[0:page.index(".")]
                    print page_id

                    #Extract the text from page
                    page_text = text_pages[page]

                    # Set up the vectoriser, passing in the stop words
                    tfidf_vectorizer = TfidfVectorizer(stop_words=stopWords)

                    # Apply the vectoriser to the training set
                    tfidf_matrix_train = tfidf_vectorizer.fit_transform([page_text,video_text])

                    cosine_sim = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train).item(1)

                    try:
                        rec_models.Similarity(
                            resource_id = video,
                            id_textual_resource = page_id,
                            type = "cosine",
                            value = cosine_sim
                        ).save()
                    except IntegrityError:
                        continue

                    if cosine_sim>max_cosine_sim:
                        max_cosine_sim = cosine_sim
                        max_doc_sim = page_text
            print "Max similarity for video: "+video.title
            print max_cosine_sim
            print max_doc_sim
            print "++++++++++++++++++++++++++"

    elif option==3:

        #initialize the Lemmatizer
        lemmatizer = WordNetLemmatizer()

        # Bring in standard stopwords
        stopWords = stopwords.words('english')

        text_sections = {}

        for book in books:
            for section in os.listdir(PATH_SECTIONS + "/" + book + "_sections_text/"):
                if section!=".DS_Store":
                    section_id = section[0:section.index(".html")]
                    section_id = section_id.replace("_", "-")
                    # Extract the text from page
                    section_text = extract_text_from_txt(PATH_PAGES + "/" + book + "_sections_text/" + section)
                    #Remove stopwords from section text
                    section_text = section_text.lower()
                    section_text = ' '.join([word for word in section_text.split() if word not in stopWords])
                    text_sections[section_id] = lemmatizer.lemmatize(section_text)

        video_set = rec_models.Resource.objects.filter(type="video")

        for video in video_set.iterator():
            #print video.title
            video_json = video.info_json
            video_text = video.title
            if "transcript" in video_json.keys():
                video_text = video_text + " " + video_json["transcript"]
            else:
                video_text = video_text + " " + video_json["description"] + " " + " ".join(video_json["tags"])
            #print video_text
            #Remove stopwords from video text
            video_text = video_text.lower()
            video_text = ' '.join([word for word in video_text.split() if word not in stopWords])
            video_text_lemmatized = lemmatizer.lemmatize(video_text)
            #print "---------------------------------------"
            max_sim = 0
            max_doc_sim = ""
            for book in books:
                for section in os.listdir(PATH_PAGES+"/"+book+"_sections_text/"):
                    if section!=".DS_Store":
                        section_id = section[0:section.index(".html")]
                        section_id = section_id.replace("_", "-")

                        #Extract the text from page
                        #section_text = text_sections[section_id]
                        section_text_lemmatized = text_sections[section_id]

                        # Set up the vectoriser, passing in the stop words
                        #tfidf_vectorizer = TfidfVectorizer(stop_words=stopWords)

                        # Apply the vectoriser to the training set
                        #tfidf_matrix_train = tfidf_vectorizer.fit_transform([section_text_lemmatized, video_text_lemmatized])

                        #cosine_sim = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train).item(1)
                        #sim = cosine_sim

                        #print(video_text_lemmatized)
                        #print("~~~~~~~~")
                        #print(section_text_lemmatized)

                        jaccard_sim = jaccard_similarity(video_text_lemmatized,section_text_lemmatized)
                        sim = jaccard_sim
                        try:
                            rec_models.Similarity(
                                resource_id = video,
                                id_textual_resource = "section-"+section_id,
                                #type = "cosine",
                                #type = "cosine_tfidf_lemmatized",
                                type="jaccard_lemmatized",
                                value = sim
                            ).save()
                        except IntegrityError:
                            continue

                        if sim>max_sim:
                            max_sim = sim
                            max_doc_sim = section_text_lemmatized
            print "Max sim for "+video.title
            print max_sim
            print max_doc_sim[0:100]
            print "+++++++++++++"





