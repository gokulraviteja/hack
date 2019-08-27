from django.contrib import admin

# Register your models here.
from .models import Profile,Buffer,Groups,Transactions

admin.site.register(Profile)
admin.site.register(Buffer)
admin.site.register(Groups)
admin.site.register(Transactions)
