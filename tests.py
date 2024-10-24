# from django.test import TestCase

from ApiCommunication.Patienten import Patienten
from QueueManagerHelpers.RetryLogic import RetryLogic

# Create your tests here.
retrylogicFactory=RetryLogic(2)
for x in range(10):
    print(retrylogicFactory.exponential_backoff(x))
