from django.shortcuts import render,redirect
from django.urls import reverse

from admintion.models import FormLead

def forms_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        fio = post.get('fio',False)
        phone = post.get('phone',False)
        source = post.get('source',False)
        comment = post.get('comment',False)
        if fio and phone and source and comment:
            lead_form = FormLead(
                fio=fio,
                phone=phone,
                source=source,
                comment=comment,
                status=1
            )
            lead_form.save()
            return redirect(reverse('admintion:forms')+f"?success={True}")
        else:
            return redirect(reverse('admintion:forms')+f"?error=1")    
    context['objs'] = FormLead.objects.all().order_by('-id')         
    return render(request,'admintion/forms.html',context) 