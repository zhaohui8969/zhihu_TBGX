一个知乎特别关心脚本，可以设定关注几个用户，当有新的动态的时候会发送邮件给你

## 配置文件

使用前复制一份配置文件模板`conf.json.example`为`conf.json`，修改配置文件`conf.json`

```json
{
    "mail_sender": "bfbot8969@163.com", # 发件人地址
    "login_passwd": "passwd_here",      # 发件人密码
    "mail_reciver": "natas_hw@163.com", # 收件人地址
    "smtp_server": "smtp.163.com",      # 发信服务器
    "user_slugs": [                     # 需要关注的用户
        "xie-bing-81-95",
        "zhao-hui-36-5"
    ]
}
```

得注册一个邮箱，然后将邮箱的发件人地址和密码、收件人地址、邮件服务器配置好，然后可以测试邮件是否能够正常发送

```bash
python sendemail.py "this is a test mail from zhihu_TBGX"
```

不出意外会你会收到一封标题文`知乎特别关心邮件测试`的邮件，发信没有问题之后修改配置文件中的`关注用户(user_slugs)`部分，对于用户`https://www.zhihu.com/people/zhao-hui-36-5/activities`的user_slug为`zhao-hui-36-5`。

## 启动脚本

```
python zhihu_TBGX.py
```

付了一个supervisor的配置文件`zhihu.supervisor.conf`