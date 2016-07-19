# Bible API data model classes
# Sammy Fung <sammy@sammy.hk>

from django.db import models


class Version(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    language = models.CharField(max_length=6)

    def __str__(self):
        return self.code


class Book(models.Model):
    TESTAMENT = (
        ('O', 'Old'),
        ('N', 'New'),
    )
    version = models.ForeignKey(Version)
    name = models.CharField(max_length=30)
    testament = models.CharField(max_length=1, choices=TESTAMENT)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "%s (%s)"%(self.name, self.version)


class Bible(models.Model):
    book = models.ForeignKey(Book)
    chapter = models.IntegerField()
    verse = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return "%s %s:%s"%(self.book.name, self.chapter, self.verse)


class Heading(models.Model):
    before = models.ForeignKey(Bible)
    text = models.TextField()
