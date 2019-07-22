import datetime

from django.core.cache import cache

from common import cache_keys, errors, config
from social.models import Swiped, Friend
from user.models import User


def recommend_users(user):
    today = datetime.date.today()

    max_year = today.year - user.profile.min_dating_age
    min_year = today.year - user.profile.max_dating_age
    #被滑动过的id列表
    swiped_user = Swiped.objects.filter(uid=user.id).only('sid')
    # print(swiped_user)
    swiped_sid_list = [s.sid for  s in swiped_user]
    # print(swiped_sid_list)

    rec_users = User.objects.filter(
        location=user.profile.location,
        sex=user.profile.dating_sex,
        birth_year__gte=min_year,
        birth_year__lte=max_year,
    ).exclude(id__in=swiped_sid_list)[0:20] #过滤掉划过的uid  不再出现
    # print(rec_users.count())
    # print(rec_users.query)
    return rec_users


def like_someone(uid, sid):
    Swiped.objects.get_or_create(uid=uid, sid=sid, mark='like')

    # 如果 sid 喜欢 uid，则进行加好友操作
    if Swiped.is_liked(sid, uid):
        Friend.make_friends(sid, uid)
        # Friend.objects.make_friends(sid, uid)


def superlike(uid, sid):
    Swiped.objects.get_or_create(uid=uid, sid=sid, mark='superlike')

    # 如果 sid 喜欢 uid，则进行加好友操作
    if Swiped.is_liked(sid, uid):
        # Friend.make_friends(sid, uid)
        Friend.objects.make_friends(sid, uid)

def rewind(user):
    """
    撤销上一次滑动操作记录
    撤销上一次创建的好友关系
    :param user:
    :return:
    """
    key = cache_keys.SWIPE_LIMIT_PREFIX.format(user.id)

    swipe_times = cache.get(key, 0)

    if swipe_times >= config.SWIPE_LIMIT:
        raise errors.SwipeLimitError

    #筛选最后一次滑动时间
    swipe = Swiped.objects.filter(uid=user.id).latest('created_at')

    if swipe.mark in ['like', 'superlike']:
        Friend.cancel_friends(swipe.uid, swipe.sid)

    swipe.delete()

    now = datetime.datetime.now()
    timeout = 86400 - now.hour * 3600 - now.minute * 60 - now.second

    cache.set(key, swipe_times + 1, timeout=timeout)


def liked_me(user):
    """
    查看喜欢过我的人，过滤掉已经存在的好友
    :param user:
    :return:
    """
    friend_list = Friend.friend_list(user.id)
    #比如76喜欢我1号，1号是不是76的sid
    swipe_list = Swiped.objects.filter(sid=user.id, mark__in=['like', 'superlike']). \
        exclude(uid__in=friend_list).only('uid')

    liked_me_uid_list = [s.uid for s in swipe_list]

    return liked_me_uid_list

