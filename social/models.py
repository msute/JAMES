from django.db import models
from django.db.models import Q

from common import errors
from social.managers import FriendManager


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



    # 创建滑动记录，存在就返回False，否则创建记录
    @classmethod
    def swiped(cls, uid, sid, mark):

        maeks = [m for m, _ in cls.MARKS]

        if mark not in maeks:
            raise errors.SidError
        if cls.objects.filter(uid=uid, sid=sid, mark=mark).exists():
            return False
        else:
            cls.objects.get_or_create(uid=uid, sid=sid, mark=mark)
            return True


    @classmethod
    def is_liked(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid, mark__in=['like', 'superlike']).exists()


    class Meta:
        db_table = 'swiped'


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    object = FriendManager()
    @classmethod
    def make_friends(cls, uid1, uid2):
        #通过自定义 uid 排序规则，来组织好友关系，且一组好友关系只保存一份数据
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return cls.objects.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def cancel_friends(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)

        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def friend_list(cls, uid):
        fid_list = []
        #建立一个好友列表
        friends = cls.objects.filter(Q(uid1=uid) | Q(uid2=uid))

        for f in friends:
            #如果当前我是登录的uid，uid2就是我的好友列表，否则反之
            fid = f.uid1 if uid == f.uid2 else f.uid2
            fid_list.append(fid)

        return fid_list

    class Meta():
        db_table = 'friends'