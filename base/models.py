from django.db import models
from django.conf import settings
from datetime import date

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.timezone import get_fixed_timezone
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from ckeditor_uploader.fields import RichTextUploadingField 

from rest_framework import serializers


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)

    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.headline

    def get_markdown_description(self):
        data = self.body_text
        return mark_safe(data)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.headline)
        super().save(*args, **kwargs)


class MyEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('id', 'headline', 'body_text', 'pub_date', 'mod_date')


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('__all__')