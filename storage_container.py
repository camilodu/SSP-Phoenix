import requests
import json
from global_variables import *

class StorageContainer:
    storage_container_dict = {}
    name = ""
    uuid = ""

    storage_container_patch_json = """
        {
            "name": "%s",
            "compression_enabled": %s,
            "storage_container_uuid": "%s"
        }
        """

    def __init__(self, storage_container_dict):
        self.storage_container_dict = storage_container_dict
        self.name = storage_container_dict["name"]
        self.uuid = storage_container_dict["storage_container_uuid"]

    def enable_compression(self, enable_compression = True, compression_delay = 0):
        patch_storage_container_url = "/api/nutanix/v2.0/storage_containers/"

        json = StorageContainer.storage_container_patch_json % (self.name,
                                                                #compression_delay,
                                                                str(enable_compression).lower(),
                                                                self.uuid)
        #print json
        response = requests.put(base_url + patch_storage_container_url,
                                data=json,
                                auth=(username,password),
                                verify=False)
        return response.response_code

    @staticmethod
    def get_storage_containers():
        get_storage_container_url = "/api/nutanix/v2.0/storage_containers/"
        response = requests.get(base_url + get_storage_container_url,
                            auth=(username, password),
                            verify=False)

        storage_containers = []
        for storage_container in json.loads(response.text)["entities"]:
            storage_containers.append(StorageContainer(storage_container))

        return storage_containers

    @staticmethod
    def get_storage_container(storage_container_name):
        containers = StorageContainer.get_storage_containers()
        storage_container = None
        print containers
        for container in containers:
            if container.name == storage_container_name:
                storage_container = container

        if storage_container == None:
            raise Exception("No value returned for storage container %s"% storage_container_name)
        else:
            return storage_container
