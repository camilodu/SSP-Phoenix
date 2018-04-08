import requests
import urllib2
import base64
import json
import socket
import sys
import pprint
import time
import re
from tasks import Tasks
from flask import redirect
from health_checks import HealthChecks
from vm import VM
from storage_container import StorageContainer
from network import Network
from blueprint import Blueprint

#Variables for create VM customization
vm_name= "W2K12R2-API"
vm_ram="4096"
vm_coresxcpu="2"

#variables for requests urls
service_url = "https://10.68.69.102:9440/PrismGateway/services/rest/v2.0/"
vms_url="vms/"
getvm_url="vms/?include_vm_disk_config=true&include_vm_nic_config=true"
poweron_url="/set_power_state/"
uuid=""
payloadCreateVM = '{\n\t\"description\": \"Tech Summit 2017\",\n\t\"guest_os\": \"Windows Server 2012 R2\",\n\t\"memory_mb\": %s,\n\t\"name\": \"%s",\n\t\"num_cores_per_vcpu\": %s,\n\t\"num_vcpus\": 1,\n\t\"vm_disks\": [\n{\n\t\t\"disk_address\": {\n\t\t\t\"device_bus\": \"ide\",\n\t\t\t\"device_index\": 0\n\t\t},\n\t\t\"is_cdrom\": true,\n\t\t\"is_empty\": false,\n\t\t\"vm_disk_clone\": {\n\t\t\t\"disk_address\": {\n\t\t\t\t\"vmdisk_uuid\": \"54d1c16b-4341-44e7-aa17-cd8a7972626b\"\n\t\t\t}\n\t\t}\n\t}, \n{\n\t\t\"disk_address\": {\n\t\t\t\"device_bus\": \"scsi\",\n\t\t\t\"device_index\": 0\n\t\t},\n\t\t\"vm_disk_create\": {\n\t\t\t\"storage_container_uuid\": \"cbad2d71-ff2a-4707-8f88-c98ecd70c237\",\n\t\t\t\"size\": 10737418240\n\t\t}\n\t}, \n{\n\t\t\"disk_address\": {\n\t\t\t\"device_bus\": \"ide\",\n\t\t\t\"device_index\": 1\n\t\t},\n\t\t\"is_cdrom\": true,\n\t\t\"is_empty\": false,\n\t\t\"vm_disk_clone\": {\n\t\t\t\"disk_address\": {\n\t\t\t\t\"vmdisk_uuid\": \"03c47aa6-0acd-4c7e-baf5-2867e9984b2a\"\n\t\t\t}\n\t\t}\n\t}],\n\t\"hypervisor_type\": \"ACROPOLIS\",\n\t\"affinity\": null\n}' % (vm_ram, vm_name, vm_coresxcpu)
payloadPowerOnVM = "{\n  \"transition\": \"ON\",\n  \"uuid\": \"b6e49497-4986-4650-9325-c949636d7412\"\n}"


def getvm(user,password):
    vm=requests.get(service_url+getvm_url,auth=(user, password),verify= False)
    flash(vm.text)
    #flash(vm.text)
    return()

def create1vm (user,password):
    print "la voy a crear"
    vm=requests.post(service_url+vms_url,data=payloadCreateVM, auth=(user, password),verify= False)
    print vm.text
    flash(vm.text)
    return()

def poweronvm (user,password):
    vm=requests.post(service_url+uuid+poweron_url,data=payloadPowerOnVM, auth=(user, password),verify= False)
    flash(vm.text)
    return()

def getuuid(user,password):
    vm=requests.get(service_url+getvm_url,auth=(user, password),verify= False)
    uuid=vm.text
    vm = re.search('uuid',uuid)
    flash(vm)
    return()

# We will enable the webserver on TCP port 5000
# It is required to install pip and after it to install Flask
#1. Download pip installer script from  https://pip.pypa.io/en/latest/installing/python get-pip.py
#2. sudo python get-pip.py
#3. Install flask : sudo pip install flask
#4. Install wtforms: sudo pip install wtforms
#4. Install virtual environments: sudo pip install virtualenv
#Flask  is the prototype used to create instances of web application

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    ip = TextField('IP:', validators=[validators.required()])
    user = TextField('USER:', validators=[validators.required()])
    password = TextField('PASSWORD:', validators=[validators.required()])

class ReusableForm1(Form):
    vm_name = TextField('VM_NAME:', validators=[validators.required()])
    vm_ram = TextField('VM_RAM:', validators=[validators.required()])
    vm_coresxcpu = TextField('VM_CORESXCPU:', validators=[validators.required()])

class ReusableForm2(Form):
    vm_name = TextField('VM_NAME:', validators=[validators.required()])
    vm_ram = TextField('VM_RAM:', validators=[validators.required()])
    vm_coresxcpu = TextField('VM_CORESXCPU:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)

#Ask for the parameters in the home page
    print form.errors
    if request.method == 'POST':
        ip=request.form['ip']
        user=request.form['user']
        password=request.form['password']

        if form.validate():
            #If user entered the requested values, executes the functions
            getvm(user,password)


        else:
            flash('Please enter valid data ')


  # for vm in vms:
    #    print "%s: " % vm.name + "".join([str(x) for x in vm.get_ips()])
    return render_template('home.html', form=form)

@app.route('/cluster/')
def cluster():
    vms = VM.get_vms()
    storagecont= StorageContainer.get_storage_containers()
    return render_template('cluster.html',vms=vms,storagecont=storagecont)

@app.route('/task/')
def task():
    tasks = Tasks.get_tasks()
    return render_template('task.html', tasks=tasks)

@app.route('/health/')
def health():
    healths = HealthChecks.get_health_checks()
    return render_template('health.html', healths=healths)

@app.route('/network/')
def network():
    vlan_name=request.form['vlan_name']
    vlan_id=request.form['vlan_id']
#    networks = Network.create_network(vlan_name,vlan_id)
    return render_template('network.html', form=form)

@app.route('/createvm/')
def createvm():
    form = ReusableForm(request.form)
#Ask for the parameters in the createvm page
    print form.errors
    if request.method == 'POST':
        vm_name=request.form['vm_name']
        vm_ram=request.form['vm_ram']
        vm_coresxcpu=request.form['vm_coresxcpu']
        user="admin"
        password="nutanix/4u"

    #create1vm(user,password)

        if form.validate():
            #If user entered the requested values, executes the functions
            #getvm(user,password)
            flash('Datos Validos')
            #create1vm(user,password)
            #getuuid(user,password)
            #poweronvm(user,password)

        else:
           flash('Please enter valid data ')

    return render_template('createvm.html',form=form)

@app.route('/letscreatevm/', methods=['POST'])
def letscreatevm():
    vm_name=request.form['vm_name']
    vm_ram=request.form['vm_ram']
    vm_coresxcpu=request.form['vm_coresxcpu']
    user="admin"
    password="nutanix/4u"
    payloadCreateVM = '{\n\t\"description\": \"Tech Summit 2017\",\n\t\"guest_os\": \"Windows TCS\",\n\t\"memory_mb\": %s,\n\t\"name\": \"%s",\n\t\"num_cores_per_vcpu\": %s,\n\t\"num_vcpus\": 1,\n\t\"vm_disks\": [\n{\n\t\t\"disk_address\": {\n\t\t\t\"device_bus\": \"ide\",\n\t\t\t\"device_index\": 0\n\t\t},\n\t\t\"is_cdrom\": true,\n\t\t\"is_empty\": false,\n\t\t\"vm_disk_clone\": {\n\t\t\t\"disk_address\": {\n\t\t\t\t\"vmdisk_uuid\": \"54d1c16b-4341-44e7-aa17-cd8a7972626b\"\n\t\t\t}\n\t\t}\n\t}, \n{\n\t\t\"disk_address\": {\n\t\t\t\"device_bus\": \"scsi\",\n\t\t\t\"device_index\": 0\n\t\t},\n\t\t\"vm_disk_create\": {\n\t\t\t\"storage_container_uuid\": \"cbad2d71-ff2a-4707-8f88-c98ecd70c237\",\n\t\t\t\"size\": 10737418240\n\t\t}\n\t}, \n{\n\t\t\"disk_address\": {\n\t\t\t\"device_bus\": \"ide\",\n\t\t\t\"device_index\": 1\n\t\t},\n\t\t\"is_cdrom\": true,\n\t\t\"is_empty\": false,\n\t\t\"vm_disk_clone\": {\n\t\t\t\"disk_address\": {\n\t\t\t\t\"vmdisk_uuid\": \"03c47aa6-0acd-4c7e-baf5-2867e9984b2a\"\n\t\t\t}\n\t\t}\n\t}],\n\t\"hypervisor_type\": \"ACROPOLIS\",\n\t\"affinity\": null\n}' % (vm_ram, vm_name, vm_coresxcpu)
    response = requests.post(service_url+vms_url,data=payloadCreateVM, auth=(user, password),verify= False)
    return render_template('/createvm.html', response=response)


@app.route('/createapp/')
def createapp():

    return render_template('createapp.html')

@app.route('/appdeploy/', methods=['POST'])
def appdeploy():
    blueprint_name=request.form['blueprint_name']
    team_name=request.form['team_name']
    application_name=request.form['application_name']
    response = Blueprint.run_blueprint(blueprint_name, team_name, application_name)
    return render_template('/createapp.html', response=response)

@app.route('/dbdeploy/', methods=['POST'])
def dbdeploy():
    blueprint_name=request.form['blueprint_name']
    team_name=request.form['team_name']
    application_name=request.form['application_name']
    response = Blueprint.run_blueprint(blueprint_name, team_name, application_name)
    return render_template('/createapp.html', response=response)

@app.route('/scaledeploy/', methods=['POST'])
def deploy():
    blueprint_name=request.form['blueprint_name']
    team_name=request.form['team_name']
    application_name=request.form['application_name']
    response = Blueprint.run_blueprint(blueprint_name, team_name, application_name)
    return render_template('/createapp.html', response=response)

@app.route('/secpatch/', methods=['POST'])
def secpatch():
    blueprint_name=request.form['blueprint_name']
    team_name=request.form['team_name']
    application_name=request.form['application_name']
    response = Blueprint.run_blueprint(blueprint_name, team_name, application_name)
    return render_template('/createapp.html', response=response)

if __name__ == "__main__":
    app.run()

##
