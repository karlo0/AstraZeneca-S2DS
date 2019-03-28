from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import time
import os

# [trigger:tmChem|DNorm|tmVar|GNormPlus]
trigger = 'DNorm'

input_query = 'breast cancer and cancer'

input_str='00000000|t|'+input_query+'\n00000000|a|'+input_query


url_Submit = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + trigger + "/Submit/"


urllib_submit = urlopen(url_Submit, input_str.encode())
urllib_result = urlopen(url_Submit, input_str.encode())
SessionNumber = urllib_submit.read()


url_Receive = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + SessionNumber.decode('utf-8') + "/Receive/"

code=404
while(code == 404 or code == 501):
    try:
        urllib_result = urlopen(url_Receive)
    except HTTPError as e:
        code = e.code
        print("HTTPError: "+str(code))
        time.sleep(1)
    except URLError as e:
        code = e.code
        print("URLError: "+str(code))
        time.sleep(1)
    else:
        code = urllib_result.getcode()

outread = urllib_result.read().decode('utf-8')
print(outread)
