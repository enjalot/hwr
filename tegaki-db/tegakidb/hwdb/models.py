# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User
from tegakidb.users.models import TegakiUser
from tegakidb.utils.models import Language

from random import randint
from datetime import datetime


class CharacterSet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    lang = models.CharField(max_length=10)      #subtag of language
    description = models.CharField(max_length=255)
    # characters is a string representation of character code lists
    # and/or character code ranges.
    # e.g. 8,10..15,17 is equivalent to 8,10,11,12,13,14,15,17
    characters = models.TextField()
    #user = models.ForeignKey(User,blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True) #Author of charset
    user_display = models.CharField(max_length=255)     #display name of author
    public = models.BooleanField(default=True) 

    @staticmethod
    def get_array_from_string(s):
        """
        Returns an an array representation of the string representation.
        e.g. "8,A..F,11" => [0x8, [0x10,0xF], 0x11]

        raises ValueError if the input is not valid.
        """
        if not isinstance(s, str) and not isinstance(s, unicode):
            raise ValueError

        ret = []
        for ele in s.strip().split(","):
            arr = [int(x, 16) for x in ele.strip().split("..")]
            if len(arr) == 1:
                ret.append(arr[0])
            else:
                ret.append(arr)
        return ret


    def get_string_from_array(list, ord=True):
        """
        Takes in a python list of characters (unicode ordinals if ord=True, utf8 representations otherwise)
        """
        pass


    def contains(self, char_code):
        """
        Returns whether a given character code belongs to the character set
        or not.
        """
        arr = CharacterSet.get_array_from_string(self.characters)
        # FIXME: replaces linear search with binary search
        #        (get_array_from_string must return a sorted array)
        for ele in arr:
            if isinstance(ele, int): # individual character code
                if ele == char_code:
                    return True
            elif isinstance(ele, list): # character code range
                if ele[0] <= char_code and char_code <= ele[1]:
                    return True
        return False

    def __len__(self):
        """
        Returns the number of characters in the character set.
        """
        arr = CharacterSet.get_array_from_string(self.characters)
        length = 0
        for ele in arr:
            if isinstance(ele, int): # individual character code
                length += 1
            elif isinstance(ele, list): # character code range
                length += ele[1] - ele[0] + 1
        return length

    def get_list(self):
        """
        Returns the character set as a python list
        """
        return CharacterSet.get_array_from_string(self.characters)

    def get_random(self):
        """
        Returns a random character code from the set.
        Character codes are equally probable.
        """
        i = randint(0, len(self)-1)
        arr = CharacterSet.get_array_from_string(self.characters)
        n = 0
        for ele in arr:
            if isinstance(ele, int): # individual character code
                if i == n:
                    return ele
                else:
                    n += 1
            elif isinstance(ele, list): # character code range
                range_len = ele[1] - ele[0] + 1
                if n <= i and i <= n + range_len - 1:
                    return ele[0] + i - n
                else:
                    n += range_len
        return None # should never be reached

    def __unicode__(self):
        return self.name

admin.site.register(CharacterSet)


class HandWritingSample(models.Model):
    #character fields
    id = models.AutoField(primary_key=True)             #this will be a unique hash
    unicode = models.IntegerField(null=True)            #Unicode ordinal for the character
    lang = models.CharField(max_length=10)              #subtag of language
    data = models.TextField()                           #coordinate data describing the sample
    data_format = models.CharField(max_length=255)      #('xml', 'json', 'sexp', etc)
    compressed = models.IntegerField(default=0)         #(NON_COMPRESSED=0, GZIP=1, BZ2=2)

    #meta data
    date = models.DateTimeField(default=datetime.today())       #date created
    user_id = models.CharField(max_length=255, blank=True)      #uniqueness implied, probably a hash
    user_display = models.CharField(max_length=255, blank=True) #display name, uniqueness not implied
    user_level = models.IntegerField(null=True)                 #proficiency level (in this lang)
    domain = models.CharField(max_length=255, blank=True)       #what domain the sample was submitted from
    device_used = models.IntegerField(default=0)                #(MOUSE, TABLET, PHONE, PDA, TOUCHSCREEN)

    def __unicode__(self):      #this is the display name
        return self.utf8()

    def utf8(self):
        return unichr(self.unicode)

admin.site.register(HandWritingSample)

class Validation(models.Model):
    """
    A Validation is performed on a HandWritingSample, want to 
    """
    id = models.AutoField(primary_key=True)             #will be unique hash
    sample_id = models.IntegerField()                   #will be the unique identifying hash of the hws
    user = models.CharField(max_length=255)             #the proofreader
    user_display = models.CharField(max_length=255)     #proofreader's display name
    user_level = models.IntegerField()                  #proficiency level of the user

    model = models.BooleanField(default=False)
    stroke_order_incorrect = models.BooleanField(default=False)
    stroke_number_incorrect = models.BooleanField(default=False)
    wrong_stroke = models.BooleanField(default=False)
    wrong_spacing = models.BooleanField(default=False)
    client = models.TextField(blank=True)



