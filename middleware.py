from django.http import HttpResponsePermanentRedirect,HttpResponseNotFound
from django.core.cache import cache
from django.utils import timezone
from .models import Redirections,NotFoundLog
from django.db.models import F
from django.utils.deprecation import MiddlewareMixin
import re


class TrailingSlashMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if re.search(r'\.[^/]+$', path):
            return None
        if re.search(r'\.[^/]+/$', path):
            return HttpResponsePermanentRedirect(path[:-1])
        if not path.endswith('/'):
            return HttpResponsePermanentRedirect(path + '/')
        return None




class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.strip('/')
        cache_key = f"redirect_{path}"

        # Attempt to retrieve the redirect entry from cache
        redirect_entry = cache.get(cache_key)

        if redirect_entry is None:
            try:
                # Fetch the redirect entry from the database
                redirect_entry = Redirections.objects.get(original_url=path)
                # Cache the redirect entry for 1 hour
                cache.set(cache_key, redirect_entry, timeout=60*60)
            except Redirections.DoesNotExist:
                redirect_entry = None

        if redirect_entry:
            # Update redirect count and last modification date atomically
            Redirections.objects.filter(pk=redirect_entry.pk).update(
                redirect_count=F('redirect_count') + 1,
                last_modification_date=timezone.now()
            )
            return HttpResponsePermanentRedirect(redirect_entry.redirect_url)

        # Continue with the regular request processing
        response = self.get_response(request)
        return response





class NotFoundMiddleware(MiddlewareMixin):
    EXCLUDED_WORDS = ["wp-content", "wp-include", "wp-admin"]  # Add more words as needed
    EXCLUDED_EXTENSIONS = [".php", ".php7",".env",".yml"]  # Add more extensions if needed

    def process_response(self, request, response):
        if response.status_code in [404, 410]:
            url = request.build_absolute_uri()

            # If URL contains excluded words or ends with excluded extensions, do not log it
            if any(word in url for word in self.EXCLUDED_WORDS) or any(url.endswith(ext) for ext in self.EXCLUDED_EXTENSIONS):
                return response

            user_agent = request.META.get('HTTP_USER_AGENT', '')

            not_found_log, created = NotFoundLog.objects.get_or_create(
                url=url,
                defaults={'user_agent': user_agent}
            )
            if not created:
                not_found_log.total_error_count += 1
                not_found_log.user_agent = user_agent
                not_found_log.save()
        return response

