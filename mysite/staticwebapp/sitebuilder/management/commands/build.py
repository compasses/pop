import os
import shutil
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.test.client import Client


def get_pages():
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
        if name.endswith('.html'):
            yield name[:-5]

class Command(BaseCommand):
    help = 'Build static site output'
    def handle(self, *args, **options):
        """ Rqeust pages and build output """
        settings.DEBUG = False
        settings.COMPRESS_ENABLED = True
#        print args
        if args:
            print "got args "
            pages = args
            available = list(get_pages())
            invalid = []
            for page in pages:
                if page not in available:
                    invalid.append(page)
                if invalid:
                    msg = "Invalid pages: {}".format(', '.join(invalid))
                    print msg
                    #raise CommandError(msg)
        else:
            page = get_pages()
            if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
                shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
            os.mkdir(settings.SITE_OUTPUT_DIRECTORY)
            os.mkdir(settings.STATIC_ROOT)
        call_command('collectstatic', interactive=False, clear=True, verbosity=0)
        call_command('compress', interactive=False, force=True)
        client = Client()
        for page in get_pages():
            url = reverse('page', kwargs={'slug' : page})
            response = client.get(url)
            if page == 'index':
                out_dir = settings.SITE_OUTPUT_DIRECTORY
            else:
                out_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY, page)
                if not os.path.exists(out_dir):
                    os.mkdir(out_dir)
            with open(os.path.join(out_dir, 'index.html'), 'wb') as f:
                f.write(response.content)
