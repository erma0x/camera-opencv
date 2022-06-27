import depthai

"""
script che mostra le videocamere connesse della marca OAK, ovvero le videocamere che supportano la libreria depthai. 
"""

for device in depthai.Device.getAllAvailableDevices():
    print(f"\n ID VIDEOCAMERA \t\t[ {device.getMxId()} ]\n NOME VIDEOCAMERA \t[ {device.state} ] \n")
