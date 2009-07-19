# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

class Language(models.Model):
    subtag = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.subtag
admin.site.register(Language)

