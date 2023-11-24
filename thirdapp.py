from flask import Flask, request
from flask import render_template
from devicelist import DeviceList
from OpModes import OpModes 
from matterbulbop import MatterBulbOp
import os
import subprocess
import json
import paho.mqtt.client as mqtt

devicelist1 = None
reqipaddr = None
DeviceDataBase= None
OperationModesDb = None
demolist=None
pahoclient=None
app = Flask(__name__)

def getip():
    global reqipaddr
    ifacename=os.environ.get('NWIFACE')
    print(ifacename)
    ipstring = "ip addr show " + ifacename + "| grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"      
    s = subprocess.check_output([ipstring], stdin=None, stderr=None, shell=True, universal_newlines=True)
    if len(s) != 0:
        reqipaddr = s[0:len(s)-1]
    

def QueueTheOperations(listops):
    cmdstr=""
    for i in listops:
        cmdstr+=i + '; echo \"\\n\\n\\n\"; '
    return cmdstr
@app.route('/Performdevops', methods=['GET'])
def PerformDeviceOps():
    global devicelist1
    global OperationModesDb
    global pahoclient
    CHIPCmdList=""
    snapvar = os.environ.get('SNAP')
    pathvar=snapvar + "/extra-bin/chip-tool "
    
    try:
        reqargs=request.args.to_dict()
        demoname=reqargs.get("demoname")
        pahoclient.publish("Bulb Op", demoname);
        deviceops=OpModes.Getdevops(OperationModesDb["operationmodes"], demoname)
        print(deviceops)
        Res= {"PerformdevOpsRes": "Failure"}
        for idx in deviceops:
            nodeid = DeviceList.GetDeviceNodeID(devicelist1, idx["devicename"])
            if nodeid == '0':
                nodeid=DeviceList.GetBridgeDeviceNodeID(DeviceDataBase, idx["devicename"])
            if nodeid != '0':    
                devicetype = DeviceList.GetDeviceType(devicelist1, idx["devicename"])
                print(devicetype)
                if devicetype in ["bridge","light", "plug", "light switch", "musicplayer"]:
                    listops=MatterBulbOp.PerformBulbOp(idx, nodeid, pathvar)
                    CHIPCmdList+=QueueTheOperations(listops)
                    Res["PerformdevOpsRes"] = "Success"
        print(CHIPCmdList)
        #pahoclient.publish("Bulb Op", "Turn On");
        #sep38TODO subprocess.call([CHIPCmdList], stdin=None, stderr=None, shell=True, universal_newlines=True)
        return Res            
    except:
        print("some failure")

def on_connect(client, userdata, flags, rc):
    print("connected paho client with rescode " + str(rc))
    #client.subscribe([("bulb on", 0), ("bulb off", 2)])
    
    
def on_message(client, userdata, message):
    print("received an message " + message.topic + " " + str(message.payload))
        
def Spawn_Paho():
    
    global reqipaddr
    global pahoclient
    if pahoclient is not None:
        print("Already Paho client created:")
        return pahoclient
        
    pahoclient = mqtt.Client()
    pahoclient.on_connect = on_connect
    pahoclient.on_message = on_message
    pahoclient.connect(reqipaddr, 1883, 60)
    pahoclient.loop_start()


@app.route('/')
def hello_world():
    global devicelist1
    global DeviceDataBase
    global reqipaddr
    global demolist
    global OperationModesDb
    if OperationModesDb is None:
        OperationModesDb={}
    if demolist is None:
        demolist = []
    if devicelist1 is None:
        devicelist1 = []
    if reqipaddr is None:
        reqipaddr = "127.0.0.1"
    if DeviceDataBase is None:
        DeviceDataBase = {}
    getip()
    Spawn_Paho()
    pathname = os.environ.get('TMPDIR')
    forwardedip=os.environ.get('FORWARDEDIP')
    fname=pathname + "/devicelist.json"
    print(pathname, fname)
    DeviceDataBase=DeviceList.getdata(fname)
    devicelist1=DeviceList.GetDeviceList(DeviceDataBase["devices"])
    opmodefile=pathname + '/opmodes.json'
    OperationModesDb=OpModes.GetData(opmodefile)
    demolist = OpModes.GetDemoList(OperationModesDb["operationmodes"])
    print(demolist)
    return render_template('/devicedemo.html', ipaddr=forwardedip, devicedemolist=demolist)

if __name__ == '__main__':
   
    reqipaddr=None
    ifacename=os.environ.get('NWIFACE')
    print(ifacename)
    ipstring = "ip addr show " + ifacename + "| grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"      
    s = subprocess.check_output([ipstring], stdin=None, stderr=None, shell=True, universal_newlines=True)
    if len(s) != 0:
        reqipaddr = s[0:len(s)-1]
    
    if reqipaddr is not None:
        app.run(host=reqipaddr, debug=True, port=5002)
    else:    
        app.run(host='0.0.0.0', debug=True, port=5002)


