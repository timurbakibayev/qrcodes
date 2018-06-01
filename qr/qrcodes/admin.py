from django.contrib import admin
from qrcodes.models import Doctor
from qrcodes.models import Clinic
from qrcodes.models import Vote

admin.site.register(Doctor)
admin.site.register(Clinic)
admin.site.register(Vote)
