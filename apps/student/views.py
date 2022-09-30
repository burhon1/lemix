from django.shortcuts import render



def student_view(request):
    return render(request, 'student/student.html', {})


def student_detail_view(request, pk):
    return render(request, 'student/student_detail.html', {})


def courses_view(request):
    return render(request, 'student/kurslar_royxati.html', {})


def rating_view(request):
    return render(request, 'student/reyting.html', {})

def exams_view(request):
    return render(request, 'student/imtihonlar_royxati.html', {})

def lesson_detail_view(request):
    return render(request, 'student/darsnig_ichki_sahifasi_video.html')

def contents_view(request):
    return render(request, 'student/content_royxati.html', {})

def test_view(request):
    return render(request, 'student/test.html')

def homework_detail_view(request):
    return render(request, 'student/uyga_vazifa_ichki.html', {})

def homework_view(request):
    return render(request, 'student/uyga_vazifa.html')

def help_view(request):
    return render(request, 'student/yordam.html')