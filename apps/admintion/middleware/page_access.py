from django.shortcuts import redirect
# from admintion.models import Page
from user.models import CustomUser

def check_user_page_access(get_response):
    def middleware(request):
        response = get_response(request)
        # page = Page.objects.filter(path=request.path).first()
        # if page is not None:
        #     user = CustomUser.objects.get(id=request.user.id)
        #     if not page.groups.filter(id__in=list(user.groups.values_list('id',flat=True))).exists():
        #         return redirect('404')
        return response
    return middleware
