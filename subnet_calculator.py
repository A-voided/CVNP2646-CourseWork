import argparse
import ipaddress
import sys


def _parse_net(ip, mask=None):
	if mask:
		return ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
	return ipaddress.IPv4Network(ip, strict=False)


def _class_from_ip(ipv4):
	o = int(str(ipv4).split('.')[0])
	if 1 <= o <= 127:
		return 'A'
	if 128 <= o <= 191:
		return 'B'
	if 192 <= o <= 223:
		return 'C'
	return 'Other'


def main(argv=None):
	argv = argv if argv is not None else sys.argv[1:]
	p = argparse.ArgumentParser(description='Subnet summary')
	p.add_argument('ip')
	p.add_argument('netmask', nargs='?')
	a = p.parse_args(argv)
	try:
		net = _parse_net(a.ip, a.netmask)
	except Exception as e:
		print('Error:', e); return 2
	prefix = net.prefixlen
	total = 1 << (32 - prefix)
	usable = total - 2 if total >= 2 else 0
	try:
		host_ip = ipaddress.IPv4Address(a.ip.split('/')[0])
	except Exception:
		host_ip = net.network_address
	print(f'Total IP addresses: {total}')
	print(f'Usable host IPs: {usable}')
	print(f'Network class: {_class_from_ip(host_ip)}')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())

