import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import yaml

email_config_file = './utils/email_config.yaml'
# 设置邮箱
with open(email_config_file, 'r') as f:
    config = yaml.safe_load(f.read())
    print(config)
    f.close()

class ErrorEmail:
    def __init__(self):

        self.my_email = config['my_email']
        self.code = config['code']

        # 1. 连接邮箱服务器 需要根据邮箱修改端口号
        #self.con = smtplib.SMTP_SSL('smtp.163.com', 465)
        self.con = smtplib.SMTP_SSL('smtp.126.com', 465)

        # 2. 登录邮箱
        self.con.login(self.my_email, self.code) 

        # 3. 准备数据
        # 创建邮件对象
        self.msg = MIMEMultipart()

        # 设置邮件主题
        subject = Header('Scicrawl Error', 'utf-8').encode()
        self.msg['Subject'] = subject

        # 设置邮件发送者
        self.msg['From'] = self.my_email

        # 设置邮件接受者
        self.msg['To'] = self.my_email
    
    def send(self, error):
        # 添加文字内容
        text = MIMEText(error, 'plain', 'utf-8')
        self.msg.attach(text)

        # 3.发送邮件
        self.con.sendmail(self.my_email, self.my_email, self.msg.as_string())
        self.con.quit()

mail=ErrorEmail()

if __name__ == '__main__':
    #mail=ErrorEmail()
    mail.send("test")