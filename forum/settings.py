from django.conf import settings

IS_INAPPROPRIATE_CONTENT_FILTERED = getattr(settings, 'IS_INAPPROPRIATE_CONTENT_FILTERED', True)
