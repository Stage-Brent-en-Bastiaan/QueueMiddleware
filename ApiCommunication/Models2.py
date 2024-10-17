from typing import Any
from dataclasses import dataclass
import json
from typing import List
from dataclasses import dataclass
import json
from typing import Optional
from datetime import datetime
# print("Loading Patient module...")

# Example Usage
# jsonstring = json.loads(myjsonstring)
# patient = Patient.from_dict(jsonstring)
"""
hier komen alle globale variabelen voor deze laag
"""
apiurl = "https://mijntest.azstlucas.be/api/v2/"

"""
hier komen alle klassen die gebruikt worden voor communicatie met de bewell api
"""


@dataclass
class PatientGet:
    id: int
    box_code: str
    first_name: str
    last_name: str
    phone_contact: str
    phone_auth: str
    gov_id: str
    hospital_id: str
    date_of_birth: str
    gender: str
    address: str
    nationality: str
    locale: str

    def full_name(self):
        return self.first_name+ " " + self.last_name

    @staticmethod
    def from_dict(obj: Any) -> "Root":
        ##print("from_dict called")
        _id = int(obj.get("id")) if obj.get("id") is not None else None
        _box_code = str(obj.get("box_code"))
        _first_name = str(obj.get("first_name"))
        _last_name = str(obj.get("last_name"))
        _phone_contact = str(obj.get("phone_contact"))
        _phone_auth = str(obj.get("phone_auth"))
        _gov_id = str(obj.get("gov_id"))
        _hospital_id = str(obj.get("hospital_id"))
        _date_of_birth = str(obj.get("date_of_birth"))
        _gender = str(obj.get("gender"))
        _address = str(obj.get("address"))
        _nationality = str(obj.get("nationality"))
        _locale = str(obj.get("locale"))
        return PatientGet(
            _id,
            _box_code,
            _first_name,
            _last_name,
            _phone_contact,
            _phone_auth,
            _gov_id,
            _hospital_id,
            _date_of_birth,
            _gender,
            _address,
            _nationality,
            _locale,
        )


@dataclass
class Content:
    text: str
    type: Optional[str] = "message"
    title: Optional[str] = "test message"


@dataclass
class MessagePost:
    recipient_id: int
    content: Content
    author_id: Optional[int] = 1
    # expiry_timestamp: Optional[int]=None
    silent: Optional[int] = 0

    @staticmethod
    def getSampleMessage():
        message = MessagePost(
            recipient_id=31969,
            content=Content(
                text="Hello! This is a test message.", type="text", title="Test Message"
            ),
            # author_id = 0,
            # expiry_timestamp = 1699999999,
            silent=1,
        )
        return message


# @dataclass
# class Answer:
#     values: List[str]
#     timestamp: int
#     id: int
#     submit_timestamp: int
#     created_timestamp: int
#     updated_timestamp: int

#     @staticmethod
#     def from_dict(obj: Any) -> 'Answer':
#         _values = [str(y) for y in obj.get("values")]
#         _timestamp = int(obj.get("timestamp"))
#         _id = int(obj.get("id"))
#         _submit_timestamp = int(obj.get("submit_timestamp"))
#         _created_timestamp = int(obj.get("created_timestamp"))
#         _updated_timestamp = int(obj.get("updated_timestamp"))
#         return Answer(_values, _timestamp, _id, _submit_timestamp, _created_timestamp, _updated_timestamp)

# @dataclass
# class Option:
#     label: str
#     value: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Option':
#         _label = str(obj.get("label"))
#         _value = str(obj.get("value"))
#         return Option(_label, _value)


@dataclass
class MessageGet:
    text: str
    type: str
    title: str
    # options: List[Option]
    id: int
    author_id: int
    recipient_id: int
    # answer: Answer
    # signature_required: bool
    # signature_timestamp: int
    # signature_datetime: int
    created_timestamp: datetime
    # updated_timestamp: int

    @staticmethod
    def from_dict(obj: Any) -> "MessageGet":
        _text = str(obj.get("text"))
        _type = str(obj.get("type"))
        _title = str(obj.get("title"))
        # _options = [Option.from_dict(y) for y in obj.get("options")]
        _id = int(obj.get("id"))
        _author_id = int(obj.get("author_id"))
        _recipient_id = int(obj.get("recipient_id"))
        # _answer = Answer.from_dict(obj.get("answer"))
        # _signature_required = False
        # _signature_timestamp = int(obj.get("signature_timestamp"))
        # _signature_datetime = int(obj.get("signature_datetime"))
        _created_timestamp = datetime.fromtimestamp(obj.get("created_timestamp"))
        # _updated_timestamp = int(obj.get("updated_timestamp"))
        return MessageGet(
            _text, _type, _title, _id, _author_id, _recipient_id, _created_timestamp
        )
