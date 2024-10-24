# from django.test import TestCase
import json
from ApiCommunication.Patienten import Patienten

# Create your tests here.
patientFactory=Patienten

response=patientFactory.getPatienten("")
json=map(lambda item: json.dumps(item.__dict__),patientFactory)
print(json)
