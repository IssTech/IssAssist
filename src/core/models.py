# Django Core Modules
from django.db import models
from django.conf import settings

# Apps specific

class CoreConfig(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
  hostname = models.CharField(max_length = 128, default = 'hostname', blank=False)
  fqdn = models.CharField(max_length = 256, default = 'hostname.company.com', blank = True)
  ipv4_address = models.CharField(max_length = 128, default = '1.2.3.4', blank=False)
  #isssys_agent = models.ForeignKey(IssSys, default=None, blank=True, null=True, on_delete=models.CASCADE)

  def __str__(self):
      return(self.fqdn)
