from pathlib import Path
from django.contrib.staticfiles.finders import AppDirectoriesFinder

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  # Include your app's static files directory
]

STATIC_ROOT = BASE_DIR / "staticfiles"  # Directory where collectstatic will collect files

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Custom finder to exclude specific apps
class ExcludeAppsFinder(AppDirectoriesFinder):
    def list(self, ignore_patterns):
        ignore_patterns += ['admin/*', 'rest_framework/*']  # Exclude admin and rest_framework static files
        return super().list(ignore_patterns)

STATICFILES_FINDERS.append('e.sixth_semester.pycharm.mental_health_django_project.settings.ExcludeAppsFinder')
