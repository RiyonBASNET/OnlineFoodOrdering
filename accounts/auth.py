from django.shortcuts import redirect

# to check if the user is logged in or not


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function

# give access to pages if request comes from admin
# if request is from normal user redirect to user dashboard


def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_function

# give access to userpage if request comes from a normal user
# if request comes from admin then redirect to admin dashboard


def user_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function
