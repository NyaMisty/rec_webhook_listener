from django.db import models


class LiveRecRecord(models.Model):
    rec_uuid = models.CharField('UUID of record', max_length=100, unique=True)
    rec_type = models.CharField('Record type', max_length=200)
    user_id = models.CharField('uid of user', max_length=100)
    room_id = models.CharField('roomId of user', max_length=100)
    user_name = models.CharField('User name', max_length=512)
    live_title = models.CharField('Live title',max_length=2048)
    start_date = models.DateTimeField('Live start time')
    end_date = models.DateTimeField('Live end time', null=True)
    rec_extra_data = models.CharField("Extra data of this record", max_length=16384)
    contributor_info = models.CharField("Contributor information", max_length=2048)
