import re

from . import Mod
import scripting_encoder_client


#https://gallery.technet.microsoft.com/scriptcenter/16439c02-3296-4ec8-9134-6eb6fb599880
# does not change vbscript -> vbscript.encode declaration
def encode_vbscript(server, port, output):
    REPLACE_ME = "REPLACEME"
    p = re.compile(r"(?i)(<\s*script.*\s+language\s*=\s*[\"'].*vb.*[\"'].*>)([\s\S]*)(<\s*\/\s*script\s*>)")
    script_search = re.search(p, output)
    if script_search:
        script = script_search.group(2)
        encoded_script = scripting_encoder_client.encode(script, server, port)
        sub = r'\1' + REPLACE_ME + r'\3'
        output = re.sub(p, sub, output)
        output = output.replace(REPLACE_ME, encoded_script)
    else:
        pass
    return output

mod_encode_vbscript = Mod(encode_vbscript)