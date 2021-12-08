# Django Core Modules
from django.db import models
from django.conf import settings

# Apps specific

class IssSys(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
  host_id = models.SmallIntegerField(default=0)
  update_datetime = models.DateTimeField(auto_now_add=True, blank=True)
  isssys_version = models.CharField(max_length = 24, default = '0.0.1-Build-0001', blank=True)
  total_updates = models.SmallIntegerField(default=0)
  security_updates = models.SmallIntegerField(default=0)
  priority1_updates = models.SmallIntegerField(default=0)
  priority2_updates = models.SmallIntegerField(default=0)
  priority3_updates = models.SmallIntegerField(default=0)
  priority4_updates = models.SmallIntegerField(default=0)
  priority5_updates = models.SmallIntegerField(default=0)

  def __str__(self):
      return(str(self.host_id))
