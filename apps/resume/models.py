from django.db import models


class Resume(models.Model):
    # TODO add a unique (name, user) constraint
    name = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.user.username, self.name)


class ResumeItem(models.Model):
    """
    A single resume item, representing a job and title held over a given period
    of time.
    """
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE)

    title = models.CharField(max_length=127)
    company = models.CharField(max_length=127)

    start_date = models.DateField()
    # Null end date indicates position is currently held
    end_date = models.DateField(null=True, blank=True)

    description = models.TextField(max_length=2047, blank=True)

    def __unicode__(self):
        return "{}: {} at {} ({})".format(self.user.username,
                                          self.title,
                                          self.company,
                                          self.start_date.isoformat())
