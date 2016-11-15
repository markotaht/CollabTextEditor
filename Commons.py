MSG_SEP = ";"
REQ_SEND_LETTER = "l"
RSP_SEND_LETTER_OK = "1"

REQ_REMOVE_LETTER = "c"
RSP_REMOVE_LETTER_OK = "2"

REQ_MODIFICATION = "b"
RSP_MODIFICATION_OK = "3"

REQ_SYNCHRONIZE = "s"
RSP_SYNCHRONIZE_OK = "4"

MSG_FIELD_SEP = ":"

DEFAULT_RCV_BUFSIZE = 1024

from base64 import decodestring, encodestring
def serialize(msg):
    return encodestring(msg)

def deserialize(msg):
    return decodestring(msg)