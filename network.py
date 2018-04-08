import requests
import json
from global_variables import *

class Network:
    create_network_post_json = """
        {
          "name": "%s",
          "vlan_id": %d,
          "vswitch_name": "%s"
        }
"""


    name = ""
    vlan = -1
    def __init__(self, name):
        self.name = name

    @staticmethod
    def create_network(name, vlan):
        create_network_url = "/api/nutanix/v2.0/networks/"

        json = (Network.create_network_post_json % (name, vlan, name))
        response = requests.post(base_url + create_network_url,
                                 data=json,
                                 auth=(username,password),
                                 verify=False)
        return Network(name, vlan)
