from django.db import models


class ResumeItem(models.Model):
    """
    A single resume item, representing a job and title held over a given period
    of time.
    """
    title = models.CharField(max_length=127)
    company = models.CharField(max_length=127)
    resume = models.ForeignKey('resume.Resume', on_delete=models.CASCADE)

    start_date = models.DateField()
    # Null end date indicates position is currently held
    end_date = models.DateField(null=True, blank=True)

    description = models.TextField(max_length=2047, blank=True)

    def __unicode__(self):
        return "{}: {} at {} ({})".format(self.user.username,
                                          self.title,
                                          self.company,
                                          self.start_date.isoformat())


class Resume(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=127)

    def __unicode__(self):
        return "{} by {}".format(self.name, self.user.username)
