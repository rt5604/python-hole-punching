import subprocess
import sys
import uuid

def is_window():
    if sys.platform == 'win32':
        return True

    return False

def is_raspberrypi():
    try:
        with open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower():
                return True
    except Exception:
        pass

    return False

def getSystemSerial():
    if is_raspberrypi():
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"
        
        return cpuserial

    elif is_window():
        cmd = 'wmic cpu get ProcessorId'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result = proc.stdout.read()
        try:
            result = result.decode('utf-8')
        except Exception as ex:
            result = result.decode('cp949')

        # print('result = {}'.format(result))

        processorIdStr = 'ProcessorId'
        lenProcessorIdStr = len(processorIdStr)
        index = result.find(processorIdStr)
        # print('index = {}'.format(index))

        procIdStr = result[index+lenProcessorIdStr:]
        sProcIdStr = procIdStr.strip()

        # print('ProcessorId = [{}]'.format(sProcIdStr))
        return sProcIdStr

    else:   # Assume that the other system is linux
        uid = uuid.getnode()
        mac = ''.join(("%012X" % uid)[i:i+2] for i in range(0, 12, 2))
        return mac

