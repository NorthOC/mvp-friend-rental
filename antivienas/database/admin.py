from django.contrib import admin
from .models import User, FriendSetting, Dispute, Order, UserProfilePicture, VerifyIdPicture

# Čia registruojami modeliai bus matomi admin/ valdymo skyde

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'profile_type', 'email', 'first_name', 'last_name', 'gender', 'birthday', 'city', 'orders_completed')
    search_fields = ('first_name', 'last_name', 'city', 'email', 'pk')

class FriendSettingAdmin(admin.ModelAdmin):
    list_display = ('friend', 'level', 'price_per_hour', 'is_public')
    search_fields = ('friend',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'friend', 'order_status', 'total_price', 'created')
    search_fields =('user', 'friend')

class DisputeAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in Dispute._meta.fields]

class UserProfilePicAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in UserProfilePicture._meta.fields]

class VerifyIdAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in VerifyIdPicture._meta.fields]
    search_fields = ('user', 'is_verified')



admin.site.register(User, UserAdmin)
admin.site.register(FriendSetting, FriendSettingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Dispute, DisputeAdmin)
admin.site.register(UserProfilePicture, UserProfilePicAdmin)
admin.site.register(VerifyIdPicture, VerifyIdAdmin)