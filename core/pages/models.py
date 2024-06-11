from django.db import models
from django.db.models import F, Func, IntegerField

# Create your models here.
class Hosts(models.Model):
    type_choices=(
        ('',''),
        ('DESKTOP','DESKTOP'),
        ('NOTEBOOK','NOTEBOOK'),
        ('SWITCH','SWITCH'),
        ('CAMERA','CAMERA'),
        ('IMPRESSORA','IMPRESSORA'),
        ('SERVIDOR','SERVIDOR'),
        ('ACCESS POINT','ACCESS POINT'),
        ('REL DIMEP SMART','REL DIMEP SMART'),
        ('REL DIMEP XP','REL DIMEP XP'),
        ('AUTOMACAO','AUTOMACAO'),
        ('BALANCA','BALANCA'),
        ('NVR INTELBRAS','NVR INTELBRAS'),
        ('DVR INTELBRAS','DVR INTELBRAS'),
        ('HUB','HUB'),
        ('HP ILO','HP ILO'),
        ('CATRACA DMP','CATRACA DMP'),
        ('PABX','PABX'),
        ('IMPRESSORA TERM','IMPRESSORA TERM'),
        ('FIREWALL','FIREWALL')
    )
    ip=models.GenericIPAddressField(default='-')
    hostname=models.CharField(max_length=100,default='-',blank=False)
    host_type=models.CharField(max_length=100,default='-',choices=type_choices,blank=False)
    mac_1=models.CharField(max_length=17,default='-',blank=False)
    mac_2=models.CharField(max_length=17,default='-',blank=True,null=False)
    uplink=models.CharField(max_length=100,default='-')
    dns=models.CharField(max_length=100,default='-')
    os=models.CharField(max_length=100,default='-')
    office=models.CharField(max_length=100,default='-')
    empresa=models.CharField(max_length=100,default='-')

    def __str__(self):
        return "{} {}".format(self.hostname,self.mac_1)
    
    class Meta:
        ordering=[
            Func(F('ip'), function='INET_ATON', output_field=IntegerField())
        ]

class Unknow(models.Model):
    ip=models.CharField(max_length=17,blank='-')
    mac=models.CharField(max_length=17,default='',blank='-')
    dns=models.CharField(max_length=100,default='',blank='-')
    scan_time=models.CharField(max_length=100,default='',blank='-')

    def __str__(self):
        return "{} {}".format(self.ip,self.mac)

    class Meta:
        ordering=[
            Func(F('ip'), function='INET_ATON', output_field=IntegerField())
        ]

class Switch(models.Model):
    switch_id=models.CharField(max_length=50,default='-')
    port=models.CharField(max_length=100,default='-')
    hostname=models.CharField(max_length=100,default='-')
    ip=models.CharField(max_length=100,default='-')
    mac_1=models.CharField(max_length=100,default='-')

    class Meta:
        ordering=[
            Func(F('port'), function='INET_ATON', output_field=IntegerField())
        ]