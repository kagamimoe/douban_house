# -*- coding: utf-8 -*-
import urllib2
import sys, smtplib, poplib
from email.mime.text import MIMEText


reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

SMTPserver = "smtp.163.com"
fromaddr = "xx@163.com"   #发送者邮箱
toaddr = "yy@qq.com"      #接收者邮箱
#sephanie@qq.com

msg_head = ['From:xx@163.com',
            'To:yy@qq.com',
            'Subject:每日豆瓣租房信息汇总']
msg_body = ''

base_url = 'http://www.douban.com/group/shanghaizufang/discussion?start='
t_list = []
link_list = []
words = [u'九号线', u'七宝', u'九亭', u'漕河泾', u'9号线',u'静安新城',u'合川路', ]    #关键字设置

def get_house_list():
    global  t_list
    global  link_list
    i = 0
    print 'start'

    while i < 20:
        num = i * 25
        i = i + 1
        page = urllib2.urlopen(base_url + str(num))
        html = page.read()
        # print html
        soup = BeautifulSoup(html.decode("utf-8"))


        title_list = soup.find_all("td",class_="title")

        for tag in title_list:
            for word in words:
                if word in (tag.contents[1])['title']:
                    t_list.append((tag.contents[1])['title'])
                    link_list.append((tag.contents[1])['href'])

    return t_list, link_list


mailto_list=["yy@qq.com"]
mail_host="smtp.163.com"  #设置服务器
mail_user="xx@163.com"    #用户名
mail_pass="password"   #口令
mail_postfix="163.com"  #发件箱的后缀

def send_mail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me="admin"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    get_house_list()
    t_list = list(set(t_list))
    link_list = list(set(link_list))
    # print '1'
    for i in range(len(t_list)):
        # print type(t_list[i].encode)
        # print ''.join(t_list[i])
        msg_body = msg_body + ''.join(t_list[i]) + '<br><href>' + ''.join(link_list[i]) + '</href><br><br>'

    # print type(msg_body.decode("utf-8"))
    # send_email()
    # print msg_body.encode("gb2312")
    # print msg_body
    # print '2'
    if send_mail(mailto_list,"豆瓣每日租房信息汇总",msg_body):
        print "发送成功"
    else:
        print "发送失败"
