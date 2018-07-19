from settings import *
import platform, os, subprocess, sys


def scan_ip(hosts, port=80):
    """
    扫描指定网段主机，并把扫描结果追加到文件中
    :param hosts:  网段  1.1.1.0/24
    :param port:  扫描端口，默认80
    :return:
    """
    print('开始扫描%s任务添加到任务队列' % hosts)
    hosts = hosts.strip()
    ip_file_name_tmp = os.path.join(OPEN_80_FILE_DIRS, '%s—tmp.txt' % hosts.replace('/', '-').strip())

    cmd = '%s %s -p80 -oL %s --randomize-hosts --rate=1000' % (MASSCAN_PATH, hosts, ip_file_name_tmp)
    print(cmd)
    os.system(cmd)
    ip_file_name = os.path.join(OPEN_80_FILE_DIRS, '%s.txt' % hosts.replace('/', '-').strip())
    with open(ip_file_name_tmp, 'r') as tmp:
        data = tmp.readlines()
        print(len(data))
        if len(data) is not 0:
            with open(ip_file_name, 'a+') as ip_file:
                for i in data:
                    if i.startswith('open'):
                        ip_file.write(i.split()[3] + '\n')
            print('扫描%s任务完成文件存储在------> %s' % (hosts, ip_file_name))
    os.remove(ip_file_name_tmp)


def main():
    globals_ip_file = open(GLOBALLS_IP_FILE_PATH, 'r')
    for i in globals_ip_file.readlines():
        scan_ip(hosts=i)


if __name__ == '__main__':
    main()
