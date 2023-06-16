from django.contrib import admin
from .models import *

admin.site.register(Goods)
admin.site.register(Cart)
admin.site.register(OrderLine)
