import tinytuya
import time
import copy
from threading import Lock as Mutex
    #dev_id='d774d88399af8258ddjmjz', address='192.168.1.83', local_key='U/$B2?kq|iO8}l`j'
class TinyTuyaPlugData:
    def __init__(self, devname, devid, devip, devkey):
        self.PlugData= {"devicename":"plug1", "CurCurrent": "0", "CurVoltage": "0", "CurPower": "0", "CurPwrUsage": "0"}
        self.PlugData["devicename"] = devname
        self.ElectricityConsumption=0
        self.datamutex=None; #This is just a overkill here
        self.DEVICEID = devid 
        self.DEVICEIP= devip
        self.DEVICEKEY=devkey
    def Getdata(self):
        data={}
        #global datamutex; 
        #global ElectricityConsumption
        eleccons =0
        if self.datamutex != None and self.datamutex.acquire(True, 2) == True:
            print(self.PlugData)
            data=copy.deepcopy(self.PlugData)
            self.datamutex.release()
        else:
            data["CurCurrent"]="InValid"
            data["CurVoltage"] = "InValid" 
            data["CurPower"] = "InValid"
            data["CurPwrUsage"] = "InValid"
        return self.ElectricityConsumption, data 
    
    def Setdata(self, data):
        #global datamutex; 
        #global ElectricityConsumption
        if self.datamutex.acquire(True, 2) == True:
            self.PlugData["CurCurrent"]=data.get('18', 0)
            voltage = data.get('20')
            if voltage == None:
                voltage = self.PlugData["CurVoltage"] 
            else:    
                voltage=float(voltage/10)
            self.PlugData["CurVoltage"] = str(voltage)
    
            pwr= data.get('19', 0)
            if pwr == None:
                pwr= self.PlugData["CurPower"] 
            else: 
                pwr= float(pwr/10)
            self.PlugData["CurPower"] = str(pwr)
    
            if data != None and data.get('17') != None:
                if data['17'] != self.PlugData['CurPwrUsage']:
                    self.PlugData["CurPwrUsage"] =   data['17']      
                    self.ElectricityConsumption += int(data['17'])
            self.datamutex.release()
    
    def ReceiveDeviceData(self):
        #global datamutex; 
        self.datamutex=Mutex() 
        d = tinytuya.OutletDevice(self.DEVICEID, self.DEVICEIP, self.DEVICEKEY)
        d.set_version(3.3)
        d.set_socketPersistent(True)
        self.datamutex.acquire() 
        print(" > Send Request for Status < ")
        payload = d.generate_payload(tinytuya.DP_QUERY)
        d.send(payload)
        count = 0
        
        print(" > Begin Monitor Loop <")
        self.datamutex.release()
        while(True):
            # See if any data is available
            data = d.receive()
            #if count%15 + 1 == 1:
            if data != None:
                    print(self.DEVICEIP, 'Received Payload: %r' % data)
                
            if data != None and  data.get('dps')!= None:
                if data['dps'].get('17') != None:
                    print(self.DEVICEIP, ' Received Payload: %r' % data['dps'])
            # Send keyalive heartbeat
            #print(" > Send Heartbeat Ping < ", count)
            if data != None and data.get('dps') != None:
                self.Setdata(data['dps']) 
            payload = d.generate_payload(tinytuya.HEART_BEAT)
            d.send(payload)
        
            # NOTE If you are not seeing updates, you can force them - uncomment:
            # print(" > Send Request for Status < ")
            # payload = d.generate_payload(tinytuya.DP_QUERY)
            # d.send(payload)
            if count % 15 == 0:
                # NOTE Some smart plugs require an UPDATEDPS command to update power data
                print(self.DEVICEIP, " > Send DPS Update Request < ")
                payload = d.generate_payload(tinytuya.DP_QUERY)
                #payload = d.generate_payload(tinytuya.UPDATEDPS)
                d.send(payload)   
                 #data = d.receive()
                 #print('Received Payload: %r' % data)
            count=count+1
    
    if __name__ == '__main__':
        ReceiveDeviceData()
