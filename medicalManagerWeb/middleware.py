from rest_framework.renderers import JSONRenderer
from .service.patient_service import patient_authenticate
from .service.record_service import record_authenticate
from .service.template_service import template_authenticate
from .service.treatment_service import treatment_authenticate
from django.urls import resolve, reverse


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


def TemplateAuthenticationMiddleware(get_response):
    def middleware(request):
        path_info = resolve(request.path_info)
        has_template_pattern = path_info.route.startswith(
            "service/user/<str:uid>/templates/<str:tid>/"
        )

        if has_template_pattern:
            path_params = path_info.kwargs
            uid, tid = path_params["uid"], path_params["tid"]
            auth_response = template_authenticate(uid, tid, lambda: get_response(request))
            auth_response.accepted_renderer = JSONRenderer()
            auth_response.accepted_media_type = "application/json"
            auth_response.renderer_context = {}
            try:
                return auth_response.render()
            except:
                return auth_response

        return get_response(request)

    return middleware


def TreatmentAuthenticationMiddleware(get_response):
    def middleware(request):
        path_info = resolve(request.path_info)
        has_treatment_pattern = path_info.route.startswith(
            "service/user/<str:uid>/patients/<str:pid>/records/<str:rid>/treatments/<str:tid>/"
        )

        if has_treatment_pattern:
            path_params = path_info.kwargs
            rid, tid = path_params["rid"], path_params["tid"]
            auth_response = treatment_authenticate(rid, tid, lambda: get_response(request))
            auth_response.accepted_renderer = JSONRenderer()
            auth_response.accepted_media_type = "application/json"
            auth_response.renderer_context = {}
            try:
                return auth_response.render()
            except:
                return auth_response

        return get_response(request)

    return middleware