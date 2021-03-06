import django_tables as tables
from models import Hosts

class HostTable(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    hostname = tables.Column(data = "hostname")
    static_ip = tables.Column(data = "static_ip")
    dhcp_ip = tables.Column(data = "dhcp_ip")
    status = tables.Column(data = "status")
    role = tables.Column(data = "role")

    class Meta:
        model = Hosts 

