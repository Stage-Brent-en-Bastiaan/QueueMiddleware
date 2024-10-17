import requests
import configparser
from .Models2 import PatientGet, apiurl
import json
from requests.auth import HTTPBasicAuth
from pprint import pprint
from functools import lru_cache

class Patienten:

    def __init__(self):
        # de basis url voor alle calls die met patienten te maken hebben
        self.apiurl = apiurl + "patients"
        #cache voor caching, wordt opgeruimd als de klasse wordt opgeruimd
        self.cache={}
    #geef een specifieke patient op basis van zijn id in de bewell api
    def getPatient(self,id):
        if id in self.cache:
            return self.cache[id]
        else:
            parameters=f"/{id}"
            returnType = PatientGet
            config = configparser.ConfigParser()
            config.read(".ini")
            user = config["api"]["username"]
            psswd = config["api"]["password"]
            url = f"{self.apiurl}{parameters}"
            print("-requesting: ", url)
            headers = {"Accept": "application/json"}

            response = requests.get(
                url, auth=HTTPBasicAuth(user, psswd), headers=headers, verify=False
            )
            patient=PatientGet.from_dict(response.json())
            self.cache[id]=patient
            return patient
    #geef een lijst van patienten op basis van een antal parameters, zie bewell documentatie. geef een lege string voor alle patienten
    @lru_cache(maxsize=20)
    def getPatienten(self,parameters):
        returnType = PatientGet
        config = configparser.ConfigParser()
        config.read(".ini")
        user = config["api"]["username"]
        psswd = config["api"]["password"]
        url = f"{self.apiurl}{parameters}"
        print("-requesting: ", url)
        headers = {"Accept": "application/json"}

        response = requests.get(
            url, auth=HTTPBasicAuth(user, psswd), headers=headers, verify=False
        )
        print("-responseStatus: ", response.status_code)
        if response.status_code == 200:
            responseDict = response.json()
            patients = []
            for patient in responseDict:
                patients.append(returnType.from_dict(patient))
            return patients
        else:
            raise ConnectionError(
                f"could not get patienten from request:{url} {response.reason}"
            )
            return []


# patients=apiCall("first_name=Aycan",Patient)
# teller=0
# for patient in patients:
#      print(f"-Patient {teller}:")
#      pprint(vars(patient))
#      teller=teller+1
