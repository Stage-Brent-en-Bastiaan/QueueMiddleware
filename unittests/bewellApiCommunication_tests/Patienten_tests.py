import unittest
from unittest.mock import patch, Mock
from BewellApiCommunication.Patienten import Patienten, TooManyResultsDBException
from BewellApiCommunication.Models2 import *

class Patienten_tests(unittest.TestCase):
    def setUp(self):
        self.patienten = Patienten()

    @patch('requests.get')
    def test_get_patient_hospital_id_success(self, mock_get):
        # Mock the response data
        mock_response_data = [
            {"id": 1, "name": "Patient 1"},
            {"id": 2, "name": "Patient 2"}
        ]
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=mock_response_data))

        patient = self.patienten.getPatientHospitalId(101)

        self.assertIsInstance(patient, PatientGet)
        self.assertEqual(patient.id, 1)  # Adjust according to your PatientGet structure
        mock_get.assert_called_once_with("?hospital_id=101")

    @patch('requests.get')
    def test_get_patient_hospital_id_too_many_results(self, mock_get):
        # Mock the response data with multiple results
        mock_response_data = [
            {"id": 1, "name": "Patient 1"},
            {"id": 2, "name": "Patient 2"}
        ]
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=mock_response_data))

        with self.assertRaises(TooManyResultsDBException):
            self.patienten.getPatientHospitalId(101)

    @patch('requests.get')
    def test_get_patient_hospital_id_no_results(self, mock_get):
        # Mock the response data with no results
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=[]))

        patient = self.patienten.getPatientHospitalId(101)

        self.assertIsNone(patient)
        mock_get.assert_called_once_with("?hospital_id=101")

    @patch('requests.get')
    def test_get_patient_success(self, mock_get):
        # Mock the response data for a specific patient
        mock_response_data = {"id": 1, "name": "Patient 1"}
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=mock_response_data))

        patient = self.patienten.getPatient(1)

        self.assertIsInstance(patient, PatientGet)
        self.assertEqual(patient.id, 1)  # Adjust according to your PatientGet structure
        mock_get.assert_called_once_with("patients/1")

    @patch('requests.get')
    def test_get_patient_not_found(self, mock_get):
        # Mock a 404 response for a patient
        mock_get.return_value = Mock(status_code=404)

        with self.assertRaises(Exception):
            self.patienten.getPatient(999)  # Assuming you handle this case somewhere

    @patch('requests.get')
    def test_get_patienten_success(self, mock_get):
        # Mock the response data for multiple patients
        mock_response_data = [
            {"id": 1, "name": "Patient 1"},
            {"id": 2, "name": "Patient 2"}
        ]
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=mock_response_data))

        patients = self.patienten.getPatienten("?hospital_id=101")

        self.assertEqual(len(patients), 2)
        self.assertIsInstance(patients[0], PatientGet)
        self.assertEqual(patients[0].id, 1)  # Adjust according to your PatientGet structure

    @patch('requests.get')
    def test_get_patienten_failure(self, mock_get):
        # Mock a failure response
        mock_get.return_value = Mock(status_code=500)

        patients = self.patienten.getPatienten("?hospital_id=101")

        self.assertEqual(patients, [])
        mock_get.assert_called_once_with("patients?hospital_id=101")

if __name__ == '__main__':
    unittest.main()
