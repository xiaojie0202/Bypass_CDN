import requests
from settings import *
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

lock = Lock()

comparison_domain_file = open(COMPARISON_DOMAIN, 'a+', encoding='utf-8')


def save_domian_to_file(futuer):
    data = futuer.result()
    respones = data['response']
    ip = data['ip']
    domain = data['domain']
    if respones.status_code == 200:
        if respones.text.find(data['gzj']) != -1:
            lock.acquire()
            comparison_domain_file.write('%s\t%s\n' % (ip, domain))
            comparison_domain_file.flush()
            print('[>]%s\t%s对比成功' % (ip, domain))
            print('写入文件', '%s\t%s\n' % (ip, domain))
            lock.release()


def handel_domain(domain, ip, gjz):
    """
    访问指定ip的80端口，并绕过cdn使用指定host取访问
    :param domain:
    :param ip:
    :return:
    """
    headers = {
        'Host': domain,
        'Referer': 'http://{0}/'.format(domain),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    domain = domain.strip()
    ip = ip.strip()
    print('[>]正在对比:%s------------>%s' % (ip, domain))
    try:
        response = requests.get(url='http://{0}'.format(ip), headers=headers)
    except Exception as e:
        response = lambda x: x
        response.status_code = 502
    data = {'response': response, 'ip': ip, 'domain': domain, 'gzj': gjz}
    return data


if __name__ == '__main__':
    # 存放域名的文件
    domain_file = open(DOMAIN_FILE_PATH, 'r', encoding='utf-8')
    # open80端口的所有文件
    open_80_files = [os.path.join(OPEN_80_FILE_DIRS, i) for i in os.listdir(OPEN_80_FILE_DIRS)]
    pool = ThreadPoolExecutor(COMPARISON_THREAD)
    for domain_gj in domain_file.readlines():
        domain, gjz = domain_gj.strip().split('----')
        for ip_file_path in open_80_files:
            with open(ip_file_path, 'r') as ip_file:
                for i in ip_file.readlines():
                    futuer = pool.submit(handel_domain, domain=domain, ip=i, gjz=gjz)
                    futuer.add_done_callback(save_domian_to_file)
    pool.shutdown()
    print('[>]对比域名结果完成，请查看%s' % COMPARISON_DOMAIN)
