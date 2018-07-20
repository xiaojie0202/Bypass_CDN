from settings import *
import platform, os, subprocess, sys
from concurrent.futures import ProcessPoolExecutor

def scan_ip(hosts, port=80):
    """
    扫描指定网段主机，并把扫描结果追加到文件中
    :param hosts:  网段  1.1.1.0/24
    :param port:  扫描端口，默认80
    :return:
    """
    hosts = hosts.strip()
    # masscan 输入存放的文件
    ip_file_name_tmp = os.path.join(OPEN_80_FILE_DIRS, '%s—tmp.txt' % hosts.replace('/', '-').strip())
    # 处理完masscan输出文件内容后存放的文件
    ip_file_name = os.path.join(OPEN_80_FILE_DIRS, '%s.txt' % hosts.replace('/', '-').strip())

    print('[>]开始扫描%s任务添加到任务队列' % hosts)
    # mascan 执行的命令
    cmd = '%s %s -p80 -oL %s --randomize-hosts --rate=%s' % (MASSCAN_PATH, hosts, ip_file_name_tmp, RATE)
    os.system(cmd)

    with open(ip_file_name_tmp, 'r') as tmp:
        data = tmp.readlines()
        print('[>]网段%s扫描到%s个开放80端口的IP' % (hosts, len(data)))
        if len(data) is not 0:
            with open(ip_file_name, 'a+') as ip_file:
                for i in data:
                    if i.startswith('open'):
                        ip_file.write(i.split()[3] + '\n')
    os.remove(ip_file_name_tmp)
    print('[>]扫描%s结果 %s' % (hosts, ip_file_name))


def main():
    pool = ProcessPoolExecutor(SCAN_PROCESS)
    globals_ip_file = open(GLOBALLS_IP_FILE_PATH, 'r')
    for i in globals_ip_file.readlines():
        pool.submit(scan_ip, hosts=i)


if __name__ == '__main__':
    main()
