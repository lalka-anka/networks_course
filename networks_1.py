import subprocess
import re
import argparse


def routing(hostname):
    ips = dict()
    traceroute = subprocess.Popen(["traceroute", hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(traceroute.stdout.readline, ""):
        if len(line) < 20:
            traceroute.kill()
            traceroute.terminate()
            break
        if re.match(r'\s\d+', line.decode('utf-8')):
            number = int(re.match(r'\s\d+', line.decode('utf-8')).group(0))
            ip = (re.split(r'[()]', line.decode('utf-8')))[1]
            as_info = whois(ip)
            ips[number] = (ip, as_info)

    return ips


def whois(ip):
    args = ['whois', ip]
    info = subprocess.run(args, stdout=subprocess.PIPE, encoding='utf-8').stdout
    if re.findall(r'AS\d+', info):
        return re.findall(r'AS\d+', info)[0]
    else:
        return '--'


def print_result(result):
    print('№ по порядку     IP                AS')
    for i in range(1, len(result)+1):
        n = 17 - len(str(i))
        p = 15 - len(str(result[i][0]))
        first_space = ' ' * n
        second_space = ' ' * p + ' ' * 3
        st = str(i) + first_space + str(result[i][0]) + second_space + str(result[i][1])
        print(st)


def parsing():
    parser = argparse.ArgumentParser(description='Трассировка автономных систем; выполнила Ильина Анна кн-202 (мен-280207)')
    parser.add_argument('-dm', '--domain', type=str, metavar='', help='Ip/domain for tracing')
    args = parser.parse_args()
    ip = args.domain
    if ip:
        return ip
    else:
        return input('Enter ip/domain: ')


if __name__ == '__main__':
    host = parsing()
    print_result(routing(host))
