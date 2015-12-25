# Create your views here.
from django.shortcuts import render_to_response


def index(request):
	from .models import Contact
	cs=Contact.objects.all().order_by('nomTags')

	return render_to_response('telephones/index.html', {"cs":cs})
