# IP address validation and timestamp utility functions
import re
from datetime import datetime

def validate_ip(ip_address):
	"""
	Validates an IPv4 address.
	Returns True if valid, False otherwise.
	"""
	pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
	if pattern.match(ip_address):
		parts = ip_address.split('.')
		return all(0 <= int(part) <= 255 for part in parts)
	return False

def get_timestamp():
	"""
	Returns the current timestamp as a string in YYYY-MM-DD HH:MM:SS format.
	"""
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
