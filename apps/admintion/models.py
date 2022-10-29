from django.db import models
from admintion.querysets import rooms_manager,groups_manager,students_manager,attendace_manager,teachers_manager, parents_manager, payment_manager, group_students_manager, course_manager
from admintion.data import chooses
from user.models import CustomUser
from user.data.chooses import COURSES_SEXES
from admintion.data.chooses import TASK_STATUS, TEACHER_TYPE
# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length=50)
    capacity = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='user/',null=True,blank=True)
    status = models.BooleanField(default=False)

    rooms = rooms_manager.RoomQueryset()

    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    lesson_duration = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    comment = models.TextField()
    status = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, models.SET_NULL, null=True)
    objects = models.Manager()
    courses = course_manager.CoursesManager()
    def __str__(self) -> str:
        return self.title


class Teacher(models.Model):
    teacer_type = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    status = models.BooleanField(default=False,null=True,blank=True)
    teachers = teachers_manager.TeacherManager()
    objects = models.Manager()

class GroupsDays(models.Model):
    days = models.PositiveSmallIntegerField(choices=chooses.GROUPS_DAYS)

class Group(models.Model):
    title = models.CharField(max_length=50)
    comments = models.TextField(default="")
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="group_teacher")
    trainer = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="trainer")
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    days = models.ManyToManyField(GroupsDays)
    pay_type = models.PositiveSmallIntegerField(choices=chooses.PAY_FORMS)
    status = models.PositiveSmallIntegerField(choices=chooses.GROUPS_STATUS)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(auto_now=False,auto_now_add=False,null=True, blank=True)
    end_time = models.TimeField(auto_now=False,auto_now_add=False,null=True, blank=True)
    limit = models.PositiveIntegerField(default=0)
    groups = groups_manager.GroupManager()
    objects = models.Manager()

    def __str__(self) -> str:
        return self.title

class Student(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=chooses.STUDENT_STATUS, default=1)
    source = models.PositiveSmallIntegerField(choices=chooses.STUDENT_SOURCES)
    groups = models.ManyToManyField(Group,related_name='student')
    comment = models.TextField()
    balance = models.IntegerField("O'quvchining hisobidagi mablag'", default=0)
    
    students =  students_manager.StudentManager()
    objects = models.Manager()

class Attendace(models.Model):
    # student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendace')
    status = models.SmallIntegerField(choices=chooses.STUDENT_ATTANDENCE_TYPE,null=True,blank=True)
    date = models.DateField()
    group_student = models.ForeignKey("GroupStudents", models.SET_NULL, null=True,related_name='attendance')
    created = models.DateTimeField(auto_now_add=True, null=True)
    creator = models.ForeignKey(CustomUser, models.SET_NULL, related_name="created_attendaces", null=True)
    
    objects = models.Manager()
    attendaces = attendace_manager.AttendaceManager()


class Payment(models.Model):
    paid = models.PositiveIntegerField()
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='payment')
    created = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(CustomUser, models.SET_NULL, null=True)
    payment_type = models.SmallIntegerField("To'lov turi", choices=chooses.PAYMENT_TYPE, default=1)
    comment = models.CharField("Izoh", max_length=500, null=True)
    payments = payment_manager.PaymentManager()


class LeadStatus(models.Model):
    status = models.CharField("Status nomi", max_length=200)
class FormLead(models.Model):
    # fio = models.CharField(max_length=100)
    # phone = models.CharField(max_length=100)
    source = models.PositiveSmallIntegerField(choices=chooses.STUDENT_SOURCES, null=True)
    status = models.ForeignKey(LeadStatus, models.SET_NULL, null=True, blank=True)
    comment = models.TextField()
    telegram = models.CharField("Telegramdagi nomeri", max_length=100, null=True)
    parents = models.CharField("Ota-onasi", max_length=150, null=True)
    p_phone = models.CharField(max_length=100, null=True)
    # address = models.CharField("Manzili", max_length=500, null=True)
    # email = models.EmailField(null=True)
    passport = models.CharField("Passport seriya va raqami", max_length=10, null=True)
    file = models.FileField(upload_to="leads", null=True)
    # gender = models.PositiveSmallIntegerField(choices=COURSES_SEXES,null=True,blank=True)
    # birthday = models.DateField(null=True,blank=True)
    days = models.ManyToManyField(GroupsDays, blank=True)
    course = models.ForeignKey(Course, models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(CustomUser, models.SET_NULL, null=True, blank=True, related_name="created_leads")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=False, null=True)
    activity = models.PositiveSmallIntegerField("Lidning statusi", choices=chooses.LEAD_FORM_STATUS, default=1)
    purpose = models.CharField("O'qishdan maqsadi", max_length=300, null=True)
    user = models.OneToOneField(CustomUser, models.SET_NULL, null=True, related_name="lead")

    def __str__(self) -> str:
        return str(self.id)


class GroupStudents(models.Model):
    student = models.ForeignKey(Student, models.CASCADE, related_name='ggroups') #, related_name="groups")
    group   = models.ForeignKey(Group, models.CASCADE, related_name="students")
    status  = models.SmallIntegerField(choices=chooses.STUDENT_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True)
    # activated_till = models.DateTimeField("O'quvchi uchun guruhning aktiv muddati", null=True)
    finished = models.BooleanField(default=False)
    custom_manager = group_students_manager.GroupStudentManager()
    objects = models.Manager()
    class Meta:
        unique_together = ('student', 'group')
class Parents(models.Model):
    user     = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    passport = models.CharField("Passport", max_length=10, null=True)
    telegram = models.CharField("Telegram contact number", max_length=16, null=True)
    
    parents = parents_manager.ParentsManager()


class LeadDemo(models.Model):
    lead = models.ForeignKey(FormLead, models.CASCADE)
    group = models.ForeignKey(Group, models.CASCADE)
    date = models.DateField('Demo dars sanaga belgilandi:', auto_now_add=False, auto_now=False)


class TaskTypes(models.Model):
    task_type = models.CharField("Topshiriq turi", max_length=150)


class UserTaskStatus(models.Model):
    whom = models.CharField("Kim uchun?", max_length=25)
    

class Tasks(models.Model):
    task_type = models.ForeignKey(TaskTypes, models.SET_NULL, null=True)
    responsibles = models.ManyToManyField(CustomUser, related_name='user_tasks')
    deadline = models.DateTimeField("Deadline:", auto_now_add=False, auto_now=False)
    comment = models.CharField(max_length=500, null=True)
    whom = models.ManyToManyField(CustomUser, related_name="my_tasks")
    user_status = models.ForeignKey(UserTaskStatus, models.SET_NULL, null=True)
    status = models.PositiveSmallIntegerField("Statusi", choices=TASK_STATUS, default=1)
    author = models.ForeignKey(CustomUser, models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, blank=True)
    leads = models.ManyToManyField(FormLead, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    parents = models.ManyToManyField(Parents, blank=True) 