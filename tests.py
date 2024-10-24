# from django.test import TestCase

from ApiCommunication.Patienten import Patienten

# Create your tests here.
patientenFactory: Patienten = Patienten()
print(patientenFactory.getPatienten("?first_name=Bastiaan"))
print(patientenFactory.getPatienten(""))
