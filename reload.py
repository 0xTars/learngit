# -*- coding: UTF-8 -*-
import os
import time



# 日志装饰器
def log(method_name):
    def decorator(func):
        def wrapper(*args, **kw):
            content = "执行函数：[{0}],参数为：{1}".format(method_name,args)
            print(content)
            write_log(content)
            return func(*args, **kw)
        return wrapper
    return decorator


# 杀死进程
@log("杀死进程")
def kill(pid):
    try:
        a = os.kill(pid,signal.SIGKILL)
        print("已经杀死pid为%s的进程，返回值是:%s"%(pid,a))
    except Exception as e:
        error_log = "没有此进程pid[{0}]！".format(pid)
        print(error_log)
        write_log(error_log)


# 根据端口查找进程pid	
@log("查找进程")
def find_pid(server_port):
    print("查找端口为[%d]的服务进程pid"%server_port)
    pid=os.popen("netstat -anp|grep %d |awk '{print $7}'"%server_port).read().split('/')[0]
    if pid == "" or pid == None:
        error_log = "未通过端口：[{0}]查找到pid".format(server_port)
        print(error_log)
        write_log(error_log)
        print("服务进程pid为：%d",pid)
    return pid


# 写入日志
def write_log(content):
    with open(file_name,'a+') as file_obj:
        file_obj.write(content)



if __name__ == '__main__':
# 初始化条件
	path = "/"
	linux_command = "mvn clear install"
	docker_command = "mvn clear install docker:build"
	log_time = time.localtime()
	file_name = str(log_time) + "\t启动日志.log"
	port = 8080
	dev = True

	exis = os.path.exists(path)
	if exis-1:
		print time.strftime("%Y-%m-%d %H:%M:%S", log_time) 
		print("未找到指定文件夹！")
		exit()

	pwd = os.getcwd()
	print("当前所在路径：%s"%pwd)


	if dev:
		command = linux_command
	else:
		command = docker_command

	# 执行打包启动
	kill(find_pid(port))
	content = os.popen(command)
	write_log(content.readlines())
	exit()
