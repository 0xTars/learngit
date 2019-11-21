#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import os	

class DB():
	def __init__(self, host='localhost', port=3306, db='', user='root', passwd='root', charset='utf8'):
		# 建立连接 
		self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
		# 创建游标，操作设置为字典类型        
		#self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()


	def __enter__(self):
		# 返回游标 
			# fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
		# fetchall(): 接收全部的返回结果行.
		# rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。       
		return self.cursor

	def __exit__(self, exc_type, exc_val, exc_tb):
		# 提交数据库并执行        
		self.conn.commit()
		# 关闭游标        
		self.cursor.close()
		# 关闭数据库连接        
		self.conn.close()


def generate(path,fetch):
	
	ceate_dir(path)

	for i in fetch:
		table = formatter(i[0]);
		db.execute("describe "+i[0])
		fields = db.fetchall()
		content = jpa_content(table,fields)
		create_file(path+"\\"+table,content)


	

# 创建文件夹
def ceate_dir(path):
	isExists=os.path.exists(path)
	if not isExists:
		# 如果不存在则创建目录
		# 创建目录操作函数
		os.makedirs(path) 
		(path+' 创建成功')
	return 

# 创建文件
def create_file(filename,content):
	'''根据本地时间创建新文件，如果已存在则不创建'''
	import time
	t = time.strftime('%Y-%m-%d',time.localtime())  #将指定格式的当前时间以字符串输出
	suffix = ".java"
	newfile= filename+suffix
	if not os.path.exists(newfile):
		f = open(newfile,'w')
		f.write(content)
		f.close()
		print(newfile + " created.")
	else:
		print(newfile + " already existed.")
	return


# 文件模板内容
def jpa_content(filename,cloums):
	packages =[
		"package com.xxy.yd.usermanage.entity;\r"
		"import lombok.Data;\r"
		"import javax.persistence.*;\r"
		"import java.io.Serializable;\r"
		" \r "
	] 
	class_annotaion = [
		"@Entity\r ",
		"@Data\r ",
	]
	primary_key = [
		"\t@GeneratedValue(strategy=GenerationType.IDENTITY)\r ",
		"\t@Id\r ",
	]
	class_name = [
		"public class ",
		filename,
		" implements Serializable{\r "
	]

	footer = [
		"}"
	]


	
	content = packages+class_annotaion+class_name+primary_key
	# 写入字段
	for c in cloums:
		fields = [
			"\tprivate ",
		]
		key_name = formatter(c[0],False)
		java_type = sqlType2JavaType(c[1])
		
		fields.append(java_type)
		fields.append(" ")
		fields.append(key_name)
		fields.append("; \r ")
		content+=fields

	content+=footer
	s = "".join(content)
	print(s)
	return s


# 将下划线分隔的名字,转换为驼峰模式
def formatter(src: str, firstUpper: bool = True):
	"""
	将下划线分隔的名字,转换为驼峰模式
	:param src:
	:param firstUpper: 转换后的首字母是否指定大写(如
	:return:
	"""
	arr = src.split('_')
	res = ''
	for i in arr:
		if i is None or i == "":
			return res
		res = res + i[0].upper() + i[1:]

	if not firstUpper:
		res = res[0].lower() + res[1:]
	return res


# mysql类型转java包装类型
def sqlType2JavaType(sqlType):
	if sqlType.startswith("varchar") or sqlType.startswith("text"):
		return "String"
	if sqlType.startswith("char"):
		return "Char"
	if sqlType.startswith("int") or sqlType.startswith("tinyint"):
		return "Integer"
	if sqlType.startswith("bigint"):
		return "Long"
	if sqlType.startswith("float") or sqlType.startswith("double") or sqlType.startswith("decimal"):
		return "Double"
	if sqlType.startswith("bit") or sqlType.startswith("boolean"):
		return "Boolean"
	if sqlType.startswith("date") or sqlType.startswith("time") or sqlType.startswith("datatime") or sqlType.startswith("timestamp"):
		return "Date"




if __name__ == '__main__':
	with DB(host='host',user='username',passwd='psd',db='database') as db:
		db.execute('SHOW TABLES')
		fetch = db.fetchall()
		path = "c:\\Users\\tars\\Desktop\\entity"
		generate(path,fetch)
