from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

from wagtail.wagtailadmin.views import account
from yubikey.models import Yubikey
from yubikey.validators import valid_public_id

from yubico_client import Yubico

import re

class AuthView(View):
    def post(self, request):
        key = request.POST.get('key', None)
        if key is None:
            response = JsonResponse({'error': _('No YubiKey found')}, status=400)
            return response

        # Make sure only acceptable characters in the key
        pattern = r'[^0-9a-zA-Z]'
        key = re.sub(pattern, '', key)

        if len(key) != 44:
            return JsonResponse({'error': _('Does not appear to be a valid YubiKey')}, status=400)

        try:
            client = Yubico(settings.YUBIKEY_CLIENT_ID, settings.YUBIKEY_CLIENT_SECRET)
            verify = client.verify(key)

            if verify:
                public_id = key[:12]

            yubikey = Yubikey.objects.get(public_id=public_id)
            user = yubikey.user
            request.session['yubikey_user_id'] = user.id
            request.session['incorrect_user'] = False
        except ObjectDoesNotExist:
            return JsonResponse({'error': _('That YubiKey is unrecognized.')}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


        output = {
            "verify": verify,
        }
        
        return JsonResponse(output)

class YubiKeySetup(View):
    def get(self, request):
        User = get_user_model()

        users = User.objects.all()

        return render(request, "yubikey/yubikey-setup.html", {
            'users': users,
        })

    def post(self, request):
        User = get_user_model()
        id = request.POST.get('id')
        public_id = request.POST.get('public_id')

        if not valid_public_id(public_id):
            return JsonResponse({'error': "Invalid public id"}, status=400)

        try:
            user = User.objects.get(pk=id)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        try:
            key = Yubikey.objects.get(user=user)
            key.public_id = public_id
        except Exception as e:
            key = Yubikey(
                public_id = public_id,
                user = user
            )
        key.save()

        output = {
            'key': key.public_id,
        }

        return JsonResponse(output)

@sensitive_post_parameters()
@never_cache
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if username:
            try:
                User = get_user_model()
                user = User.objects.get(username=username)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
            if int(request.session.get('yubikey_user_id')) != user.id:
                request.session['incorrect_user'] = True
                return HttpResponseRedirect( reverse('login') )
    return account.login(request)