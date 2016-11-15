MSG_SEP = ";"
REQ_SEND_LETTER = "l"
RSP_SEND_LETTER_OK = "1"

REQ_ADD_NEW_LINE = "z"
RSP_ADD_NEW_LINE_OK = "2"

REQ_REMOVE_LINE = "e"
RSP_REMOVE_LINE_OK = "3"

REQ_REMOVE_LETTER = "c"
RSP_REMOVE_LETTER_OK = "4"

REQ_MODIFICATION = "b"
RSP_MODIFICATION_OK = "5"

REQ_SYNCHRONIZE = "s"
RSP_SYNCHRONIZE_OK = "6"

MSG_FIELD_SEP = ":"

DEFAULT_RCV_BUFSIZE = 1024

from base64 import decodestring, encodestring
def serialize(msg):
    return encodestring(msg)

def deserialize(msg):
    return decodestring(msg)