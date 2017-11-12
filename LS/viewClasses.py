class teacherClass:
	def __init__(self, object):
		self.name = object[0]
		self.contact_no = object[1]
		self.salary = object[2]
		self.subjects = object[3]
		self.id = object[4]
		self.start_year = object[5]
		self.image = object[6]


class subjectClass:
	def __init__(self, object):
		self.title = object[0]
		self.incharge = object[1]
		self.id = object[2]


class newsClass:
	def __init__(self, object):
		self.id = object[0]
		self.heading = object[1]
		self.link = object[2]
		self.timestamp = object[3]



class nurseClass:
	def __init__(self, object):
		self.name = object[0]
		self.start_year = object[1]
		self.contact_no = object[2]
		self.id = object[3]
		self.salary = object[4]
		self.image = object[5]
		self.s_a = object[6]


class doctorClass:
	def __init__(self, object):
		self.name = object[0]
		self.specialisation = object[1]
		self.start_year = object[2]
		self.contact_no = object[3]
		self.id = object[4]
		self.salary = object[5]
		self.image = object[6]
		self.s_a = object[7]

class donorClass:
	def __init__(self, object):
		self.username = object[0]
		self.first_name = object[1]
		self.last_name = object[2]
		self.email = object[3]
		self.contact_no = object[4]
		self.PAN = object[5]


class donationCLass:
	def __init__(self, object):
		self.amount = object[0]
		self.first_name = object[1]
		self.last_name = object[2]

class ecClass():
	"""docstring for ecClass"""
	def __init__(self, object):
		self.name = object[0]
		self.post = object[1]	
		self.id = object[2]	
		self.image = object[3]


class studentClass():
	"""docstring for studentClass"""
	def __init__(self, object):
		self.name = object[1]
		self.major_disability = object[3]
		self.address = object[2]
		self.father_name = object[4]
		self.mother_name = object[5]
		self.contact_no = object[6]
		self.id = object[0]
		self.doctor = object[7]
		self.nurse = object[8]
		

class nstaffClass():
	"""docstring for nstaffClass"""
	def __init__(self,object):
		self.ns_id = object[0]
		self.name = object[1]
		self.designation = object[2]
		self.salary = object[3]
		self.start_year = object[4]
		self.contact_no = object[5]
		self.isadmin = object[6]
		self.image = object[7]
		


