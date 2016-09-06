"""
nvproj URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from nvqueue import views

# Create a router and register our viewsets with it.
router = DefaultRouter(schema_title='NV Queue API')
router.register(r'queues', views.QueueViewSet)
router.register(r'printjobs', views.PrintjobViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]

# following code is useful if you want to see the router generated URLs

# def print_url_pattern_names(patterns):
#     """Print a list of urlpattern and their names"""
#     for pat in patterns:
#         if pat.__class__.__name__ == 'RegexURLResolver':            # load patterns from this RegexURLResolver
#             print_url_pattern_names(pat.url_patterns)
#         elif pat.__class__.__name__ == 'RegexURLPattern':           # load name from this RegexURLPattern
#             if pat.name is not None:
#                 print '[API-URL] {} \t\t\t-> {}'.format(pat.name, pat.regex.pattern)
#
# from django.conf import settings
# if settings.DEBUG:
#     print_url_pattern_names(urlpatterns)