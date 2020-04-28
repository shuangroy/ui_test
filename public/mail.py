"""
 @desc:邮件发送
 @author: yansh
"""
import os
import sys
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from public.log import Log
from public.readconfig import ReadConfig

# log = Log()
read = ReadConfig()
# root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_path = os.path.dirname(os.path.abspath(sys.argv[0]))

# 测试报告的路径
reportPath = os.path.join(root_path, 'report', 'testreport')
mail_server = read.getValue('Mail', 'mail_server')
mail_subject = read.getValue('Mail', 'mail_subject')
# 配置收发件人
recvaddress = read.getValue('Mail', 'mail_to')  # ['xxx.xx@xxx.com', 'xxxx@qq.com']
sendaddr_name = read.getValue('Mail', 'mail_from')
sendaddr_pwd = read.getValue('Mail', 'mail_from_pwd')


class SendMail:
    def __init__(self, recver=None):
        """接收邮件的人：list or tuple"""
        if recver is None:
            self.sendTo = recvaddress
        else:
            self.sendTo = recver

    def __get_report(self):
        """获取最新测试报告"""
        dirs = os.listdir(reportPath)
        dirs.sort()
        newreportname = dirs[-1]
        print('The new report name: {0}'.format(newreportname))
        return newreportname

    def __take_messages(self):
        """生成邮件的内容，和html报告附件"""
        newreport = self.__get_report()
        self.msg = MIMEMultipart()
        self.msg['Subject'] = mail_subject
        self.msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

        with open(os.path.join(reportPath, newreport), 'rb') as f:
            mailbody = f.read()
        html = MIMEText(mailbody, _subtype='html', _charset='utf-8')
        self.msg.attach(html)

        # html附件
        att1 = MIMEText(mailbody, 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="TestReport.html"'  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        self.msg.attach(att1)

    def send(self):
        """发送邮件"""
        log.info('开始发送邮件...')
        self.__take_messages()
        self.msg['from'] = sendaddr_name
        try:
            smtp = smtplib.SMTP(mail_server, 25)
            smtp.login(sendaddr_name, sendaddr_pwd)
            smtp.sendmail(self.msg['from'], self.sendTo, self.msg.as_string())
            smtp.close()
            log.info('邮件发送成功！！')
        except Exception as e:
            log.error('发送邮件错误,{}'.format(e))
            raise


if __name__ == '__main__':
    sendMail = SendMail()
    # sendMail.send()