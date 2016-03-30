import hashlib
import os
import sys

from django.conf import settings
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', '%+%g=!o)+2!x5h@9v6ek#m4c^f$7&!qfymmi*u2&hp%%bt-_v=')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG = DEBUG,
    SECRET_KEY = SECRET_KEY,
    ALLOWED_HOSTS = ALLOWED_HOSTS,
    ROOT_URLCONF = __name__,
    MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    INSTALLED_APPS = (
    'django.contrib.staticfiles',
    ),
    TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    ),
    STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    ),
    STATIC_URL = '/static/',
)

from django import forms
from django.conf.urls import url
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import etag


from io import BytesIO
from PIL import Image, ImageDraw

class ImageForm(forms.Form):
    height = forms.IntegerField(min_value=1, max_value=2000)
    width  = forms.IntegerField(min_value=1, max_value=2000)
    def generate(self, image_format='PNG'):
        height = self.cleaned_date['height']
        width = self.cleaned_date['width']
        key = '{}.{}.{}'.format(height, width, image_format)
        content = cache.get(key)
        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{}X{}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight)//2
                textleft = (width - textwidth )//2
                draw.text((textleft, texttop), text, fill(255,255,255))
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60*60)

        return content

def generate_etag(request, width, height):
    content = 'placeholder: {0}X{1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag)
def placeholder(request, width, height):
    form = ImageForm({'height' : height, 'width' : width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Request')

def index(request):
    example = reverse('placeholder', kwargs={'width':50, 'height':50})
    context = {
        'example' : request.build_absolute_uri(example)
    }
    return render(request, 'home.html', context)

urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder,
            name='placeholder'),
    url(r'^$', index, name='homepage'),
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)