
from django.conf.urls import url
from django.core.urlresolvers import reverse

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from yubikey import views

@hooks.register('register_settings_menu_item')
def register_frank_menu_item():
	return MenuItem('YubiKey', reverse('yubikey-setup'), classnames='icon icon-password', order=10000)

@hooks.register('register_admin_urls')
def urlconf_time():
	return [
		url(r'^yubikey-setup/$', views.YubiKeySetup.as_view(), name='yubikey-setup' ),
	]

# @hooks.register('register_admin_urls')
# def urlconf_time():
# 	return [
# 		url(r'^login', views.login, name='login' ),
# 	]