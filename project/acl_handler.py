from functools import wraps

from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden

from project.models import ProjectUser


def _is_in_group(request, group_name: list[str] | str) -> bool:
    """Check if the user associated with the request is in the specified group.

    Args:
        request (HttpRequest): The HTTP request object containing user information.
        group_name (list[str] | str): The names of the groups to check membership against.
    Returns:
        bool: True if the user is in the specified group, False otherwise.
    """
    user = request.user
    if not user.is_authenticated:
        return False
    try:
        if isinstance(group_name, str):
            group_name = [group_name]
        project_user = ProjectUser.objects.get(username=user)
        return project_user.groups.filter(name__in=group_name).exists()
    except ProjectUser.DoesNotExist:
        return False


def make_group_checker(group_name):
    """
    Create a dynamic checker function to verify if a user belongs to a specific group.
    This factory function generates a closure that checks whether the user in a given
    request is a member of the specified group. The returned function is suitable for
    use as a custom permission checker or decorator.
    Args:
        group_name (str): The name of the group to check membership against.
    Returns:
        callable: A checker function that takes a request object and returns a boolean
                 indicating whether the user belongs to the specified group. The function
                 name is dynamically set to 'is_<group_name>' with spaces replaced by
                 underscores and converted to lowercase.
    Example:
        >>> is_admin = make_group_checker('Admin')
        >>> is_admin(request)  # Returns True if user is in 'Admin' group
        >>> is_admin.__name__
        'is_admin'
    """

    def checker(request):
        return _is_in_group(request, group_name)

    checker.__name__ = f'is_{group_name.lower().replace(" ", "_")}'
    return checker


def group_required(group_name):
    """
    Decorator to restrict view access to users in a specific group.

    Usage:
        @group_required("Image Manager")
        def my_view(request):
            # Only users in "Image Manager" group can access this
            pass
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if _is_in_group(request, group_name):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )

        return wrapped_view

    return decorator


def create_all_group_checkers():
    """
    Create checker functions for all existing groups in the database.
    This function retrieves all group names from the Group model and generates
    a corresponding checker function for each group using the make_group_checker
    factory function. The generated checkers are stored in a dictionary for easy
    access.

    Returns:
        dict: A dictionary where keys are group names and values are the corresponding
              checker functions.
    """
    groups_checkers = {}
    groups = Group.objects.values_list("name", flat=True)
    for group in groups:
        groups_checkers[group] = make_group_checker(group)

    return groups_checkers


# Middleware to check user admin status on every request
class UserAdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        groups_checkers = create_all_group_checkers()
        for group_name, checker in groups_checkers.items():
            setattr(
                request.user,
                f'is_{group_name.lower().replace(" ", "_")}',
                checker(request),
            )

        response = self.get_response(request)
        if response.status_code == 403:
            messages.error(request, "You don't have permission to access this page.")
            redirect_url = "/login/" if not request.user.is_authenticated else "/"
            response.status_code = 302
            response["Location"] = redirect_url
            response.content = b"You don't have permission to access this page."
        return response
