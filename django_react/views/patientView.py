from rest_framework.decorators import api_view
from rest_framework.response import Response
from ApiCommunication.Patienten import Patienten
import json


@api_view()
def PatientGet(request):
    patientenFactory: Patienten = Patienten()

    patients_data = patientenFactory.getPatienten("")

    patients_json = json.dumps([patient.__dict__ for patient in patients_data])

    return Response(patients_json)
