import ipaddress
import os

# Internal IPs (required for Django Debug Toolbar)
# https://docs.djangoproject.com/en/stable/ref/settings/#internal-ips


class IPv4List(list):
    """IPv4 addresses from CIDR."""

    def __init__(self, cidr):
        super().__init__()
        self.network = ipaddress.IPv4Network(cidr)

    def __contains__(self, ip):
        return ipaddress.IPv4Address(ip) in self.network


INTERNAL_IPS = IPv4List(os.environ.get("INTERNAL_IP_CIDR", "127.0.0.1/32"))
