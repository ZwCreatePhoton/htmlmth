import os
import tempfile
import shlex
from subprocess import Popen, PIPE

from flask import Flask, request

app = Flask(__name__)

# python.exe -m pip install flask
# set FLASK_APP=scripting_encoder_server.py
# python.exe -m flask run --host=0.0.0.0

encoder_content = r"""
Option Explicit 
 
dim oEncoder, oFilesToEncode, file, sDest 
dim sFileOut, oFile, oEncFile, oFSO, i 
dim oStream, sSourceFile 
 
set oFilesToEncode = WScript.Arguments 
set oEncoder = CreateObject("Scripting.Encoder") 
For i = 0 to oFilesToEncode.Count - 1 
    set oFSO = CreateObject("Scripting.FileSystemObject") 
    file = oFilesToEncode(i) 
    set oFile = oFSO.GetFile(file) 
    Set oStream = oFile.OpenAsTextStream(1) 
    sSourceFile=oStream.ReadAll 
    oStream.Close 
    sDest = oEncoder.EncodeScriptFile(".vbs",sSourceFile,0,"") 
    sFileOut = file & ".vbe" 
    Set oEncFile = oFSO.CreateTextFile(sFileOut) 
    oEncFile.Write sDest 
    oEncFile.Close 
Next 
"""
encoder_path = "encoder.vbs"
with open(encoder_path, "w") as f:
    f.write(encoder_content)

@app.route('/encode', methods=['POST'])
def encode():
    script = request.form['script']
    encoded_script = ""
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as fp:
        pass
    os.unlink(path)
    path += ".vbs"
    encoded_path = path + ".vbe"
    try:
        with open(path, 'w') as tmp:
            tmp.write(script)
        encode_command = 'wscript {0} "{1}"'.format(encoder_path, path)
        print(encode_command)
        process = Popen(shlex.split(encode_command), stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        with open(encoded_path, "r") as g:
	        encoded_script = g.read()
    finally:
        try:
            os.remove(path)
            os.remove(encoded_path)
        except:
            pass
    return encoded_script
