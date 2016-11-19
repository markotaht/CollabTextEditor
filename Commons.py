MSG_SEP = ";"

INTRODUCTION = "I"
RSP_INTRODUCTION_OK = "I+"
RSP_INTRODUCTION_NOTOK = "I-"

REQ_SEND_LETTER = "A"
RSP_SEND_LETTER_OK = "A+"
RSP_SEND_LETTER_NOTOK = "A-"

REQ_REMOVE_LETTER = "R"
RSP_REMOVE_LETTER_OK = "R+"
RSP_REMOVE_LETTER_NOTOK = "R-"

REQ_MODIFICATION = "M"
RSP_MODIFICATION_OK = "M+"

REQ_SYNCHRONIZE = "S"
RSP_SYNCHRONIZE_OK = "S+"

MSG_FIELD_SEP = ":"

DEFAULT_PORT = 7777;

DEFAULT_RCV_BUFSIZE = 1024

from base64 import decodestring, encodestring
def serialize(msg):
    return encodestring(msg)

def deserialize(msg):
    return decodestring(msg)