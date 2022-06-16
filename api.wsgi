import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/gettranscript.ca/OHM')
from api import app as application
