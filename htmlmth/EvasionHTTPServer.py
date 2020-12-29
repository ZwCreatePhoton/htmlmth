#!/usr/bin/env python2
import socket, sys, os, SocketServer
import importlib
import argparse
from collections import OrderedDict

package_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(package_path)
from htmlmth.utils import TransformFunctionArgument, MIME_TYPE_MAP, IsYaml, ParseBaselineYaml, ParseTestcaseYaml, TransformFunction


class EvasionHTTPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, baseline, cases, address_family=socket.AF_INET, test_case=None):
        # TODO: assume cases is OrderedDict and remove upgrading cases to a OrderedDict in a future revision (a)
        if isinstance(cases, TransformFunction):
            cases = OrderedDict([cases.name, cases])

        baselines = []
        if IsYaml(baseline):
            baselines.extend(ParseBaselineYaml(baseline))
        else:
            bl = {
                "host": "",
                "path": "/",
                "filepath": baseline,
                "content": open(baseline, "r").read()
            }
            baselines.append(bl)

        # TODO: support different cases based on path (before pre-evasion path and post-evasion path). Too difficult to implement right now.
        # so path should be wildcard ("")
        self.testcases = []
        if cases is not None:
            if test_case:
                if IsYaml(test_case):
                    self.testcases.extend(ParseTestcaseYaml(test_case))
                    if len(self.testcases) == 0:
                        tc = {
                            "host": "",
                            "path": "",
                            "casename": ""
                        }
                        self.testcases.append(tc)
                else:
                    tc = {
                        "host": "",
                        "path": "",
                        "casename": test_case
                    }
                    self.testcases.append(tc)
        else:
            tc = {
                "host": "",
                "path": "",
                "casename": ""
            }
            self.testcases.append(tc)

        # should we auto populate missing testcases with entries (will null cases) for HTTP paths in baselines?
        # right now if path: "/a.html" does not have an entry in testcases, then we will return a 404 even if an entry exists for "/a.html" in baselines

        # generate cases. may take some time
        self.hosted_files = [] # list of tuple: (testcase, output)
        for tc in self.testcases:
            case_args = []
            for bl in baselines:
                if not (tc["host"] or bl["host"] or tc["host"].lower() == bl["host"].lower()):
                    continue
                if (tc["path"] and bl["path"]) and (tc["path"] != bl["path"]):
                    continue
                file_ext = os.path.splitext(bl["filepath"])[-1]
                case_arg = TransformFunctionArgument(content=bl["content"], content_type=MIME_TYPE_MAP.get(file_ext, "None/None"))
                case_arg.metadata.http.host = bl["host"]
                case_arg.metadata.http.path = bl["path"]
                case_arg.metadata.http.server_header = True
                case_arg.metadata.http.server_header_value = "Apache/2.0.33"
                case_arg.metadata.http.content_type_header = True
                case_arg.metadata.http.content_length_header = True
                case_arg.metadata.http.connection_header = True
                case_args.append(case_arg)
            if tc["casename"]:
                case = cases[tc["casename"]]
                output = case(case_args)
            else:
                output = case_args
            self.hosted_files.extend([(tc, o) for o in output])

        EvasionHTTPServer.address_family = address_family
        SocketServer.ThreadingTCPServer.__init__(self, server_address, EvasionHTTPRequestHandler)


class EvasionHTTPRequestHandler(SocketServer.BaseRequestHandler):

    RESPONSE_404 = "HTTP/1.1 404 Not Found\r\n" \
                            "\r\n"

    def setup(self):
        self.request.settimeout(2.5)

    def handle(self):
        csock = self.request

        try:
            req = ""
            should_continue = False
            while not req.endswith("\r\n\r\n"):  # '\r\n\r\n' = end of HTTP request header
                try:
                    req += csock.recv(1024)
                except socket.error as e:
                    print(e)
                    if req == "":
                        should_continue = True
                        break  # no data recvieved
                except socket.timeout as e:
                    print "timeout"
                    should_continue = True
                    break  # Ignores the spammy favicon requests &| empty request that IE likes to send
            if should_continue: return
        except Exception as e:
            print("{}".format(e))
            return

        path = req.split()[1].split("?")[0]
        host = req.lower().split("host: ")[1].split("\n")[0].split("\r")[0].split(":")[0] if len(req.lower().split("host: ")) > 1 else None

        # keep searching until an insensitive host match or the last wild card match
        hosted_file = None
        for tc, hf in self.server.hosted_files:
            if tc["host"] and tc["host"].lower() != host.lower():
                continue
            if (hf.metadata.http.path == path) and ((not host) or (not hf.metadata.http.host) or (hf.metadata.http.host.lower() == host.lower())):
                hosted_file = hf
                if host and hf.metadata.http.host:
                    break

        if hosted_file is not None:
            response = hosted_file.metadata.http.headers + hosted_file.metadata.http.body
            csock.sendall(response)
        else:
            csock.sendall(self.__class__.RESPONSE_404)

    def finish(self):
        self.request.shutdown(socket.SHUT_RDWR)
        self.request.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--host', required=True, type=str,
                        help='ip to host the server on')
    parser.add_argument('-p', '--port', required=True, type=int,
                        help='port to host the server on')
    parser.add_argument('-ipv', '--ipversion', required=False, type=int, choices=[4,6], default=4,
                        help='ip version')
    parser.add_argument('-b', '--baseline', required=True, type=str,
                        help='Path to a YAML that describes baseline files OR path to a baseline file to apply evasions to. e.g. {} OR {}.'.format(
                            os.path.join(package_path, "baseline", "example2.yaml"),
                            os.path.join(package_path, "baseline", "example.html")))
    parser.add_argument('-c', '--cases', required=False, type=str, default=None,
                        help='Path to python file that implements the cases. e.g. {}'.format(
                            os.path.join(package_path, "cases", "example.py")))
    parser.add_argument('-tc', '--testcase', required=False, default=None, type=str,
                        help='test case name OR path to a YAML that describes which cases to use.')
    parser.add_argument('-sesh', '--scriptencodeserverhost', required=True, type=str,
                        help='ip of server running "scripting_encoder_server.py" # needed for evasions.html.encoded_script ; if that evasion is not used enter anything')
    parser.add_argument('-sesp', '--scriptencodeserverport', required=True, type=int,
                        help='port of server running "scripting_encoder_server.py" # needed for evasions.html.encoded_script ; if that evasion is not used enter anything')
    args = parser.parse_args()


    host, port = args.host, args.port
    ipver = str(args.ipversion)
    baseline = args.baseline
    cases_py = args.cases
    test_case = args.testcase
    script_encoder_server = args.scriptencodeserverhost # ip of server running "scripting_encoder_server.py" # needed for evasions.html.encoded_vbscript
    script_encoder_port = args.scriptencodeserverport # port of server running "scripting_encoder_server.py" # needed for evasions.html.encoded_vbscript
    import evasions.html
    evasions.html.encoded_script.SCRIPTING_ENCODER_SERVER = script_encoder_server
    evasions.html.encoded_script.SCRIPTING_ENCODER_PORT = script_encoder_port

    # import cases
    if cases_py:
        cases_module_directory = os.path.dirname(cases_py)
        sys.path.append(os.path.abspath(cases_module_directory))
        cases_module_name = os.path.splitext(os.path.basename(cases_py))[0]
        cases_module = importlib.import_module(cases_module_name)
        cases = cases_module.get_cases()
    else:
        cases = None

    af = socket.AF_INET6 if "6" in ipver else socket.AF_INET

    server = EvasionHTTPServer((host, port), baseline, cases, address_family=af, test_case=test_case)

    print("\n\n\t\tHosting...\n\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        print("Exiting...")
