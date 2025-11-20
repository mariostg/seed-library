from project.models import ProjectUser


def _is_in_group(request, group_name):
    """Check if the user associated with the request is in the specified group.

    Args:
        request (HttpRequest): The HTTP request object containing user information.
        group_name (str): The name of the group to check membership against.
    Returns:
        bool: True if the user is in the specified group, False otherwise.
    """
    user = request.user
    if not user.is_authenticated:
        return False
    try:
        project_user = ProjectUser.objects.get(username=user)
        return project_user.groups.filter(name=group_name).exists()
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


is_image_manager = make_group_checker("Image Manager")
is_user_manager = make_group_checker("User Manager")
is_project_admin = make_group_checker("Project Admin")
is_plant_profile_manager = make_group_checker("Plant Profile Manager")


# Middleware to check user admin status on every request
class UserAdminCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user.is_project_admin = is_project_admin(request)
        request.user.is_plant_profile_manager = is_plant_profile_manager(request)
        response = self.get_response(request)
        return response
