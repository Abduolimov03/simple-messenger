from django.utils import timezone

class UpdateLastSeenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            user = request.user
            if user.is_authenticated:
                user.last_seen = timezone.now()
                user.save(update_fields=['last_seen'])
        except Exception:
            pass
        return response
