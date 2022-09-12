from fastapi import FastAPI
import os
import subprocess
import asyncio
from typing import Optional
import json

# Author: Jubaer

app = FastAPI()

os.environ["GOPATH"] = str(os.getcwd())+"/go/bin/tools"
os.environ["GOBIN"] = str(os.getcwd())+"/go/bin"
subprocess.run(["chmod -R +x "+str(os.getcwd())+"/go/bin/go"], shell=True)

## Only uncomment for render.com
subprocess.run([str(os.getcwd())+"/go/bin/go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"], shell=True)
subprocess.run([str(os.getcwd())+"/go/bin/go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"], shell=True)

## Only uncomment for local environment
# subprocess.run(["go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"], shell=True)
# subprocess.run(["go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"], shell=True)


@app.get("/api/scanner1/{domain}")
async def subdomain(domain:str):
    special_characters = """"!@# $%^&*'()}{[]|\`+?_=,<>/"""
    if 'http' in domain:
        return "Error Input"
    elif len(domain) < 1:
        return "Error Input"
    elif '.' not in domain:
        return "Error Input"
    elif 'www.' in domain:
        return "Error Input! Please remove WWW"
    elif any(c in special_characters for c in domain):
        return "Error Input"

    out = await asyncio.create_subprocess_shell(str(os.getcwd()) + "/go/bin/subfinder -d " + str(domain),
                                                stdout=subprocess.PIPE)
    data = []
    output = await out.communicate()

    for subs in output[0].decode().split('\n'):
        if len(subs) != 0:
            data.append(subs)
    return {'result':data}


@app.get("/api/scanner2/nuclei")
async def nuclei_scanner(target_name: str, autoscan: bool, tags: Optional[str] = None):
    try:

        if autoscan == True:
            out = subprocess.Popen(str(os.getcwd()) + "/go/bin/nuclei -u " + str(target_name) + " -as -json", shell=True,
                                   stdout=subprocess.PIPE)
        else:
            out = subprocess.Popen(str(os.getcwd()) + "/go/bin/nuclei -u " + str(target_name) + " -json -tags " + str(tags),
                                   shell=True, stdout=subprocess.PIPE)

        output = out.communicate()

        data = []
        for result in output[0].decode().split('\n'):
            if len(result) != 0:
                output_json = json.loads(result)
                data.append(output_json)
        return data

    except Exception as e:
        return {'message': "Error, Please try again!"}







