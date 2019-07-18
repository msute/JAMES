from django.db import models


class Swiped(models.Model):
    '''
    滑动记录
    '''
    MARKS = (
        ('like', '喜欢'),
        ('dislike', '不喜欢'),
        ('superlike', '超级喜欢'),
    )

    uid = models.IntegerField()  #当前登录的用户
    sid = models.IntegerField()  #其他用户，被划过的人
    mark = models.CharField(max_length=16, choices=MARKS)
    created_at = models.DateTimeField(auto_now_add=True)  #滑动时间

    class Meta:
        db_table = 'swiped'
