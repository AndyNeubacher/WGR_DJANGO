from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def dashboard(request):
    return HttpResponse("Manager-Dashboard (Platzhalter fuer Task 3).")
