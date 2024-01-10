from rest_framework.renderers import JSONRenderer
from .service.access_service import user_authenticate
from .service.doctor_service import doctor_authenticate
from .service.patient_service import patient_authenticate
from .service.record_service import record_authenticate
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


def DoctorAuthenticationMiddleware(get_response):
    def middleware(request):
        path_info = resolve(request.path_info)
        has_doctor_pattern = path_info.route.startswith(
            "service/user/<str:uid>/doctors/<str:did>/"
        )
        if has_doctor_pattern:
            path_params = path_info.kwargs
            uid, did = path_params["uid"], path_params["did"]
            auth_response = doctor_authenticate(uid, did, lambda: get_response(request))
            auth_response.accepted_renderer = JSONRenderer()
            auth_response.accepted_media_type = "application/json"
            auth_response.renderer_context = {}
            try:
                return auth_response.render()
            except:
                return auth_response

        return get_response(request)

    return middleware


def PatientAuthenticationMiddleware(get_response):
    def middleware(request):
        path_info = resolve(request.path_info)
        has_patient_pattern = path_info.route.startswith(
            "service/user/<str:uid>/patients/<str:pid>/"
        )

        if has_patient_pattern:
            path_params = path_info.kwargs
            uid, pid = path_params["uid"], path_params["pid"]
            auth_response = patient_authenticate(uid, pid, lambda: get_response(request))
            auth_response.accepted_renderer = JSONRenderer()
            auth_response.accepted_media_type = "application/json"
            auth_response.renderer_context = {}
            try:
                return auth_response.render()
            except:
                return auth_response

        return get_response(request)

    return middleware


def RecordAuthenticationMiddleware(get_response):
    def middleware(request):
        path_info = resolve(request.path_info)
        has_record_pattern = path_info.route.startswith(
            "service/user/<str:uid>/patients/<str:pid>/records/<str:rid>/"
        )

        if has_record_pattern:
            path_params = path_info.kwargs
            pid, rid = path_params["pid"], path_params["rid"]
            auth_response = record_authenticate(pid, rid, lambda: get_response(request))
            auth_response.accepted_renderer = JSONRenderer()
            auth_response.accepted_media_type = "application/json"
            auth_response.renderer_context = {}
            try:
                return auth_response.render()
            except:
                return auth_response

        return get_response(request)

    return middleware