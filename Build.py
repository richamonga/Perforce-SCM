import configparser
import time
import subprocess
import smtplib
from P4 import P4, P4Exception



'''
Function to read Configurations from the config file 
and build a dictionary for all elements read
'''
def ReadConfigs(filename):
    parser = configparser.ConfigParser()
    read_ok = parser.read(filename)
    configs = {}
    
    if(read_ok[0] == filename):
        for section in parser.sections():
            for key, value in parser.items(section):
                configs[key] = value 
    return configs



'''
Funtion to write/update the timestamp of the last run time 
of this script 
'''
def UpdateLastTime(filename):
    parser = configparser.ConfigParser()
    parser.read_file(open(filename))

    if(False == parser.has_section("Timestamp")):
        parser.add_section("Timestamp")
    
    parser.set("Timestamp","LastRunTime", str(int(time.time())))    
    with open('Config.ini', 'r+') as configfile:
        parser.write(configfile)




'''
Function to create SMTP connection and sends
Email to the reciever
'''
def SendEmail(config, errorMsg):
    s = smtplib.SMTP(config['smtp_server'], int(config['smtp_port']))
    s.starttls()
    s.login(config['sender'], config['email_pwd'])
    
    subject = 'P4 build failure notification' 
    message = 'Subject: {}\n\n{}'.format(subject, errorMsg)
    s.sendmail(config['sender'], config['receiver'], message) 
    s.quit()
    print("Email Sent Successfully!!!")
    
    

'''
Funtion to login into P4 , perform SCM
and execute batch file
'''    
def LoginToP4(configs):   
    p4 = P4()
    p4.user = configs['p4_user']
    p4.password = configs['p4_pwd']
    p4.port = configs['p4_port']
    p4.client = configs['p4_client']
    
    try:
        p4.connect()
        
        FileStat = p4.run("fstat", "//depot/try/task.bat")        
        FileAttr = FileStat[0]
        
        headchange = FileAttr.get('headChange')
        ClientBatFile = FileAttr.get('clientFile')
        RevTime = int(FileAttr.get('headTime'))
        CurrRev = int (FileAttr.get('haveRev'))
        MaxRev = int(FileAttr.get('headRev'))
        
        p4.tagged = 0 
        
        MessageStr = ""
        for Num in range(CurrRev, MaxRev+1, 1):
            MessageStr += "\n+++++++++++++++++++++++++++++++ Rev: "+str(Num)+" +++++++++++++++++++++++++++++++\n"
            changeList = p4.run("describe",str(Num))
            MessageStr += " ".join(changeList)
            
        MessageStr += "\n+++++++++++++++++++++++++++++++\ FINISH +++++++++++++++++++++++++++++++\n\n\n\n"    
        
        strArg = "//depot/try/...@" + headchange
        Result = ""
        
        if(RevTime < int(configs['lastruntime'])):
            p4.run_changes(strArg)
            p4.run_sync()
            Result = subprocess.check_output(ClientBatFile)
            
        strRes = Result.decode("utf-8")
        if(strRes.find("Error") >= 0):
            MessageStr += "Build Error: " + strRes 
            SendEmail(configs, MessageStr)
             
    except P4Exception:
        for e in p4.errors:
            print(e)
    finally:
        p4.disconnect()




if __name__ == "__main__":
    file_name = 'Config.ini'
    configs = ReadConfigs(file_name)    
    LoginToP4(configs)
    UpdateLastTime(file_name)
