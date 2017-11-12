# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.db import connection, IntegrityError, transaction
from datetime import datetime, date
from viewClasses import *
import re
import MySQLdb as db
import time
import datetime
from dateutil.tz import *
import pytz

db = db.connect("127.0.0.1","root","152Vj@138152","LS")

def write_file(data,filename):
	with open(filename,'wb') as f:
		f.write(data)

# Create your views here.
@csrf_protect
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('dashboard'))
	if request.POST:
		username = request.POST['username']
		password = request.POST.get('password')
		if username== '':
			return render(request, 'LS/login.html')
		cursor = db.cursor()
		cursor.execute("SELECT * from auth_user where username='"+username+"';")
		db.commit()
		data = cursor.fetchall()
		if data is not None:				# Check if user is registered
			user = auth.authenticate(username=username, password=password)			# Authenticates the username and password
			if user is not None:
				auth.login(request, user)											# Logs in
				return HttpResponseRedirect(reverse('dashboard'))
			else:																	# User exists but password is incorrect
				messages.error(request, 'The username and password combination is incorrect.')
		else:
			messages.error(request, 'ID not registered.')
	return render(request, 'LS/login.html')

@csrf_protect
def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('dashboard'))
	#flag = 0
	if request.POST:
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		address = request.POST['address']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']
		email = request.POST['email']
		contact_no = request.POST['contact_no']
		PAN = request.POST['PAN']
		#flag=1

		match = re.search(r'[\w.-]+@[\w-]+\.[\w.-]+', email)
		panbool = re.search(r'[A-Z]+[A-Z]+[A-Z]+[A-Z]+[A-Z]+\d+\d+\d+\d+[A-Z]', PAN)
		contact_bool = re.search(r'^[0-9]{10}',contact_no)
		cursor = db.cursor()
		username = str(username)
		#print username
		cursor.execute("SELECT * from auth_user where username = '"+username+"';")
		db.commit()
		data = cursor.fetchall()
		cursor.execute("SELECT * from auth_user where email = '"+email+"';")
		db.commit()
		data2 = cursor.fetchall()
		#print data
		if len(data) != 0:
			messages.error(request, 'username already taken')
		elif len(data2) != 0:
			messages.error(request, 'Email ID already registered')
		elif pass1 != pass2:
			messages.error(request, 'Passwords do not match.')
		elif not match:
			messages.error(request, 'Invalid Email ID.')
		elif username == '':
			messages.error(request, 'username cannot be left blank.')
		elif not panbool:
			messages.error(request, 'Invalid PAN number.')
		elif not contact_bool:
			messages.error(request,'Invalid contact number.')
		else:
			cursor = db.cursor()
			#cursor.execute("INSERT into auth_user(username,first_name,last_name,password,email,is_staff,is_active,) values('"+username+"','"+first_name+"','"+last_name+"','"+pass1+"','"+email+"') ")
			user = User.objects.create_user(username, email, pass1)
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			cursor = db.cursor()
			cursor.execute("SELECT * from auth_user;")
			db.commit()
			data = cursor.fetchall()
			userid = data[-1][0]
			userid = str(userid)
			cursor.execute("INSERT into donor values('"+PAN+"','"+contact_no+"','"+userid+"','"+address+"');")
			db.commit()
			messages.success(request,"User successfully registered.")
			return HttpResponseRedirect(reverse('dashboard'))
	return render(request, 'LS/register.html') 


def home(request):
	cursor = db.cursor()
	cursor.execute("SELECT ne_id,heading,link,timestamp from news order by timestamp desc;")
	db.commit()
	data = cursor.fetchall()
	if len(data) > 5:
		data = data[:5]
	news = []
	for i in data:
		news.append(newsClass([i[0],i[1],i[2],i[3]]))

	cursor = db.cursor()
	cursor.execute("SELECT d.amount,a.first_name,a.last_name from donation as d,auth_user as a order by d.timestamp desc")
	db.commit()
	data = cursor.fetchall()
	if len(data) > 5:
		data = data[:5]
	donation = []
	for i in data:
		donation.append(donationClass([i[0],i[1],i[2]]))

	details = {'news':news, 'donation':donation}
	return render(request, 'LS/home.html', details)


def ec(request):
	if request.POST:
		delete = request.POST['id']
		if delete  == "0":
			staffid = request.POST['staffid']
			stafftype = request.POST['type']
			post = request.POST['post']
			if stafftype == "teacher":
				cursor = db.cursor()
				cursor.execute("SELECT * FROM teacher WHERE t_id = '"+staffid+"';")
				db.commit()
				data = cursor.fetchall()
				cursor = db.cursor()
				cursor.execute("SELECT * from ecommittee where th_id = '"+staffid+"';")
				db.commit()
				data1 = cursor.fetchall()
				if len(data) == 0:
					messages.error(request,"Invalid teaching staff id")
				elif len(data1) !=0:
					messages.error(request,"Already a member")
				else:
					cursor = db.cursor()
					cursor.execute("INSERT into ecommittee(post,th_id) values('"+post+"','"+staffid+"')")
					db.commit()
					messages.success(request,"Successfully added member.")
			elif stafftype == "doctor":
				cursor = db.cursor()
				cursor.execute("SELECT * FROM doctor WHERE d_id = '"+staffid+"';")
				db.commit()
				data = cursor.fetchall()
				cursor = db.cursor()
				cursor.execute("SELECT * from ecommittee where dt_id = '"+staffid+"';")
				db.commit()
				data1 = cursor.fetchall()
				if len(data) == 0:
					messages.error(request,"Invalid doctor id")
				elif len(data1) !=0:
					messages.error(request,"Already a member")
				else:
					cursor = db.cursor()
					cursor.execute("INSERT into ecommittee(post,dt_id) values('"+post+"','"+staffid+"')")
					db.commit()
					messages.success(request,"Successfully added member.")
			elif stafftype == "nontechnical":
				cursor = db.cursor()
				cursor.execute("SELECT * FROM nontechnicalstaff WHERE t_id = '"+staffid+"';")
				db.commit()
				data = cursor.fetchall()
				cursor = db.cursor()
				cursor.execute("SELECT * from ecommittee where ntf_id = '"+staffid+"';")
				db.commit()
				data1 = cursor.fetchall()
				if len(data) == 0:
					messages.error(request,"Invalid teaching staff id")
				elif len(data1) !=0:
					messages.error(request,"Already a member")
				else:
					cursor = db.cursor()
					cursor.execute("INSERT into ecommittee(post,ntf_id) values('"+post+"','"+staffid+"')")
					db.commit()
					messages.success(request,"Successfully added member.")
		else:
			cursor = db.cursor()
			cursor.execute("DELETE from ecommittee where e_id = '"+delete+"';")
			db.commit()
			messages.success(request,"Successfully deleted member.")

	cursor = db.cursor()
	cursor.execute("select * from ecommittee;")
	records = []
	data = cursor.fetchall()
	for i in data:
		if i[2] is not None:
			cursor = db.cursor()
			p = i[2]
			p = str(p)
			cursor.execute("SELECT * from nontechnicalstaff where ns_id='"+p+"'")
			db.commit()
			data1 = cursor.fetchall()
			if len(data1)!=0:
				for j in data1:
					img = "./temp/nsf_img"+str(j[0])+".jpg"
					records.append(ecClass([j[1],i[1],i[0]]))
		elif i[3] is not None:
			cursor = db.cursor()
			p = i[3]
			p = str(p)
			cursor.execute("SELECT * from doctor where d_id = '"+p+"';")
			db.commit()
			data1 = cursor.fetchall()
			if len(data1)!=0:
				for j in data1:
					img = "./temp/doctor_img"+str(j[0])+".jpg"
					records.append(ecClass([j[1],i[1],i[0],img]))
		elif i[4] is not None:
			cursor = db.cursor()
			p = i[4]
			p = str(p)
			cursor.execute("SELECT * from teacher where t_id = '"+p+"';")
			db.commit()
			data1 = cursor.fetchall()
			if len(data1)!=0:
				for j in data1:
					img = "./temp/teacher_img"+str(j[0])+".jpg"
					records.append(ecClass([j[1],i[1],i[0],img]))
	return render(request, 'LS/ExecutiveCommittee.html',{'members':records})

@csrf_protect
def medical(request):
	if request.POST:
		delete = request.POST['id']
		if delete == '0':
			name = request.POST['name']
			salary = request.POST['salary']
			start_year = request.POST['start_year']
			contact_no = request.POST['contact_no']
			stafftype = request.POST['type']
			specialisation = request.POST['specialisation']
			image = request.FILES['image'].read()
			contact_bool = re.search(r'^[0-9]{10}',contact_no)
			#salary = re.search(r'^')
			cursor = db.cursor()
			cursor.execute("SELECT * from doctor where contact_no = '"+contact_no+"' and name = '"+name+"' and salary = '"+salary+"' and start_year = '"+start_year+"' and specialisation = '"+specialisation+"';")
			db.commit()
			data = cursor.fetchall()
			cursor.execute("SELECT * from nurse where contact_no = '"+contact_no+"' and name = '"+name+"' and salary = '"+salary+"' and start_year = '"+start_year+"';")
			db.commit()
			data2 = cursor.fetchall()
			if len(data) != 0 or len(data2) != 0:
				messages.error(request,"Staff already registered.")
			elif not contact_bool:
				messages.error(request,"Invalid contact number.")
			elif stafftype == 'doctor':
				cursor.execute("INSERT into doctor(name,specialisation,salary,start_year,contact_no) values('"+name+"','"+specialisation+"','"+salary+"','"+start_year+"','"+contact_no+"');")
				db.commit()
				try:
					cursor = db.cursor()
					cursor.execute("SELECT * FROM doctor")
					db.commit()
					data = cursor.fetchall()
					write_file(str(image),'./LS/static/temp/doctor_img'+str(data[-1][0])+'.jpg')
				except:
					pass
				messages.success(request,"Doctor profile successfully added.")
			elif stafftype == "nurse":
				cursor.execute("INSERT into nurse(name,salary,start_year,contact_no) values('"+name+"','"+salary+"','"+start_year+"','"+contact_no+"');")
				db.commit()
				try:
					cursor = db.cursor()
					cursor.execute("SELECT * FROM nurse")
					db.commit()
					data = cursor.fetchall()
					write_file(str(image),'./LS/static/temp/nurse_img'+str(data[-1][0])+'.jpg')
				except:
					pass
				messages.success(request,"Nurse profile successfully added.")
		else:
			stype = request.POST['ss']
			if stype != "":
				cursor = db.cursor()
				cursor.execute("SELECT * FROM student where dc_id = '"+str(delete)+"';")
				db.commit()
				data = cursor.fetchall()
				# cursor = db.cursor()
				# cursor.execute("SELECT specialisation FROM doctor where d_id = '"+str(delete)+"';")
				# db.commit()
				# data1 = cursor.fetchall()
				cursor = db.cursor()
				cursor.execute("DELETE FROM ecommittee where dt_id = '"+str(delete)+"';")
				db.commit()
				cursor = db.cursor()
				cursor.execute("DELETE FROM doctor where d_id = '"+str(delete)+"';")
				db.commit()
				for i in data:
					cursor = db.cursor()
					cursor.execute("SELECT * FROM doctor where specialisation = '"+str(i[3])+"' order by s_a, start_year desc;")
					db.commit()
					data1 = cursor.fetchall()
					if len(data1)!=0:
						cursor = db.cursor()
						cursor.execute("update student set dc_id = '"+str(data1[0][0])+"' where s_id = '"+str(i[0])+"';")
						db.commit()
						cursor = db.cursor()
						cursor.execute("update doctor set s_a = s_a +1 where dc_id = '"+str(data1[0][0])+"';")
						db.commit()
				messages.success(request,"Doctor profile successfully deleted.")
			else:
				cursor = db.cursor()
				cursor.execute("SELECT * FROM student where nu_id = '"+str(delete)+"';")
				db.commit()
				data = cursor.fetchall()
				cursor = db.cursor()
				cursor.execute("delete from nurse where n_id = '"+str(delete)+"';")
				db.commit()
				for i in data:
					cursor = db.cursor()
					cursor.execute("select * from nurse order by s_a, start_year desc;")
					db.commit()
					data1 = cursor.fetchall()
					if len(data1) != 0:
						cursor = db.cursor()
						cursor.execute("update student set nu_id = '"+str(data1[0][0])+"' where s_id = '"+str(i[0])+"';")
						db.commit()
						cursor = db.cursor()
						cursor.execute("update nurse set s_a = s_a +1 where nu_id = '"+str(data1[0][0])+"';")
						db.commit()
				messages.success(request,"Nurse profile successfully deleted.")
	cursor = db.cursor()
	cursor.execute("SELECT name,start_year,contact_no,n_id,salary,s_a FROM nurse order by start_year")
	db.commit()
	data = cursor.fetchall()
	nurse = []
	for i in data:
		img = "./temp/nurse_img"+str(i[3])+".jpg"
		nurse.append(nurseClass([i[0],i[1],i[2],i[3],i[4],img,i[5]]))

	cursor = db.cursor()
	cursor.execute("SELECT name,specialisation,start_year,contact_no,d_id,salary,s_a FROM doctor order by start_year")
	db.commit()
	data = cursor.fetchall()
	doctor = []
	for i in data:
		img = "./temp/doctor_img"+str(i[4])+".jpg"
		doctor.append(doctorClass([i[0],i[1],i[2],i[3],i[4],i[5],img,i[6]]))

	details = {'nurse':nurse, 'doctor':doctor}	
	return render(request, 'LS/MedicalStaff.html', details)

@csrf_protect
def teaching(request):
	if request.POST:
		delete  = request.POST['id']
		if delete == '0':
			name = request.POST['name']
			salary = request.POST['salary']
			start_year = request.POST['start_year']
			contact_no = request.POST['contact_no']
			image = request.FILES['image'].read()
			print image
			cursor = db.cursor()
			cursor.execute("SELECT * from teacher where contact_no = '"+contact_no+"' and name = '"+name+"' and salary = '"+salary+"' and start_year = '"+start_year+"';")
			db.commit()
			data = cursor.fetchall()
			if len(data) != 0:
				messages.error(request,"Teacher already registered.")
			else:
				cursor.execute("INSERT into teacher(name,salary,start_year,contact_no,image) values(%s,%s,%s,%s,%s);",(str(name),str(salary),str(start_year),str(contact_no),str(image) ))
				db.commit()

				cursor = db.cursor()
				cursor.execute("SELECT * FROM teacher")
				db.commit()
				data1 = cursor.fetchall()

				cursor = db.cursor()
				cursor.execute("SELECT * FROM student")
				db.commit()
				data = cursor.fetchall()
				for i in data:
					cursor = db.cursor()
					cursor.execute("INSERT INTO student_teacher values('"+str(i[0])+"','"+str(data1[-1][0])+"');")
					db.commit()
				try:
					cursor = db.cursor()
					cursor.execute("SELECT * FROM teacher")
					db.commit()
					data = cursor.fetchall()
					write_file(str(image),'./LS/static/temp/teacher_img'+str(data[-1][0])+'.jpg')
				except:
					pass
				messages.success(request,"Teacher profile successfully added.")
		else:
			cursor = db.cursor()
			cursor.execute("DELETE from student_teacher where te_id = '"+delete+"';")
			db.commit()
			cursor = db.cursor()
			cursor.execute("DELETE from ecommittee where th_id = '"+delete+"';")
			db.commit()
			cursor = db.cursor()
			cursor.execute("DELETE from subject where tr_id = '"+delete+"';")
			db.commit()
			cursor = db.cursor()
			cursor.execute("DELETE from teacher where t_id = '"+delete+"';")
			db.commit()
			messages.success(request,"Teacher profile successfully deleted.")
	cursor = db.cursor()
	cursor.execute("SELECT t_id,name,contact_no,salary,start_year,image FROM teacher order by start_year")
	db.commit()
	data = cursor.fetchall()
	teachers = []
	#print data
	for i in data:
		cursor.execute("SELECT title FROM subject where tr_id='"+str(i[0])+"';")
		db.commit()
		subjects = cursor.fetchall()
		final = []
		for j in subjects:
			final.append(j[0])
		#print i[6]
		#i.append("./temp/img"+str(i[0])+".jpg")
		#print i[6]
		#pagal
		img = "./temp/teacher_img"+str(i[0])+".jpg"
		teachers.append(teacherClass([i[1],i[2],i[3],final,i[0],i[4],img]))
	details = {'teachers':teachers}
	#details = {'t_id':data[0], 'name':data[1], 'salary':data[2], 'start_year':data[3], 'contact_no':data[4], 'image':data[5]}
	return render(request, 'LS/TeachingStaff.html', details)

@csrf_protect
def news(request):
	if request.POST:
		delete = request.POST['id']
		if delete == "0":
			heading = request.POST['heading']
			link = request.POST['link']
			nsf_id = request.POST['nsf_id']
			#timestamp = datetime.datetime.now()
			tz = pytz.timezone('Asia/Kolkata')
			timestamp = datetime.datetime.now(tz)
			timestamp = str(timestamp)
			timestamp = timestamp[0:timestamp.index('.')]
			cursor = db.cursor()
			cursor.execute("SELECT * from nontechnicalstaff where ns_id = '"+nsf_id+"';")
			db.commit()
			data = cursor.fetchall()
			cursor.execute("SELECT * from news where heading = '"+heading+"' and link = '"+link+"';")
			db.commit()
			data2 = cursor.fetchall()
			if len(data) == 0:
				messages.error(request,"Invalid staff ID.")
			elif len(data2) != 0: 
				messages.error(request,"News item already added.")
			elif data[0][6]==0:
				messages.error(request,"Staff not admin, hence cannot add news item")
			else:
				cursor.execute("INSERT into news(heading,link,timestamp,nsf_id) values('"+heading+"','"+link+"','"+timestamp+"','"+nsf_id+"');")
				db.commit()
				messages.success(request,"News item successfully added.")
		else:
			cursor = db.cursor()
			cursor.execute("DELETE FROM news WHERE ne_id = '"+delete+"';")
			db.commit()
			messages.success(request,"news item deleted.")

	cursor = db.cursor()
	cursor.execute("SELECT ne_id,heading,link,timestamp from news order by timestamp desc")
	db.commit()
	data = cursor.fetchall()
	news = []
	for i in data:
		news.append(newsClass([i[0],i[1],i[2],i[3]]))
	details = {'news':news}
	return render(request, 'LS/news.html',details)

@csrf_protect
def subjects(request):
	# if user is admin, in that case
	if request.POST:
		delete = request.POST['id']
		if delete == "0":
			title = request.POST['title']
			t_id = request.POST['t_id']
			cursor = db.cursor()
			cursor.execute("SELECT * from teacher where t_id = '"+t_id+"';")
			db.commit()
			data = cursor.fetchall()
			cursor.execute("SELECT * from subject where title = '"+title+"';")
			db.commit()
			data2 = cursor.fetchall()
			if len(data) == 0:
				messages.error(request,"Invalid Teacher ID.")
			elif len(data2) != 0: 
				messages.error(request,"Subject already added.")
			else:
				cursor.execute("INSERT into subject(title,tr_id) values('"+title+"','"+t_id+"');")
				db.commit()
				messages.success(request,"Subject successfully added.")
		else:
			cursor = db.cursor()
			cursor.execute("DELETE from student_subject where sb_id = '"+delete+"';")
			db.commit()
			cursor = db.cursor()
			cursor.execute("DELETE FROM subject WHERE su_id = '"+delete+"';")
			db.commit()
			messages.success(request,"Subject Deleted.")

	# retrieving data		
	cursor = db.cursor()
	db.commit()
	cursor.execute("SELECT s.title,t.name,s.su_id FROM subject as s, teacher as t where t.t_id = s.tr_id")
	db.commit()
	subjects = cursor.fetchall()
	data = []
	for subject in subjects:
		data.append(subjectClass([subject[0],subject[1],subject[2]]))
	details = {'subjects':data}
	return render(request, 'LS/subjects.html',details)

def donate(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	cursor = db.cursor()
	username = str(request.user.username)
	cursor.execute("SELECT a.username,a.first_name,a.last_name,a.email,d.ContactNo,d.PAN FROM auth_user as a,donor as d where a.id = d.userid and a.username = '"+username+"';")
	db.commit()
	data = cursor.fetchall()
	donors = []
	for i in data:
		donors.append(donorClass([i[0],i[1],i[2],i[3],i[4],i[5]]))
	details = {'donors':donors}
	return render(request, 'LS/donate.html',details)

def dashboard(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	if request.POST:
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']
		cursor = db.cursor()
		username = str(request.user.username)
		#print username
		cursor.execute("SELECT * from auth_user where username = '"+username+"';")
		db.commit()
		data = cursor.fetchall()
		#print data
		if pass1 != pass2:
			messages.error(request, 'Entered passwords do not match.')
		else:
			cursor = db.cursor()
			#cursor.execute("INSERT into auth_user(username,first_name,last_name,password,email,is_staff,is_active,) values('"+username+"','"+first_name+"','"+last_name+"','"+pass1+"','"+email+"') ")
			user = User.objects.get(username = username)
			user.set_password(str(pass1))
			user.save()
			messages.success(request,"Password changed successfully.")
			return HttpResponseRedirect(reverse('dashboard'))

	cursor = db.cursor()
	username = str(request.user.username)
	cursor.execute("SELECT a.username,a.first_name,a.last_name,a.email,d.ContactNo,d.PAN FROM auth_user as a,donor as d where a.id = d.userid and a.username = '"+username+"';")
	db.commit()
	data = cursor.fetchall()
	donors = []
	for i in data:
		donors.append(donorClass([i[0],i[1],i[2],i[3],i[4],i[5]]))
	cursor.execute("SELECT dn.amount,dn.timestamp from donation as dn,donor as dr where dr.userid = dn.dr_id order by dn.timestamp desc")
	db.commit()
	data = cursor.fetchall()
	donations = []
	for i in data:
		donations.append(donationClass([i[0],i[1]]))
	details = {'donors':donors,'donations':donations}
	return render(request, 'LS/dashboard.html',details)

def admin_student(request):
	if request.user.id != 1:
		return HttpResponseRedirect(reverse('home'))
	if request.POST:
		name = request.POST['name']
		address = request.POST['address']
		disability = request.POST['type']
		father_name = request.POST['father_name']
		mother_name = request.POST['mother_name']
		contact_no = request.POST['contact_no']
		dc_id = request.POST['dc_id']
		nu_id = request.POST['nu_id']
		cursor = db.cursor()
		cursor.execute("select * from student where name = '"+name+"' and contact_no = '"+contact_no+"' and father_name = '"+father_name+"' and mother_name = '"+mother_name+"';")
		db.commit()
		data = cursor.fetchall()
		if len(data) != 0:
			messages.error(request,"Student already registered.")
		else:
			cursor = db.cursor()
			cursor.execute("INSERT into student(name,address,major_disability,father_name,mother_name,contact_no,nu_id,dc_id) values('"+name+"','"+address+"','"+disability+"','"+father_name+"','"+mother_name+"','"+contact_no+"','"+nu_id+"','"+dc_id+"');")
			db.commit()
			cursor = db.cursor()
			cursor.execute("update doctor set s_a = s_a + 1 where d_id = '"+dc_id+"';")
			db.commit()
			cursor = db.cursor()
			cursor.execute("update nurse set s_a = s_a + 1 where n_id = '"+nu_id+"';")
			db.commit()
			cursor = db.cursor()
			cursor.execute("select * from student")
			db.commit()
			data = cursor.fetchall()
			s_id = data[-1][0]
			s_id = str(s_id)
			cursor = db.cursor()
			cursor.execute("select * from teacher")
			db.commit()
			datat = cursor.fetchall()
			for i in range(len(datat)):
				cursor = db.cursor()
				p = datat[i][0]
				p = str(p)
				cursor.execute("INSERT into student_teacher values('"+s_id+"','"+p+"');")
				db.commit()

			cursor = db.cursor()
			cursor.execute("select * from subject")
			db.commit()
			datat = cursor.fetchall()
			for i in range(len(datat)):
				cursor = db.cursor()
				p = datat[i][0]
				p = str(p)
				cursor.execute("INSERT into student_subject values('"+s_id+"','"+p+"');")
				db.commit()
			messages.success(request,"Student successfully registered.")

	cursor = db.cursor()
	cursor.execute("select * from doctor;")
	data = cursor.fetchall()
	disabilities = set()
	for i in data:
		disabilities.add(i[2])
	details = {'disabilities':disabilities}
	return render(request, 'LS/students.html',details)


def admin_nsf(request):
	if request.POST:
		delete = request.POST['id']
		if delete == "0":
			name = request.POST['name']
			salary = request.POST['salary']
			start_year = request.POST['start_year']
			contact_no = request.POST['contact_no']
			designation = request.POST['designation']
			image = request.FILES['image'].read()
			isadmin = request.POST['isadmin']
			cursor = db.cursor()
			cursor.execute("SELECT * from nontechnicalstaff where contact_no = '"+contact_no+"' and name = '"+name+"' and salary = '"+salary+"' and start_year = '"+start_year+"';")
			db.commit()
			data = cursor.fetchall()
			if len(data) != 0:
				messages.error(request,"Staff already registered.")
			else:
				cursor.execute("INSERT into nontechnicalstaff(name,salary,start_year,contact_no,designation,isadmin,image) values(%s,%s,%s,%s,%s,%s,%s);",(str(name),str(salary),str(start_year),str(contact_no),str(designation),str(isadmin),str(image) ))
				db.commit()
				try:
					cursor = db.cursor()
					cursor.execute("SELECT * FROM nontechnicalstaff")
					db.commit()
					data = cursor.fetchall()
					write_file(str(image),'./LS/static/temp/nsf_img'+str(data[-1][0])+'.jpg')
				except:
					pass
				messages.success(request,"Staff profile successfully added.")
		else:
			# cursor = db.cursor()
			# cursor.execute("delete from news where nsf_id = '"+delete+"';")
			# db.commit()
			cursor = db.cursor()
			cursor.execute("DELETE FROM nontechnicalstaff WHERE ns_id = '"+delete+"';")
			db.commit()
			messages.success(request,"Staff profile deleted.")


	cursor = db.cursor()
	cursor.execute("SELECT * FROM nontechnicalstaff")
	db.commit()
	data = cursor.fetchall()
	staff = []
	for i in data:
		img = "./temp/teacher_img"+str(i[0])+".jpg"
		staff.append(nstaffClass([i[0],i[1],i[2],i[3],i[4],i[5],i[6],img]))
	details = {'staff':staff}
	#details = {'t_id':data[0], 'name':data[1], 'salary':data[2], 'start_year':data[3], 'contact_no':data[4], 'image':data[5]}
	return render(request, 'LS/nsf.html', details)


@csrf_protect
def view_student(request):
	if request.POST:
		delete  = request.POST['id']
		cursor = db.cursor()
		cursor.execute("DELETE FROM student_teacher where sd_id = '"+delete+"';")
		cursor = db.cursor()
		cursor.execute("DELETE from student_subject where st_id = '"+delete+"';")
		cursor = db.cursor()
		cursor.execute("select dr.d_id,dr.name from doctor as dr,student as st where dr.d_id = st.dc_id and st.s_id = '"+str(delete)+"';")
		data_d = cursor.fetchall()
		cursor = db.cursor()
		cursor.execute("select ne.n_id,ne.name from nurse as ne,student as st where ne.n_id = st.nu_id and st.s_id = '"+str(delete)+"';")
		data_n = cursor.fetchall()
		cursor = db.cursor()
		if len(data_d)!=0:
			cursor.execute("update doctor set s_a = s_a - 1 where d_id = '"+str(data_d[0][0])+"';")
		cursor = db.cursor()
		if len(data_n)!=0:
			cursor.execute("update nurse set s_a = s_a - 1 where n_id = '"+str(data_n[0][0])+"';")
		cursor = db.cursor()
		cursor.execute("DELETE from student where s_id = '"+delete+"';")
		db.commit()
		messages.success(request,"Student Profile successfully deleted")

	students = []
	cursor = db.cursor()
	cursor.execute("SELECT * from student order by name")
	db.commit()
	details = []
	data = cursor.fetchall()
	if len(students)!=0:
		for i in students:
			details.append(studentClass(i))
	else:
		for i in data:
			cursor = db.cursor()
			cursor.execute("SELECT * from doctor where d_id = '"+str(i[8])+"'")
			db.commit()
			data1 = cursor.fetchall()
			cursor = db.cursor()
			cursor.execute("SELECT * from nurse where n_id = '"+str(i[7])+"'")
			db.commit()
			data2 = cursor.fetchall()
			nurse_name = "None"
			doctor_name = "None"
			if len(data2) != 0:
				nurse_name = str(data2[0][1])
			if len(data1) != 0:
				doctor_name = str(data1[0][1])	
			details.append(studentClass([i[0],i[1],i[2],i[3],i[4],i[5],i[6],doctor_name,nurse_name]))
	#details = {'students':students}
	return render(request,'LS/viewstudents.html',{'students':details})


def logout(request):
	if request.user.is_authenticated():
		auth.logout(request)
		messages.success(request, 'Successfully logged out.')
	return HttpResponseRedirect(reverse('login'))