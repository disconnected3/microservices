from django.db import models

class Post(models.Model):
    user_id = models.CharField(max_length=30,null=True,blank=True)
    text = models.CharField(max_length=400)
    image = models.ImageField(upload_to="post_images/",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.user_id} -> Post {self.id}"

class Like(models.Model):
    user_id = models.CharField(max_length=30)
    post_id = models.CharField(max_length=30)
    liked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.user_id} -> Post {self.post_id}"

