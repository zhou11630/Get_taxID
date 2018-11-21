#_*_coding: utf-8_*_
#!/usr/bin/python

def qq邮箱发送提醒邮件(my_sender,my_pass,my_user,my_title,my_words):
    #!/usr/bin/python
    # -*- coding: UTF-8 -*-
    # this is a function of using qq-email to send you a remind email.
    # you can get your own qq-email pass follow this blog：http://www.runoob.com/python/python-email.html
    # my_sender='sender@qq.com'    # sender`s email 发件人邮箱账号
    # my_pass = '**************'              # the pass you can get from qq-email 发件人邮箱密码
    # my_user='accepter@hotmail.com'      # accepter`s email 收件人邮箱账号，我这边发送给自己
    # my_title='operate done!'     # title of you email 邮件主题为：操作完成

    import smtplib
    import time
    from email.mime.text import MIMEText
    from email.utils import formataddr

    def mail():
        ret=True
        try:
            msg=MIMEText(my_words,'plain','utf-8')
            msg['From']=formataddr(["来自我的GCE服务器",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["my_name",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']=my_title                # 邮件的主题，也可以说是标题

            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret=False
        return ret

    ret=mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

def NCBIpacong(var1):# get taxID from NCBI blast
    from Bio import Entrez
    from Bio.Blast import NCBIWWW, NCBIXML

    Entrez.email = "!!!!!!!!!!@qq.com"     # Always tell NCBI who you are
    fasta_string = var1
    result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)
    blast_record = NCBIXML.read(result_handle)
    E_VALUE_THRESH = 0.04
    text_final=''
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < E_VALUE_THRESH:
                handle = Entrez.efetch(db="nucleotide", id=alignment.hit_id.split('|')[1], rettype="gb", retmode="text")
                text_middle=handle.read()
                str_middle=text_middle.split('/db_xref="taxon:')
                for text_final_check in str_middle[1]:
                    if text_final_check>='0' and text_final_check<='9':
                        text_final=text_final+text_final_check
                    else:
                        return text_final

import time

# 设置通知邮箱信息
my_sender='sender@qq.com'    # 发件人邮箱账号
my_pass = '!!!!!!!!'              # 发件人邮箱密码
my_user='!!!!!!!!@hotmail.com'      # 收件人邮箱账号，我这边发送给自己
my_title='开始计算'     # 邮件主题为：操作完成
my_words=time.asctime( time.localtime(time.time()) )+'开始计算'
# 在第二步中设置运行基因文件名“OTUs.fasta”

# 开始运行程序

# 第一步：记录开始运行时间
my_words1=time.asctime( time.localtime(time.time()) )+'开始计算'+'\n'

# 第二步：从基因文件中读取每个基因组信息
f=open(r'1.1 OTUs.fasta', "r") # important: change this "1.1 OTUs.fasta" to your own fasta file
i=-1#定义基因的序号
jiyinzu_genes=[]#读取的基因组信息
for index,line in enumerate(f.readlines()):#按行遍历文件，将每个基因信息存储到一个数组内；
    if line[0]=='>':
        i=i+1
        jiyinzu_genes.append("")
    else:
        jiyinzu_genes[i]=jiyinzu_genes[i]+line.strip()

# 第三步：用文件中提取出的基因数组jiyinzu_genes，运行biopython查询taxid
taxonomyID=[]   # 定义与基因数组jiyinzu_genes对应的taxid数组
f = open('runing_log1.1 .txt','w')
f.write(time.strftime('%Y-%m-%d',time.localtime(time.time()))+"start to run!!!"+"\n")
f.close()
print(time.strftime('%Y-%m-%d',time.localtime(time.time()))+"start to run!!!"+"\n")
# 3.1 调用biopython查询taxid子程序查询，如果一次查询出错就再查两次
# 3.2 以追加a的方式向日志文件runing_log.txt中添加taxid信息
for index,line in enumerate(jiyinzu_genes):
    try:
        strN=NCBIpacong(line)+"\n"
    except :
        try:
            strN=NCBIpacong(line)+"\n"
        except :
            try:
                strN=NCBIpacong(line)+"\n"
            except :
                strN='wrong detect!'+"\n"
    f = open('runing_log1.1 .txt','a')
    f.write(strN)
    f.close()
    taxonomyID.append(strN)
    print('finished gene detect '+str(index)+', the result coming back is: '+strN)
#将运行的结果保存
f=open('runing_log1.1 .txt','a')
f.write(time.strftime('%Y-%m-%d',time.localtime(time.time()))+"end the running!!!"+"\n")
f.close()

# 第四步：发送操作完成提醒邮件
my_title='完成计算 1.1 '     # 邮件主题为：操作完成
my_words=my_words1+time.asctime( time.localtime(time.time()) )+'完成 1.1 计算!'+'\n'
try:
    qq邮箱发送提醒邮件(my_sender,my_pass,my_user,my_title,my_words)
except :
    try:
        qq邮箱发送提醒邮件(my_sender,my_pass,my_user,my_title,my_words)
    except:
        try:
            qq邮箱发送提醒邮件(my_sender,my_pass,my_user,my_title,my_words)
        except:
            print('TaxID detective all done!')

# # 第五步：biopython检测结果runing_log.txt检查是否有错误，并去重

# f = open("runing_log.txt","r",encoding='utf-8') 
# errlines=0
# for index,line in enumerate(f.readlines()):
#     if line[0]<='9' and line[0]>='0':
#         continue
#     else:
#         print(str(index+1)+'    行有问题')
#         errlines=errlines+1
# f.close()
# print(errlines)
# print('end!!!!!')

# file文件=open('runing_log.txt','r',encoding='utf-8')
# file去重=open('runing_log去重.txt','w',encoding='utf-8')
# str文件=file文件.readlines()
# str文件.pop() #去除末行
# str文件.pop(0) #去除首行
# file去重.write('')
# str去重=[]
# for i in set(str文件):
#     file去重.write(i.strip())
#     file去重.write(',')
#     file去重.write(str(str文件.count(i)))
#     file去重.write('\n')
# file去重.close()
# print('runing_log detective done！')

# # 第六步：NPASS爬虫
# # csv文件结构：taxID,个数,是否检测到
# import requests
# import csv
# import time

# print(time.strftime( '%Y-%m-%d %X', time.gmtime( time.time() ) )+'开始统计')
# # 读取数据并进行处理
# with open('runing_log去重.csv','r+') as f:
#     f_csv = csv.reader(f)
#     headers = next(f_csv) # 文件头
#     rows=[]
#     rows.append(headers) # 存储处理结果的数组
#     i=0
#     for row in f_csv:
#         address="http://bidd2.nus.edu.sg/NPASS/"
#         checkID=row[0]
#         params={'OrganismName':'','OrganismID':checkID,'search_by_organism':'SEARCH'}
#         r=requests.post('http://bidd2.nus.edu.sg/NPASS/search_organism.php',data=params)
#         halflink=r.text.split('<td><a  target="_blank" href="')
#         for i1 in halflink[1]:
#             if i1!='"':
#                 address=address+str(i1)
#             else:
#                 break
#         row.append(len(halflink)-1)
#         row.append(address)
#         rows.append(row)
#         i=i+1
#         print('完成'+str(i))
# # 将处理完的数据存入文件
# with open("result.csv","w",encoding='utf8',newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(rows)
#     f.close()
# print(time.strftime( '%Y-%m-%d %X', time.gmtime( time.time() ) )+'结束')
