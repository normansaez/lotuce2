from django.shortcuts import render

from django.template import  loader
from django.template import RequestContext
from django.http import HttpResponse

import os

# Create your views here.
DIRNAME = os.path.dirname(__file__)
path = os.path.normpath(os.path.join(DIRNAME, '../media/tux.png'))

def home(request):
    resp = """<img src="/media/tux.png" alt="tux">""" 
    return HttpResponse(resp)

#def index(request):
#    """
#    The same as ste function, but no showing nothing at the begging
#    """
#    t = loader.get_template(path + '/ste.html')
#    c = RequestContext(request, {'ste_name': 'ste'})
#    return HttpResponse(t.render(c))
# Create your views here.
