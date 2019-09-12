activate_this = 'C:/Users/Administrator/Desktop/dev/vm_eDCMS/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/Administrator/Desktop/dev/vm_eDCMS/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/Administrator/Desktop/dev/Source/eDCMS')
sys.path.append('C:/Users/Administrator/Desktop/dev/Source/eDCMS/eDCMS')

os.environ['DJANGO_SETTINGS_MODULE'] = 'eDCMS.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eDCMS.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()