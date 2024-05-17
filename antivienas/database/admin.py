from django.contrib import admin
from .models import User, FriendSetting, Dispute, Order

# Čia registruojami modeliai bus matomi admin/ valdymo skyde

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'profile_type', 'email', 'first_name', 'last_name', 'gender', 'birthday', 'city')
    search_fields = ('first_name', 'last_name', 'city', 'email', 'pk')

class FriendSettingAdmin(admin.ModelAdmin):
    list_display = ('friend', 'level', 'orders_completed', 'price_per_hour', 'is_public')
    search_fields = ('friend',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'friend', 'order_status', 'total_price', 'created')
    search_fields =('user', 'friend')

class DisputeAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in Dispute._meta.fields]


admin.site.register(User, UserAdmin)
admin.site.register(FriendSetting, FriendSettingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Dispute, DisputeAdmin)