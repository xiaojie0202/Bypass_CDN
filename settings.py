import os, platform
system = platform.system()

# 程序根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 全球IP网段的文件
GLOBALLS_IP_FILE_PATH = os.path.join(BASE_DIR, 'res', 'global_ip.txt')

# 存放域名的文件
DOMAIN_FILE_PATH = os.path.join(BASE_DIR, 'res', 'domain.txt')
# 存放域名对比结果的文件
COMPARISON_DOMAIN = os.path.join(BASE_DIR, 'res', 'comparison_domain.txt')

# masscan文件位置
MASSCAN_PATH = os.path.join(BASE_DIR, 'bin', 'windows_64', 'masscan.exe') if system == 'Windows' else 'masscan'

# 存放开放80端口IP文件夹
OPEN_80_FILE_DIRS = os.path.join(BASE_DIR, 'res', 'open80_dir')

# 每秒发的数据包个数
RATE = 100000

# HOSTS对比的时候线程数
COMPARISON_THREAD = 1000