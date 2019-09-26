import os
import django 

from django.contrib.auth.hashers import make_password
from django.utils.timezone import datetime #important if using timezones
from django.db import IntegrityError

import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ereader.settings")
django.setup()

from django.contrib.auth.models import User

file_name = 'INFSCI_2140_IR_Student_list.csv'
row_count = 0
map_index_column = {}
users_list = []
with open(file_name, 'rb') as csvfile:
	users_reader= csv.reader(csvfile, delimiter=',')#, quotechar='|')
	for row in users_reader:
		if (row_count==0):
			for index in range(0,len(row)):
				map_index_column[index] = row[index] # row[index] -> column name 
		else:
			user = {}
			for index in range(0,len(row)):
				user[map_index_column[index]] = row[index]
			users_list.append(user)

		row_count = row_count + 1
	print users_list
		

try:
	User.objects.bulk_create([
	    User(
	        first_name=user['first_name'],
	        last_name=user['last_name'],
	        username=user['username'],
	        email=user['email'],
	        password=make_password(user['password']),
	        date_joined= datetime.now(),
	        is_active=True,
			is_staff=False,
	        is_superuser = False,
	    ) for user in users_list
	])
except IntegrityError:
    for user in users_list:
        try:
            User(
		        first_name=user['first_name'],
		        last_name=user['last_name'],
		        username=user['username'],
		        email=user['email'],
		        password=make_password(user['password']),
		        date_joined= datetime.now(),
		        is_active=True,
				is_staff=False,
		        is_superuser = False,
	    	).save()
        except IntegrityError:
            continue