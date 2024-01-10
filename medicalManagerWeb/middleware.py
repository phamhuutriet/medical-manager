from rest_framework.renderers import JSONRenderer
from .service.access_service import user_authenticate
from django.urls import resolve, reverse


# Views that don't need user authentication
USER_AUTH_BYPASS_VIEWS = {
    "signup_view": ["POST"],
    "signin_view": ["POST"],
    "verify_signup_view": ["GET"],
}


def UserAuthenticationMiddleware(get_response):
    def middleware(request):
        resolved_path_name = resolve(request.path_info).url_name

        # This leave room for customized auth for remote
        if (
            resolved_path_name in USER_AUTH_BYPASS_VIEWS
            and request.method in USER_AUTH_BYPASS_VIEWS[resolved_path_name]
        ):
            return get_response(request)

        auth_response = user_authenticate(request, callback=lambda: get_response(request))
        auth_response.accepted_renderer = JSONRenderer()
        auth_response.accepted_media_type = "application/json"
        auth_response.renderer_context = {}
        try:
            return auth_response.render()
        except:
            return auth_response

    return middleware