from django.db import models
from admintion.querysets import (
    rooms_manager,groups_manager,students_manager,attendace_manager,teachers_manager, 
    parents_manager, payment_manager, group_students_manager, course_manager,lead_manager,
    task_manager, educenters_managers, common_managers,lead_forms_managers
)
from admintion.data import chooses
from user.data.chooses import COURSES_SEXES
from admintion.data.chooses import TASK_STATUS, TEACHER_TYPE, MESSAGE_TYPE,CONTACT_TYPES, MESSAGE_STATUS,EXAM_FORMAT,EXAM_TYPE
from admintion.validators import validate_file_size

class RoomImage(models.Model):
    image = models.ImageField(upload_to='user/',null=True,blank=True)
    room = models.ForeignKey('admintion.Room',on_delete=models.CASCADE,related_name='room_image',null=True,blank=True)

class Room(models.Model):
    title = models.CharField(max_length=50)
    capacity = models.PositiveSmallIntegerField()
    # images = models.ManyToManyField(RoomImage)
    status = models.BooleanField(default=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)

    rooms = rooms_manager.RoomManager()
    objects = models.Manager()

    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    duration_type = models.PositiveSmallIntegerField(choices=chooses.COURCE_DURATION_TYPES,blank=True,null=True)
    lesson_duration = models.CharField(max_length=50)
    lesson_duration_type = models.PositiveSmallIntegerField(choices=chooses.LESSON_DURATION_TYPES,blank=True,null=True)
    price = models.PositiveIntegerField()
    price_type = models.PositiveSmallIntegerField(choices=chooses.PRICE_TYPES,blank=True,null=True)
    comment = models.TextField()
    status = models.BooleanField(default=True)
    author = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)
    
    objects = models.Manager()
    courses = course_manager.CoursesManager()
    def __str__(self) -> str:
        return self.title


class Teacher(models.Model):
    teacer_type = models.BooleanField(default=False)
    user = models.ForeignKey('user.CustomUser',on_delete=models.CASCADE)
    status = models.BooleanField(default=True,null=True,blank=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)
    
    teachers = teachers_manager.TeacherManager()
    objects = models.Manager()

class GroupsDays(models.Model):
    days = models.PositiveSmallIntegerField(choices=chooses.GROUPS_DAYS)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)

class Group(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="group_teacher")
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    days = models.ManyToManyField(GroupsDays)
    pay_type = models.PositiveSmallIntegerField(choices=chooses.PAY_FORMS)
    status = models.PositiveSmallIntegerField(choices=chooses.GROUPS_STATUS)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(auto_now=False,auto_now_add=False,null=True, blank=True)
    end_time = models.TimeField(auto_now=False,auto_now_add=False,null=True, blank=True)
    limit = models.PositiveIntegerField(default=0,null=True,blank=True)
    trainer = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="trainer",null=True,blank=True)
    comments = models.TextField(default="",null=True,blank=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)
    
    groups = groups_manager.GroupManager()
    objects = models.Manager()

    def __str__(self) -> str:
        return self.title

class Student(models.Model):
    user = models.ForeignKey('user.CustomUser',on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=chooses.STUDENT_STATUS, default=1)
    source = models.ForeignKey('Sources', models.SET_NULL, null=True) # models.PositiveSmallIntegerField(choices=chooses.STUDENT_SOURCES)
    groups = models.ManyToManyField(Group,related_name='student')
    comment = models.TextField()
    balance = models.IntegerField("O'quvchining hisobidagi mablag'", default=0)
    pay_type = models.PositiveSmallIntegerField(choices=chooses.PAY_FORMS,blank=True,null=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)
    students =  students_manager.StudentManager()
    objects = models.Manager()

class Attendace(models.Model):
    # student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendace')
    status = models.SmallIntegerField(choices=chooses.STUDENT_ATTANDENCE_TYPE,null=True,blank=True)
    date = models.DateField()
    group_student = models.ForeignKey("GroupStudents", models.SET_NULL, null=True,related_name='attendance')
    created = models.DateTimeField(auto_now_add=True, null=True)
    creator = models.ForeignKey('user.CustomUser', models.SET_NULL, related_name="created_attendaces", null=True)
    lead_demo = models.ForeignKey("LeadDemo", models.SET_NULL, null=True, related_name='lead_attendance')
    objects = models.Manager()
    attendaces = attendace_manager.AttendaceManager()


class Payment(models.Model):
    paid = models.PositiveIntegerField()
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='payment')
    created = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True)
    payment_type = models.SmallIntegerField("To'lov turi", choices=chooses.PAYMENT_TYPE, default=1)
    comment = models.CharField("Izoh", max_length=500, null=True)
    payments = payment_manager.PaymentManager()


class LeadStatus(models.Model):
    status = models.CharField("Status nomi", max_length=200)
    color = models.CharField("Status rangi", max_length=200, null=True, blank=True)
    
class FormLead(models.Model):
    source = models.ForeignKey('Sources', models.SET_NULL, null=True) #models.PositiveSmallIntegerField(choices=chooses.STUDENT_SOURCES, null=True)
    status = models.ForeignKey(LeadStatus, models.SET_NULL, null=True, blank=True)
    comment = models.TextField()
    telegram = models.CharField("Telegramdagi nomeri", max_length=100, null=True)
    parents = models.ForeignKey("admintion.Parents", models.SET_NULL, null=True, blank=True)
    p_phone = models.CharField(max_length=100, null=True)
    passport = models.CharField("Passport seriya va raqami", max_length=10, null=True)
    file = models.FileField(upload_to="leads", null=True, validators=[validate_file_size])
    days = models.ManyToManyField(GroupsDays, blank=True)
    course = models.ForeignKey(Course, models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True, blank=True, related_name="created_leads")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=False, null=True)
    activity = models.PositiveSmallIntegerField("Lidning statusi", choices=chooses.LEAD_FORM_STATUS, default=1)
    purpose = models.CharField("O'qishdan maqsadi", max_length=300, null=True)
    user = models.OneToOneField('user.CustomUser', models.SET_NULL, null=True, related_name="lead")
    via_form = models.ForeignKey('LeadForms', models.SET_NULL, null=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)
    objects = models.Manager()
    leads = lead_manager.LeadManager()
    def __str__(self) -> str:
        return str(self.id)


class GroupStudents(models.Model):
    student = models.ForeignKey(Student, models.CASCADE, related_name='ggroups') #, related_name="groups")
    group   = models.ForeignKey(Group, models.CASCADE, related_name="students")
    status  = models.SmallIntegerField(choices=chooses.STUDENT_STATUS, default=1)
    attend_date = models.DateField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    # activated_till = models.DateTimeField("O'quvchi uchun guruhning aktiv muddati", null=True)
    finished = models.BooleanField(default=False)
    custom_manager = group_students_manager.GroupStudentManager()
    objects = models.Manager()
    class Meta:
        unique_together = ('student', 'group')

class Parents(models.Model):
    user     = models.OneToOneField('user.CustomUser',on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    passport = models.CharField("Passport", max_length=10, null=True)
    telegram = models.CharField("Telegram contact number", max_length=16, null=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)
    status = models.BooleanField(default=True)
    objects = models.Manager()
    parents = parents_manager.ParentsManager()


class LeadDemo(models.Model):
    lead = models.ForeignKey(FormLead, models.CASCADE, related_name="demo")
    group = models.ForeignKey(Group, models.CASCADE)
    date = models.DateField('Demo dars sanaga belgilandi:', auto_now_add=False, auto_now=False)
    

class TaskTypes(models.Model):
    task_type = models.CharField("Topshiriq turi", max_length=150)


class UserTaskStatus(models.Model):
    whom = models.CharField("Kim uchun?", max_length=25)
    

class Tasks(models.Model):
    task_type = models.ForeignKey(TaskTypes, models.SET_NULL, null=True)
    responsibles = models.ManyToManyField('user.CustomUser', related_name='user_tasks')
    deadline = models.DateTimeField("Deadline:", auto_now_add=False, auto_now=False)
    comment = models.CharField(max_length=500, null=True)
    whom = models.ManyToManyField('user.CustomUser', related_name="my_tasks")
    user_status = models.ForeignKey(UserTaskStatus, models.SET_NULL, null=True)
    status = models.PositiveSmallIntegerField("Statusi", choices=TASK_STATUS, default=1)
    author = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, blank=True)
    leads = models.ManyToManyField(FormLead, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    parents = models.ManyToManyField(Parents, blank=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)
    objects = models.Manager()
    tasks = task_manager.TasksManager()

class SmsIntegration(models.Model):
    limit = models.PositiveIntegerField("Smslar soniga cheklov", default=100)
    used = models.PositiveIntegerField("Foydalanilgan bonus smslar soni", default=0)
    email = models.EmailField("Sms Integratsiya qilingan email", blank=True, null=True)
    password = models.CharField("Sms Integratsiya qilingan parol", blank=True, null=True, max_length=128)
    main = models.BooleanField("Asosiymi?", help_text="Agar bu firmaning(o'quv markazniki emas) ma'lumotlari bo'lsa, belgilang", default=False)
    class Meta:
        verbose_name = "Sms Integratsiya"
        verbose_name_plural = "Sms Integratsiya"


class Messages(models.Model):
    text = models.CharField("Xabar matni", max_length=5000)
    user = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True, related_name='author_messages')
    message_type = models.PositiveSmallIntegerField(choices=MESSAGE_TYPE, default=1)

class EduFormats(models.Model):
    name = models.CharField("Ta'lim formati", max_length=150)

    def __str__(self):
        return self.name

class EduCenters(models.Model):
    name = models.CharField(max_length=150, verbose_name="O'quv markazi")
    director = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey('admintion.Countries', models.SET_NULL, null=True)
    region = models.ForeignKey('admintion.Regions', models.SET_NULL, null=True)
    district = models.ForeignKey('admintion.Districts', models.SET_NULL, null=True)
    address = models.CharField("Manzil", max_length=500, null=True, blank=True)
    max_groups = models.PositiveIntegerField("Maksimal guruh sig'imi", default=0)
    phone_number = models.CharField(max_length=100,null=True,blank=True)
    max_students = models.PositiveIntegerField("Maksimal o'quvchilar sig'imi", default=0)
    teacher_can_see_payments = models.BooleanField("O'qituvchilar talaba to'lovlarini ko'rishi mumkin", default=False)
    teacher_can_sign_contracts = models.BooleanField("O'quvchilar bilan shartnoma imzolash", default=False)
    # format = models.ForeignKey(EduFormats, models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', models.SET_NULL, null=True, blank=True, related_name='filiallar')
    logo = models.ImageField(upload_to='educenters/logos', null=True,blank=True)
    oferta = models.FileField(upload_to='educenters/', null=True,blank=True)
    s_contract = models.FileField(upload_to='educenters/', null=True,blank=True)
    t_contract = models.FileField(upload_to='educenters/', null=True,blank=True)
    j_contract = models.FileField(upload_to='educenters/', null=True,blank=True)
    
    objects = models.Manager()
    educenters = educenters_managers.EduCentersManager()
    def __str__(self):
        return self.name

class LeadForms(models.Model):
    name  = models.CharField(max_length=150, verbose_name="Forma nomi", null=True, blank=True)
    title = models.CharField(max_length=150, verbose_name="Forma sarlavhasi")
    image = models.ImageField(upload_to='forms',null=True,blank=True)
    comment = models.CharField(max_length=2000, null=True,blank=True)
    educenters = models.ForeignKey(EduCenters,on_delete=models.CASCADE, null=True, blank=True)
    courses = models.ForeignKey(Course,on_delete=models.CASCADE, null=True, blank=True)
    sources = models.ForeignKey('Sources',on_delete=models.CASCADE, null=True, blank=True)
    link    = models.URLField(verbose_name="Havola",null=True,blank=True)
    russian = models.BooleanField(default=False)
    english = models.BooleanField(default=False)
    seen    = models.PositiveIntegerField(default=0)
    qrcode  = models.ImageField(upload_to='formleads', null=True)
    lead_forms = lead_forms_managers.LeadFormManager()
    objects = models.Manager()
    def __str__(self) -> str:
        return self.name

class Sources(models.Model):
    title = models.CharField(max_length=150, unique=True)
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
        
class Contacts(models.Model):
    contact_type = models.PositiveSmallIntegerField("Aloqa turi", choices=CONTACT_TYPES)
    value        = models.CharField(max_length=150)
    leadform     = models.ForeignKey(LeadForms, models.CASCADE)

class FormFields(models.Model):
    title    = models.CharField(max_length=150)
    key      = models.CharField(max_length=50, null=True)
    leadform = models.ForeignKey(LeadForms, models.CASCADE)
    order    = models.PositiveIntegerField(default=1)
    required = models.BooleanField("Talab qilinadimi?", default=False)

class FormUniversalFields(models.Model):
    title    = models.CharField(max_length=150)
    key      = models.CharField(max_length=50, null=True)
    order    = models.PositiveIntegerField(default=1)
    required = models.BooleanField("Talab qilinadimi?", default=False)


class Countries(models.Model):
    name = models.CharField("Davlat nomi", max_length=150)
    objects = models.Manager()
    countries = common_managers.CountriesManager()
    def __str__(self):
        return self.name


class Regions(models.Model):
    name = models.CharField("Viloyat nomi", max_length=150)
    country = models.ForeignKey(Countries, models.CASCADE, verbose_name='Davlat')
    objects = models.Manager()
    regions = common_managers.RegionsManager()
    def __str__(self):
        return self.name

class Districts(models.Model):
    name = models.CharField("Viloyat nomi", max_length=150)
    country = models.ForeignKey('Countries', models.CASCADE, verbose_name='Davlat')
    region = models.ForeignKey('Regions', models.CASCADE, verbose_name='Viloyati')
    objects = models.Manager()
    districts = common_managers.DistrictsManager()
    
    def __str__(self):
        return self.name
    

class Exam(models.Model):
    format = models.PositiveSmallIntegerField(choices=EXAM_FORMAT, default=1)  
    type = models.PositiveSmallIntegerField(choices=EXAM_TYPE, default=1)   
    title = models.CharField(max_length=100)
    day = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=100)
    comment = models.TextField()
    file = models.FileField(upload_to='educenters/')
    educenter = models.ForeignKey('admintion.EduCenters', models.SET_NULL, null=True)

    def __str__(self):
        return self.title 