# imports
import requests
import configparser
from .Models2 import MessageGet, apiurl, basicauth, MessagePost
from requests.auth import HTTPBasicAuth
from pprint import pprint
from datetime import timedelta, datetime
import json
from dataclasses import asdict
from functools import reduce, lru_cache


class Messages:
    def __init__(self):
        # de basis url voor alle calls die met messages te maken hebben
        self.apiurl = apiurl + "messages?"
        self.basicauth = basicauth

    # geeft het meest recent aangemaakte bericht
    def getMostRecentMessage(self) -> MessageGet:
        returnType = MessageGet
        today = datetime.today() - timedelta(days=1)
        url = f"{self.apiurl}created_from={datetime.timestamp(today)}"
        print("-requesting: ", url)
        headers = {"Accept": "application/json"}
        response = requests.get(url, auth=self.basicauth, headers=headers, verify=False)
        print("responseStatus:", response.status_code)
        if response.status_code == 200:
            responseList = response.json()
            print(
                "lf test message: ",
                list(
                    filter(
                        lambda message: message.get("title") == "test message",
                        responseList,
                    )
                ),
            )
            mostRecentMessage: MessageGet = returnType.from_dict(
                dict(
                    reduce(
                        lambda accum, new: accum
                        if accum.get("created_timestamp") > new.get("created_timestamp")
                        else new,
                        responseList,
                    )
                )
            )
            print("recentste patient", mostRecentMessage)
            return mostRecentMessage
        else:
            # print(response.status_code)
            raise ConnectionError(response.json()["error_message"])
            return None

    # maakt een nieuw bericht in de bewell api op basis van de parameter message:MessagePost
    def PostNewMessage(self, Message:MessagePost)->str:
        url = self.apiurl
        print("-posting: ", url)
        headers = {"Content-Type": "application/json;charset=utf-8"}
        messageJson = json.dumps(asdict(Message))
        print("post payload: ", messageJson)
        response = requests.post(
            url,
            auth=self.basicauth,
            headers=headers,
            verify=False,
            data=messageJson,
        )
        print("responseStatusCode:", response.status_code)
        print("responseStatus:", response.reason)

        if response.ok:
            print("succesvol aangemaakt")
            return response.json().get("message_id")
        else:
            print("responsetext: ", response.text)
            # raise ConnectionError(response.json()["error_message"])
            return response.json().get("message_id")


# mostRecentMessage=getMostRecentMessage()
# print(mostRecentMessage)
