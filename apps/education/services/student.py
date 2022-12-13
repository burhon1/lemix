from education.models import Contents
from admintion.models import Student


def set_student_viewed_content(student: Student, content: Contents) -> None:
    content.students.add(student)
    content.save()