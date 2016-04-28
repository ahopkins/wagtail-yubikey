# README #

**IMPORTANT** Before completing the installation, it is suggested that you already have a session logged into the Wagtail admin panel. It makes the setup easier at the end to already be authenticated. 

## Step 0 - Install Dependencies ##

This app makes use of [django-overextends](https://github.com/stephenmcd/django-overextends) to override the default Wagtail login template, and [python-yubico-client](https://github.com/Kami/python-yubico-client).

```bash
$ pip install django-overextends
$ pip install yubico-client
```

## Step 1 - Install the App ##

Grab the package from this repository and place it in your Django project.

## Step 2 - Setup the App ##

Make the following changes to two of your Wagtail app files.

### ```settings.base.py``` ###

Update your Wagtail ```settings``` by editing the appropriate file to include ```yubikey``` in the  ```INSTALLED_APPS``` list, and saving your **client_id** and **client_secret** supplied by Yubico as follows:

```python
INSTALLED_APPS = [
    ...
    'yubikey', # Must be before 'wagtail.wagtailadmin',
    'overextends',
    ...
]

YUBIKEY_CLIENT_ID = '12345'
YUBIKEY_CLIENT_SECRET = 'zzzxxxyyyAAABBBCCC111222333='
```

### ```urls.py``` ###

Update the **main** url file in your project's main app directory. It should be the one that already has ```url(r'^admin/', include(wagtailadmin_urls)),``` in the ```urlpatterns``` list. Import ```yubikey.urls.urlpatterns``` and include them inside of the ```urlpatterns``` list.

**HOWEVER**, in order for this to work properly, you need to override the existing ```r'^admin/login'``` route. Thereefore, make sure to list the new login route before Wagtail's admin include.

```python
from yubikey.urls import urlpatterns as yubikey_urls

urlpatterns = [
    ...
    url(r'^yubikey/', include(yubikey_urls)),
    url(r'^admin/login', yubikey_login, name='login' ), # Must become before include(wagtailadmin_urls)
    ...
    url(r'^admin/', include(wagtailadmin_urls)), # This is Wagtail's default admin URL include.
```

## Step 3 - Run the Migrations ##

Once this is complete, run:
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

## Step 4 - Setup your YubiKeys ##

You should now have a new menu in Wagtail Admin at *Settings* >> *YubiKey*. Here you can manage your user's keys.

---

This is still an early version of this app. Still some tweaks are needed:

- Create pip installer
- Command line interface for updating and managing ```public_id``` and YubiKeys of users
- Remove YubiKey from a User
- Disable YubiKey login requirement for a User
