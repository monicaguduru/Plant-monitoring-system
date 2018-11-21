from django.shortcuts import redirect

def login_redirect(request):
	return redirect('/sensors/home/')    #redirects to home page
