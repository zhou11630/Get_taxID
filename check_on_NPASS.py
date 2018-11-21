# 这是从GCE查询ID后需要运行的操作
# 第五步：biopython检测结果runing_log.txt检查是否有错误，并去重

f = open("runing_log.txt","r",encoding='utf-8') 
errlines=0
for index,line in enumerate(f.readlines()):
    if line[0]<='9' and line[0]>='0':
        continue
    else:
        print(str(index+1)+'    行有问题')
        errlines=errlines+1
f.close()
print(errlines)
print('end!!!!!')

file文件=open('runing_log.txt','r',encoding='utf-8')
file去重=open('runing_log去重.txt','w',encoding='utf-8')
str文件=file文件.readlines()
str文件.pop() #去除末行
str文件.pop(0) #去除首行
file去重.write('')
str去重=[]
for i in set(str文件):
    file去重.write(i.strip())
    file去重.write(',')
    file去重.write(str(str文件.count(i)))
    file去重.write('\n')
file去重.close()
print('runing_log detective done！')

# 第六步：NPASS爬虫
# csv文件结构：taxID,个数,是否检测到
import requests
import csv
import time

print(time.strftime( '%Y-%m-%d %X', time.gmtime( time.time() ) )+'开始统计')
# 读取数据并进行处理
with open('runing_log去重.txt','r+') as f:
    f_csv = csv.reader(f)
    # headers = next(f_csv) # 文件头
    rows=[]
    # rows.append(headers) # 存储处理结果的数组
    i=0
    for row in f_csv:
        address="http://bidd2.nus.edu.sg/NPASS/"
        checkID=row[0]
        params={'OrganismName':'','OrganismID':checkID,'search_by_organism':'SEARCH'}
        r=requests.post('http://bidd2.nus.edu.sg/NPASS/search_organism.php',data=params)
        halflink=r.text.split('<td><a  target="_blank" href="')
        if(len(halflink)>=2):
            for i1 in halflink[1]:
                if i1!='"':
                    address=address+str(i1)
                else:
                    break
            row.append(len(halflink)-1)
            row.append(address)
            rows.append(row)
        i=i+1
        print('完成'+str(i))
# 将处理完的数据存入文件
with open("result.csv","w",encoding='utf8',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
    f.close()
print(time.strftime( '%Y-%m-%d %X', time.gmtime( time.time() ) )+'结束')
