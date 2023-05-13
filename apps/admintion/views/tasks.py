from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from admintion.forms.tasks import TaskForm

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            return JsonResponse({'status':'ok'}, status=201)        
        else:
            return JsonResponse(form.errors, safe=False, status=400)
    return JsonResponse(["So'rov metodi to'g'ri emas"], safe=False, status=400)
    

def tasks_view(request):
    if request.method == "POST":
        pass
        deadline = request.POST.get('deadline',False)
        description = request.POST.get('description',False)
    pass
