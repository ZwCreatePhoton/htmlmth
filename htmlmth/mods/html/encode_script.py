import re

from . import Mod
import scripting_encoder_client


#https://gallery.technet.microsoft.com/scriptcenter/16439c02-3296-4ec8-9134-6eb6fb599880
# does not change vbscript -> vbscript.encode declaration
def encode_vbscript(server, port, output):
    p = re.compile(r"(?i)(<\s*script.*\s+(?:language|type)\s*=\s*[\"'].*vb.*[\"'].*>)((?:(?!<script)[\w\W])*)(<\s*\/\s*script\s*>)")

    def encode(m):
        script = m.group(2)
        encoded_script = scripting_encoder_client.encode(script, server, port)
        return m.group(1) + encoded_script + m.group(3)
    output = p.sub(encode, output)

    return output

mod_encode_vbscript = Mod(encode_vbscript)

# does not change javascript -> javascript.encode declaration
def encode_javascript(server, port, output):
    p = re.compile(r"(?i)(<\s*script.*\s+(?:language|type)\s*=\s*[\"'].*j.*[\"'].*>)((?:(?!<script)[\w\W])*)(<\s*\/\s*script\s*>)")

    def encode(m):
        script = m.group(2)
        encoded_script = scripting_encoder_client.encode(script, server, port)
        return m.group(1) + encoded_script + m.group(3)
    output = p.sub(encode, output)

    return output

mod_encode_javascript = Mod(encode_javascript)
