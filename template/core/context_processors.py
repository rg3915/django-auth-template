from django.conf import settings


def project(request):
    """Deixa {{ project_name }} disponível em todo template."""
    return {'project_name': getattr(settings, 'PROJECT_NAME', '')}
