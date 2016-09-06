from __future__ import unicode_literals

from django.db import models

class Queue(models.Model):

    """
    Print queues
    """
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "Queue '%s'%s" % (self.name, (" (ID=" + str(self.id) + ")") if self.id else "")


class Printjob(models.Model):

    """
    Print jobs each with a reference to their associated queue
    """

    STATE_CHOICES = (
        ('waiting', 'waiting'),
        ('printing', 'printing'),
        ('complete', 'complete'),
    )

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=255)  # name of this print job; possible enhancement: use (possibly truncated) filename if not present
    state = models.CharField(choices=STATE_CHOICES, default='waiting', max_length=20)

    # for this example the submitting user is sent in the POST request and is stored as a string
    # typically this would be done using django.auth, for example user = models.ForeignKey('auth.User', related_name='printjobs')
    user = models.CharField(max_length=255)

    filename = models.CharField(max_length=1024)  # filename send by requestor
    printer = models.CharField(max_length=255, blank=True)  # updated when a job is given to a printer
                                                            # might eventually be a foreign key to a printer table
    queue = models.ForeignKey('Queue', related_name='printjobs')  # queue that this job is associated with

    class Meta:
        ordering = ('queue', 'created',)

    def __str__(self):
        return "Job '%s' on queue '%s'" % (self.name, self.queue.name)