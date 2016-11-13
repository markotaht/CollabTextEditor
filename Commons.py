MSG_SEP = ";"
REQ_SEND_LETTER = "l"
RSP_SEND_LETTER_OK = "1"

REQ_ADD_NEW_LINE = "z"
RSP_ADD_NEW_LINE_OK = "2"

REQ_REMOVE_LINE = "e"
RSP_REMOVE_LINE_OK = "3"

REQ_MOVE_CARET = "a"
RSP_MOVE_CARET_OK = "4"

MSG_FIELD_SEP = ":"

from base64 import decodestring, encodestring
def serialize(msg):
    return encodestring(msg)

def deserialize(msg):
    return decodestring(msg)