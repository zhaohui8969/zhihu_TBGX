# coding:utf-8
import requests
import json
import hashlib
import sendemail
import time
import logging

with open('conf.json') as fop:
    conf = json.loads(fop.read())

user_slugs = [i.encode('utf-8') for i in conf['user_slugs']]

list_size = 20

DEAFULT_HEADER = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.28 Safari/537.36',
                  'Host': 'www.zhihu.com',
                  'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}

session = requests.session()
session.headers.update(DEAFULT_HEADER)


class json_item():
    def __init__(self, content):
        self.action = content['action_text'].encode('utf-8')
        verb = content['verb']
        if verb == 'QUESTION_FOLLOW':  # 关注了问题
            self.title = content['target']['title'].encode('utf-8')
            self.contentless = ''
        elif verb == 'ANSWER_VOTE_UP':  # 赞同了回答
            self.title = content['target']['question']['title'].encode('utf-8')
            self.contentless = content['target']['excerpt'].encode('utf-8')
        elif verb == 'TOPIC_FOLLOW':  # 关注话题
            self.title = content['target']['name'].encode('utf-8')
            self.contentless = ''
        elif verb == 'MEMBER_FOLLOW_COLUMN':  # 关注了专栏
            self.title = content['target']['title'].encode('utf-8')
            self.contentless = content['target']['description'].encode('utf-8')
        elif verb == 'MEMBER_COLLECT_ARTICLE':  # 收藏了文章
            self.title = content['target']['title'].encode('utf-8')
            self.contentless = content['target']['excerpt'].encode('utf-8')
        elif verb == 'ANSWER_CREATE':  # 回答了问题
            self.title = content['target']['question']['title'].encode('utf-8')
            self.contentless = content['target']['excerpt'].encode('utf-8')
        elif verb == 'MEMBER_VOTEUP_ARTICLE':  # 赞了文章
            self.title = content['target']['title'].encode('utf-8')
            self.contentless = content['target']['excerpt'].encode('utf-8')
        elif verb == 'QUESTION_CREATE':  # 添加了问题
            self.title = content['target']['title'].encode('utf-8')
            self.contentless = ''
        elif verb == 'MEMBER_COLLECT_ANSWER':  # 收藏了回答
            self.title = content['target']['question']['title'].encode('utf-8')
            self.contentless = content['target']['excerpt'].encode('utf-8')
        else:  # 未知
            logging.info("UNKNOW %s" % verb)
            self.title = verb.encode('utf-8')
            self.contentless = json.dumps(content, indent=4).encode('utf-8')

        md5(self.action)
        md5(self.title)
        md5(self.contentless)
        self.md5 = md5("%s%s%s" % (self.action, self.title, self.contentless))

    def little_repr(self):
        return "%s %s" % (self.action, self.title)

    def tostring(self):
        return "%s %s\n\n%s" % (self.action, self.title, self.contentless)


def md5(msg):
    return hashlib.md5(msg).hexdigest()


def get_activities(user_slug):
    resp = session.get(
        r'https://www.zhihu.com/api/v4/members/%s/activities?limit=%s&desktop=True' % (user_slug, str(list_size)))
    ret_json = json.loads(resp.content)
    # print json.dumps(ret_json, indent=4)
    json_item_pool = [json_item(i) for i in ret_json['data']]
    return json_item_pool[::-1]


logging.basicConfig(level=logging.INFO)

hash_list = {}
for user_slug in user_slugs:
    hash_list[user_slug] = [0 for i in range(list_size)]
while True:
    for user_slug in user_slugs:
        try:
            notify_msg = []
            json_item_pool = get_activities(user_slug)
            for i in json_item_pool:
                if i.md5 not in hash_list[user_slug]:
                    hash_list[user_slug].append(i.md5)
                    hash_list[user_slug].pop(0)
                    notify_msg.insert(0, i.tostring())
                    logging.info("%s %s" % (user_slug, i.little_repr()))
            if notify_msg:
                logging.info('%s send mail' % user_slug)
                user_url = 'https://www.zhihu.com/people/%s/activities' % user_slug
                user_a_tag = '<a href="%s">%s</a>' % (user_url, user_slug)
                msg_title = u"知乎特别关心 %s" % user_slug
                msg_body = '<br><hr/>'.join([i.replace('\n', '<br>') for i in notify_msg])
                msg_body = "%s<br><hr/>%s" % (user_a_tag, msg_body)
                sendemail.sendmail(msg_title, msg_body)
            else:
                logging.info('%s no update' % user_slug)
        except Exception as e:
            print str(e)
    time.sleep(5 * 60)
