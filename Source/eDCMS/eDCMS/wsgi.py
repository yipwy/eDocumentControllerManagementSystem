activate_this = 'C:/Users/sam_hs/Desktop/dev/eDocumentControllerManagementSystem/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/sam_hs/Desktop/dev/eDocumentControllerManagementSystem/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/sam_hs/Desktop/dev/eDocumentControllerManagementSystem/Source/eDCMS')
sys.path.append('C:/Users/sam_hs/Desktop/dev/eDocumentControllerManagementSystem/Source/eDCMS/eDCMS')

os.environ['DJANGO_SETTINGS_MODULE'] = 'eDCMS.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eDCMS.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()