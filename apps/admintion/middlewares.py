class FirstMiddleware:  
    def __init__(self, get_response):  
        self.get_response = get_response  
      
    def __call__(self, request):  
        print(request.user)
        if request.user.is_authenticated:
            branch = request.GET.get('branch',False)
            print(branch)
        response = self.get_response(request)  
        return response  