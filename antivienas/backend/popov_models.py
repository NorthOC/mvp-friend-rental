from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import os
from PIL import Image

def user_img_upload_path(instance, filename):
    return os.path.join(f"user_uploads/user_{instance.user.pk}", filename)

class User(AbstractUser):
    
    @property
    def avatar(self):
        return UserProfilePicture.avatar(self)

class UserProfilePicture(models.Model):
    """User profile pictures"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_img_upload_path)
    is_avatar = models.BooleanField(default=False)
    created =   models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def avatar(cls, user):
        """returns a users selected avatar"""

        try:
            image = UserProfilePicture.objects.filter(user=user, is_avatar=True)[0]
        except:
            return None
        return image
    
    def rebalance_avatar(self, *args, **kwargs):
        """after deleting an image, makes sure that there's an avatar image"""

        user_images = UserProfilePicture.objects.filter(user=self.user).order_by("created")

        if user_images.count() == 0:
            return

        avatar = user_images.filter(is_avatar=True).first()

        if not avatar:
            image = user_images.first()
            image.is_avatar = True
            image.save()
    
    @classmethod
    def set_avatar(cls, user, avatar_id):
        """sets the users preferred avatar"""
        user_images = UserProfilePicture.objects.filter(user=user).order_by("created")
        user_images.update(is_avatar=False)

        if user_images.count() == 0:
            return

        if user_images.count() > avatar_id:
            image = user_images[avatar_id]
            image.is_avatar = True
            image.save()


    def delete(self, *args, **kwargs):
        """deletes an image and rebalances avatars"""
        super().delete()
        self.rebalance_avatar()

    def crop_and_save(self, *args, **kwargs):
        """allows only 3 images per user. Crops the image into square before saving"""
        super().save()

        # delete if this is 4th picture uploaded
        images = UserProfilePicture.objects.filter(user=self.user).order_by('created')

        if images.count() > 3:
            images[0].delete()
        
        if images.count() == 1:
            avatar = images.first()
            avatar.is_avatar = True
            avatar.save()
                  

        img_path = self.image.path
        img = Image.open(img_path)
        width, height = img.size  # Get dimensions

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 400 or height > 400:
            img.thumbnail((400, 400))

        img.save(img_path)