class FirstMiddleware:  
    def __init__(self, get_response):  
        self.get_response = get_response  
      
    def __call__(self, request): 
        if request.user.is_authenticated:
            branch = request.GET.get('branch',False)
            if branch:
                request.session['branch_id']=str(branch)
            else:
                if not request.session.get('branch_id',False):
                    request.session['branch_id']=str(request.user.educenter)
        response = self.get_response(request)  
        return response  