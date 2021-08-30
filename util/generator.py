import random
import base64
        
def base64_convert(s):
    converted = base64.b64encode(s.encode(encoding="utf-8"))
    return converted.decode(encoding="utf-8")