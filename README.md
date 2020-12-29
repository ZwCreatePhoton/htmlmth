**Install Dependencies**


`sudo apt install libtidy-dev`

`python -m pip install --ignore-installed -r requirements.txt`



**Output cases to disk and print case descriptions**

`rm -r out ; mkdir out ; ./htmlmth/htmlmth/output_cases.py -sesp 5000 -sesh 127.0.0.1 -sesp 5000 -o out -b htmlmth/baselines/example3.yaml -c htmlmth/cases/example.py -bch abc.com -ld`


**Host evasion server**

`python htmlmth/EvasionHTTPServer.py -i 0.0.0.0 -p 8000 -ipv 4 -sesh 127.0.0.1 -sesp 5000 -b baselines/example.html -c cases/example.py -tc example-middle-011`

visit http://SERVERIP:8000/

`python htmlmth/EvasionHTTPServer.py -i 0.0.0.0 -p 8000 -ipv 4 -sesh 127.0.0.1 -sesp 5000 -b baselines/example3.yaml -c cases/example.py -tc cases/example3.yaml`

visit http://SERVERIP:8000/example.html
