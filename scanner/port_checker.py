# Port checking utility functions


def check_port_status(port):
	common_ports = {22, 80, 443, 3306, 8080}
	return "OPEN" if port in common_ports else "CLOSED"


def is_privileged(port):
	return 0 <= port <= 1023
