from BestJob.settings import UserRole


def roles(request):
    """добавляет значение ролей в контексте"""
    return {
        'roles': UserRole
    }
