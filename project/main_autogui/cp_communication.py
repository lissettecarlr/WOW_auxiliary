import requests

def vx_post(serverkey,vxtitle,vxtext):
    print(serverkey+"|"+vxtitle+"|"+vxtext)
    data = {
    "text":vxtitle,
    "desp":vxtext
    }
    r = requests.post(serverkey, data)


# vx_post(api,"fff","3ffff21")

