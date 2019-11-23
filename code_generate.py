#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import os	


# Mysql连接
class DB():
	def __init__(self, host='localhost', port=3306, db='', user='root', passwd='root', charset='utf8'):
		# 建立连接 
		self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
		# 创建游标，操作设置为字典类型        
		#self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
		# 游标元组类型
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


# 生成文件
def generate(path,fetch):
	entity_path = path + "\\enity"
	repository_path = path + "\\repository" 
	create_dir(entity_path,"")
	create_dir(repository_path,"")

	for i in fetch:
		table_name = formatter(i[0]);
		db.execute("describe "+i[0])
		fields = db.fetchall()
		content = jpa_entity(table_name,fields)
		create_file(entity_path+"\\"+table_name,content)
		re_content = jpa_repository(table_name,fields)
		#print(re_content)
		create_file(repository_path+"\\"+table_name+"Repository",re_content)


# 创建文件夹
def create_dir(path: str ,appendir: str):
	isExists=os.path.exists(path)
	if not isExists:
		# 如果不存在则创建目录
		# 创建目录操作函数
		if appendir != "":
			path += appendir
		os.makedirs(path) 
		(path+' created success.')
	return 


# 创建文件
def create_file(filename,content):
	suffix = ".java"
	newfile= filename+suffix
	if not os.path.exists(newfile):
		f = open(newfile,'w+')
		f.write(content)
		f.close()
		print(newfile + " created.")
	else:
		print(newfile + " already existed.")
	return


# Jpa实体类文件模板内容
def jpa_entity(filename,cloums):
	packages =[
		"package com.xxy.yd.common.entity;\r",
		"import lombok.Data;\r"
		"import javax.persistence.*;\r"
		"import java.io.Serializable;\r"	
	] 
	class_annotaion = [
		"@Entity\r",
		"@Data\r",
	]
	primary_key = [
		"\t@GeneratedValue(strategy=GenerationType.IDENTITY)\r",
		"\t@Id\r",
	]
	class_name = [
		"public class ",
		filename,
		" implements Serializable{\r "
	]

	footer = [
		"}"
	]




	# 存储字段
	fileds = []

	# 写入字段
	for val in cloums:
		field = [
			"\tprivate ",
		]
		key_name = formatter(val[0],False)
		java_type = sqlType2JavaType(val[1])
		if java_type == "Date" and "import java.util.Date;\r" not in packages:
			packages.append("import java.util.Date;\r")
		
		field.append(java_type)
		field.append(" ")
		field.append(key_name)
		field.append("; \r")
		fileds+=field


	packages.append(" \r")
	content = packages+class_annotaion+class_name+primary_key+fileds

	content+=footer
	file_content = "".join(content)
	return file_content


# Jpa repositoty
def jpa_repository(table_name,cloums):
	id_key = sqlType2JavaType(cloums[0][1])
	print(id_key)
	packages = [
		"package com.xxy.yd.usermanage.dao.repository;\r",
		"import org.springframework.data.jpa.repository.JpaRepository;\r",
		"import org.springframework.data.repository.NoRepositoryBean;\r",
		"import com.xxy.yd.common.entity."+table_name+";\r",
		"\r",
	]

	class_annotaion = [
		"@NoRepositoryBean\r",

	]

	class_name = [
		"public interface ",
		table_name+"Repository ",
		"extends JpaRepository<"+table_name+","+id_key+"> {\r\n}"
	]
	content = packages+class_annotaion+class_name
	return "".join(content)


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



# 判断引用类型添加包
def reference_type(java_type):
	if java_type == "Date":
		return "import java.util.Date;\r"
	if java_type == "List":
		return "import java.util.List;\r"
	if java_type == "Map":
		return "import java.util.Map;\r"
	return None



if __name__ == '__main__':
	with DB(host='host',user='user',passwd='psd',db='databas') as db:
		db.execute('SHOW TABLES')
		# 所有表信息
		fetch = db.fetchall()
		# 文件输入文件夹
		path = "c:\\Users\\tars\\Desktop\\auto_code"
		generate(path,fetch)
