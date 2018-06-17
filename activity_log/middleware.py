# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django
from django.utils.module_loading import import_string as _load
from django.core.exceptions import DisallowedHost
from django.http import HttpResponseForbidden
from .models import ActivityLog
from . import conf


try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    # Works perfectly for everyone using MIDDLEWARE_CLASSES
    MiddlewareMixin = object


def get_ip_address(request):
    for header in conf.IP_ADDRESS_HEADERS:
        addr = request.META.get(header)
        if addr:
            return addr.split(',')[0].strip()


def get_extra_data(request, response, body):
    if not conf.GET_EXTRA_DATA:
        return
    return _load(conf.GET_EXTRA_DATA)(request, response, body)


def is_authenticated(request):
    if django.__version__ < '2':
        return request.user.is_authenticated()
    else:
        return request.user.is_authenticated


class ActivityLogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.saved_body = request.body
        if conf.LAST_ACTIVITY and is_authenticated(request):
            getattr(request.user, 'update_last_activity', lambda: 1)()

    def process_response(self, request, response):
        try:
            self._write_log(request, response, getattr(request, 'saved_body', ''))
        except DisallowedHost:
            return HttpResponseForbidden()
        return response

    def _write_log(self, request, response, body):
        miss_log = [
            not(conf.ANONIMOUS or is_authenticated(request)),
            request.method not in conf.METHODS,
            any(url in request.path for url in conf.EXCLUDE_URLS)
        ]

        if conf.STATUSES:
            miss_log.append(response.status_code not in conf.STATUSES)

        if conf.EXCLUDE_STATUSES:
            miss_log.append(response.status_code in conf.EXCLUDE_STATUSES)

        if any(miss_log):
            return

        if getattr(request, 'user', None) and is_authenticated(request):
            user, user_id = request.user.get_username(), request.user.pk
        elif getattr(request, 'session', None):
            user, user_id = 'anon_{}'.format(request.session.session_key), 0
        else:
            return

        ActivityLog.objects.create(
            user_id=user_id,
            user=user,
            request_url=request.build_absolute_uri()[:255],
            request_method=request.method,
            response_code=response.status_code,
            ip_address=get_ip_address(request),
            extra_data=get_extra_data(request, response, body)
        )
