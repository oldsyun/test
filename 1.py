# _*_ coding:utf-8 _*_

# ----------------------------------------------------------------------------
# import modules 
# ----------------------------------------------------------------------------
import time,datetime
import requests
import re,os
import smtplib
import xlwt,xlrd
from xlutils.copy import copy
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.application import MIMEApplication 

def src_dir():
    return os.path.dirname(os.path.realpath(__file__))

def set_style(name, height, bold = False):
	style = xlwt.XFStyle()   #初始化样式
	font = xlwt.Font()       #为样式创建字体
	font.name = name
	font.bold = bold
	font.color_index = 4
	font.height = height
	style.font = font
	return style

def set_pattern(num):
	pattern = xlwt.Pattern() # Create the Pattern
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern.pattern_fore_colour = num # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
	style = xlwt.XFStyle() # Create the Pattern
	style.pattern = pattern # Add Pattern to Style
	return style

def spyd():
	s = requests.Session()
	headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, compress',
				'Accept-Language': 'en-us;q=0.5,en;q=0.3',
				'Cache-Control': 'max-age=0',
				'Connection': 'keep-alive',
				'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	s.headers.update(headers)
	url1 = 'http://www.riyuecloud.com/Terminal/TerminalMain.aspx?pid=20'
	url2 = 'http://www.riyuecloud.com/AjaxService.ashx?ac=changeList&page=1&order=&upper=&type=&sitename=&country=&province=&city=&from=&to=&random=0.8201823006998097'
	s.get(url1)
	html_doc = s.get(url2)
	#print (html_doc.text)
	pa = re.compile('<tr.*?<td><a title=\'(.*?)\' ><img .*?></a></td><td>.*?</td><td><a href=.*?>(.*?)</a></td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td><td>.*?</td><td>&yen;.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td></tr>',re.S)
	items = re.findall(pa, html_doc.text)
   # print (items)
	return items

	
def update_excel(num):
	workbook = xlrd.open_workbook(src_dir()+'\\'+datetime.datetime.now().strftime("%Y%m")+'.xls',formatting_info=True)
	#workbook = xlrd.open_workbook(r'd:\13\\'+'+.xls',formatting_info=True)
	#print (datetime.datetime.now().strftime("%Y%m")+'.xls')
	item = spyd()
	newWb = copy(workbook)
	newWs = newWb.get_sheet(0)
	day = datetime.datetime.now().day
	newWs.write(0,day+2, day, set_style('Arial', 220, False))
	#print (day)
	for j in range(len(item)):
		if item[j][0] == "工作正常":
			newWs.write(8*j+6+num,day+2, item[j][0], set_pattern(3))
			newWs.write(8*j+2+num,day+2, item[j][2], set_style('Arial', 220, False))
			#newWs.write(8*j+2+num,day+3, item[j][1], set_style('Arial', 220, False))
		else:
			if item[j][0] == "通信中断":
				newWs.write(8*j+6+num,day+2, item[j][0], set_pattern(2))
				newWs.write(8*j+2+num,day+2, item[j][2], set_style('Arial', 220, False))
				#newWs.write(8*j+2+num,day+3, item[j][1], set_style('Arial', 220, False))
			else:
				if item[j][0] == "逆变器报警":
					newWs.write(8*j+6+num,day+2, item[j][0], set_pattern(5))
					newWs.write(8*j+2+num,day+2, item[j][2], set_style('Arial', 220, False))
					#newWs.write(8*j+2+num,day+3, item[j][1], set_style('Arial', 220, False))
	newWb.save(src_dir()+'\\'+datetime.datetime.now().strftime("%Y%m")+'.xls')

def f1():
	now = datetime.datetime.now()
	if now.strftime("%m") == '01':
		f1=(datetime.datetime(now.year-1,12,now.day).strftime("%Y%m"))
	else:
		f1=(datetime.datetime(now.year,(now.month-1),now.day).strftime("%Y%m"))
	return f1
	
def send_mail():	
#第三方SMTP服务
	mail_host = "smtp.qq.com"           # 设置服务器
	mail_user = "steedyu@qq.com"        # 用户名
	mail_pwd  = "xxxxxxxx"      # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
	mail_to  = ['steedyu@163.com']     #接收邮件列表,是list,不是字符串
	msg = MIMEMultipart() 

#邮件内容

	msg['Subject'] = "常熟开关制造有限公司太阳能发电"+f1()+"统计表"     # 邮件标题
	msg['From'] = mail_user        # 发件人
	msg['To'] = ','.join(mail_to)         # 收件人，必须是一个字符串
	part = MIMEText(f1()+'.xls'+"统计表")      # 邮件正文
	msg.attach(part)

	part = MIMEApplication(open(f1()+'.xls','rb').read())  
	part.add_header('Content-Disposition', 'attachment', filename=f1()+'.xls')  
	msg.attach(part)

	try:
		smtpObj = smtplib.SMTP_SSL(mail_host, 465)
		smtpObj.login(mail_user, mail_pwd)
		smtpObj.sendmail(mail_user,mail_to, msg.as_string())
		smtpObj.quit()
		print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"邮件发送成功!")
	except smtplib.SMTPException:
		print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"邮件发送失败!")
		
def add_excel():	
workbook = xlrd.open_workbook(src_dir()+'\\'+'xx.xls',formatting_info=True)
	newWb = copy(workbook)
	newWs = newWb.get_sheet(0)
	send_mail()
	#保存文件
	newWb.save(src_dir()+'\\'+datetime.datetime.now().strftime("%Y%m")+'.xls')

if __name__ == '__main__':
        
        while True:
                current_time = time.localtime(time.time())
                if((datetime.datetime.now().day == 1) and (current_time.tm_hour == 7 ) and (current_time.tm_min == 30) and (current_time.tm_sec == 0)):
                        add_excel()
						
                else:
                        if((current_time.tm_hour == 8) and (current_time.tm_min == 30) and (current_time.tm_sec == 0)):
                            update_excel(0)
                            print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'   ok')
                        else:
                                if((current_time.tm_hour == 11) and (current_time.tm_min == 30) and (current_time.tm_sec == 0)):
                                        update_excel(1)
                                        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'   ok')
                                else:
                                        if((current_time.tm_hour == 13) and (current_time.tm_min == 30) and (current_time.tm_sec == 0)):
                                                update_excel(2)
                                                print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'   ok')
                                        else:
                                                if((current_time.tm_hour == 15 ) and (current_time.tm_min == 30) and (current_time.tm_sec == 0)):
                                                        update_excel(3)
                                                        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'   ok')
                                                else:
                                                        time.sleep(1)
    
