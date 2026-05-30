import os
from datetime import datetime
from uuid import uuid4

from django.conf import settings


class RequestIDMiddleware:

    def __init__(self, get_response):
        self.DEBUG = settings.DEBUG
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = request.META.get("HTTP_X_REQUEST_ID") or str(uuid4())

        print("AddRequestIDMiddleware", request.get_full_path(), "Request ID", request.request_id)

        response = self.get_response(request)

        response.headers["X-Request-ID"] = request.request_id

        return response

class UserActivityLoggingMiddleware:
    # запись в файл usersActivity.log информации о посещённых пользователем URL.

    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = getattr(settings, 'USER_ACTIVITY_LOG_FILE', 'usersActivity.log')
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def __call__(self, request):
        self._log_activity(request)
        response = self.get_response(request)
        return response

    def _log_activity(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            username = request.user.username
        else:
            username = "Anonymous"

        text = f"{datetime.now().strftime("%m.%d.%Y %H:%M")} | {username} | URL={request.get_full_path()}\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            print(f"Failed to write user activity log: {e}")