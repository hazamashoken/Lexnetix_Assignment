from ninja import Schema, ModelSchema
from ninja.orm import create_schema
from lexnetic_school.models import Class, Student, Teacher, School, HeadMaster, PersonalInfo, Member

######################
#   Wrapper Schemas  #
######################

class ErrorOut(Schema):
	detail: str

class OkOut(Schema):
	detail: str
	username: str = None
	model: ModelSchema

######################
# Schemas for input  #
######################

class PersonalInfoIn(ModelSchema):
	class Config:
		model = PersonalInfo
		model_fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone', 'address']

class SchoolIn(ModelSchema):
	class Config:
		model = School
		model_fields = ['name', 'address', 'phone', 'email', 'website']

class MemberIn(Schema):
	school_id: int
	personal_info: PersonalInfoIn

class HeadMasterIn(Schema):
	school_id: int
	username: str = None
	personal_info: PersonalInfoIn

class TeacherIn(Schema):
	school_id: int
	username: str = None
	personal_info: PersonalInfoIn

class StudentIn(Schema):
	school_id: int
	username: str = None
	class_id: int
	intake_year: int
	personal_info: PersonalInfoIn

class HeadMasterPut(Schema):
	school_id: int
	personal_info: PersonalInfoIn

class TeacherPut(Schema):
	school_id: int
	personal_info: PersonalInfoIn

class StudentPut(Schema):
	school_id: int
	personal_info: PersonalInfoIn

class ClassIn(ModelSchema):
	teacher_id: int
	school_id: int
	class Config:
		model = Class
		model_fields = ['year']


######################
# Schemas for output #
######################

class PersonalInfoOut(ModelSchema):
	class Config:
		model = PersonalInfo
		model_fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone', 'address']

class MemberOut(ModelSchema):
	class Config:
		model = Member
		model_fields = ['id', 'school', 'username']
	username: str = None
	role: str
	personal_info: PersonalInfoOut

	@staticmethod
	def resolve_personal_info(obj):
		return obj.personal_info

	@staticmethod
	def resolve_role(obj):
		return obj.get_role_display()


class StudentOut(ModelSchema):
	class Config:
		model = Student
		model_fields = ['id', 'intake_year']
	class_id: int
	personal_info: PersonalInfoOut

	@staticmethod
	def resolve_personal_info(obj):
		if obj.member:
			return obj.member.personal_info

	@staticmethod
	def resolve_class_id(obj):
		if obj.f_class:
			return obj.f_class.id

class TeacherOut(ModelSchema):
	class Config:
		model = Teacher
		model_fields = ['id']
	personal_info: PersonalInfoOut

	@staticmethod
	def resolve_personal_info(obj):
		if obj.member:
			return obj.member.personal_info

class ClassOut(ModelSchema):
	class Config:
		model = Class
		model_fields = '__all__'
	teachers: TeacherOut = None
	students: list[StudentOut] = None

	@staticmethod
	def resolve_teachers(obj):
		if obj.teacher:
			return obj.teacher

	@staticmethod
	def resolve_students(obj):
		return [student for student in Student.objects.all() if student.f_class.id == obj.id]

class HeadMasterOut(ModelSchema):
	school_id: int = None
	class Config:
		model = HeadMaster
		model_fields = ['id']
	personal_info: PersonalInfoOut

	@staticmethod
	def resolve_school_id(obj):
		if obj.school:
			return obj.school.id

	@staticmethod
	def resolve_personal_info(obj):
		if obj.member:
			return obj.member.personal_info

class SchoolOut(ModelSchema):
	class Config:
		model = School
		model_fields = '__all__'
	head_master: HeadMasterOut = None
	classes: list[ClassOut] = None

	@staticmethod
	def resolve_head_master(obj):
		for head_master in HeadMaster.objects.all():
			if head_master.school.id == obj.id:
				return head_master

	@staticmethod
	def resolve_classes(obj):
		if obj.class_set:
			return obj.class_set.all()
