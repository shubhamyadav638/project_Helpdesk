from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required()
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')





# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
#
# @login_required  # This decorator ensures the user is logged in before accessing the view.
# def dashboard(request):
#     context = {
#         'request': request  # Include the request object in the context to access user information.
#     }
#     print(request.user.is_customer)
#     return render(request, 'dashboard/dashboard.html', context)