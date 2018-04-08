import requests
import json
from global_variables import *

class VM:
    # instance variables
    vm_dict = {}
    name = ""
    uuid = ""

    #static variables
    set_power_state_json = """
    {
      "transition": "%s",
      "uuid": "%s"
    }
    """

    create_vm_post_json = """
        {
           "description":"test",
           "guest_os":"%s",
           "memory_mb":%d,
           "name":"%s",
           "num_cores_per_ vcpu":1,
           "num_vcpus":%d,
           "vm_disks":[
              {
                 "disk_address":{
                    "device_bus":"ide",
                    "device_index":0
                 },
                 "is_ cdrom":true,
                 "is_empty":false,
                 "vm_disk_clone":{
                    "disk_address":{
                       "vmdisk_uuid":"%s"
                    }
                 }
              },
              {
                 "disk_address":{
                    "device_bus":"scsi",
                    "device_index":0
                 },
                 "vm_disk_create":{
                    "storage_container_uuid":"%s",
                    "size":10737418240
                 }
              },
              {
                 "disk_address":{
                    "device_bus":"ide",
                    "device_index":1
                 },
                 "is_ cdrom":true,
                 "is_empty":false,
                 "vm_disk_clone":{
                    "disk_address":{
                       "vmdisk_uuid":"%s"
                    }
                 }
              }
           ],
           "hypervisor_type":"ACROPOLIS",
           "affinity":null
        }
    """
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid

    def set_power_state(self, power_state):
        set_power_state_url = "/api/nutanix/v2.0/vms/%s/set_power_state/"
        json = (set_power_state_json %(power_state.upper(), self.uuid))

        response = requests.post(base_url + set_power_state_url % uuid,
                                 data = json,
                                 auth = (username,password),
                                 verify=False)

        if response.status_code == 201:
            return 0
        else:
            return reponse.status_code

    def get_ips(self):
        get_vms_v1_url = "/PrismGateway/services/rest/v1/vms/"
        response = requests.get(base_url + get_vms_v1_url,
                                auth = (username,password),
                                verify = False)

        parsed_json = json.loads(response.text)
        ips = []
        vm_found = False
        for vm in parsed_json["entities"]:
            if vm["uuid"] == self.uuid:
                vm_found = True
                ips = vm["ipAddresses"]

        if vm_found == True:
            return ips
        else:
            raise Exception("VM not found in V1 APIs using url: %s" % get_vms_v1_url)


    def delete(self):
        delete_vm_url = "/api/nutanix/v2.0/vms/%s/"

        return requests.delete(base_url + delete_vm_url % self.uuid(self.name),
                           auth=(username,password),
                           verify=False)

    @staticmethod
    def get_vms():
        get_vms_url = "/api/nutanix/v2.0/vms/"

        response = requests.get(base_url + get_vms_url,
                                auth=(username, password),
                                verify=False)
        parsed_json = json.loads(response.text)
        vm_list = []
        for vm in parsed_json["entities"]:
            vm_list.append(VM(vm["name"], vm["uuid"]))
        return vm_list

    @staticmethod
    def get_vm(name):
        get_vms_url = "/api/nutanix/v2.0/vms/"

        vm_response_json = VM.get_vms().text
        parsed_json = json.loads(vm_response_json)

        vm_json = None
        for vm in parsed_json["entities"]:
            if vm["name"] == name:
                vm_json = vm

        if vm_json == None:
          raise Exception("No value returned for vm %s"% name)
        else:
          return VM(vm_json["name"], vm_json["uuid"])

    @staticmethod
    def create_windows_vm(os_name, vm_name, num_cpus, mem_mb, disk_container_uuid,
                  disk_image_uuid, virtio_image_uuid):
        create_vm_url = "/api/nutanix/v2.0/vms/"

        json = (create_vm_post_json % (os_name, mem_mb, vm_name, num_cpus,
                                       disk_image_uuid, disk_container_uuid,
                                       virtio_image_uuid))
        return requests.post(base_url + create_vm_url,
                            data=json,
                            auth=(username,password),
                            verify=False)

    #@staticmethod
    #def create_vm_from_qcow2(os_name, vm_name, num_cpus, mem_mb, disk_container_uuid)

    @staticmethod
    def get_vm_uuid(vm_name):
        vm_response_json = get_vms().text
        parsed_json = json.loads(vm_response_json)

        uuid = None
        for vm in parsed_json["entities"]:
            if vm["name"] == vm_name:
                uuid = vm["uuid"]

        if uuid == None:
            raise Exception("No value returned for vm %s"% vm_name)
        else:
            return uuid
