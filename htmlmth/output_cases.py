#!/usr/bin/env python2
import argparse
import importlib
import os
import sys

package_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(package_path)
from htmlmth.utils import TransformFunctionArgument, MIME_TYPE_MAP, IsYaml, ParseBaselineYaml, ParseTestcaseYaml


if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-b', '--baseline', required=True, type=str,
                        help='Path to a YAML that describes baseline files OR path to a baseline file to apply evasions to. e.g. {} OR {}.'.format(os.path.join(package_path, "baseline", "example2.yaml"), os.path.join(package_path, "baseline", "example.html")))
    parser.add_argument('-c', '--cases', required=True, type=str,
                        help='Path to python file that implements the cases. e.g. {}'.format(os.path.join(package_path, "cases", "example.py")))
    parser.add_argument('-tc', '--testcase', required=False, default=None, type=str,
                        help='test case name OR path to a YAML that describes which cases to use. If not specified, all cases will output')
    parser.add_argument('-bch', '--bchost', required=False, type=str, default="127.0.0.1",
                        help='host used to select baseline & case.')
    parser.add_argument('-o', '--outdir', required=False, default='out', help='output directory', metavar='DIR')
    parser.add_argument('-sesh', '--scriptencodeserverhost', required=True, type=str,
                        help='ip of server running "scripting_encoder_server.py" # needed for evasions.html.encoded_script ; if that evasion is not used enter anything')
    parser.add_argument('-sesp', '--scriptencodeserverport', required=True, type=int,
                        help='port of server running "scripting_encoder_server.py" # needed for evasions.html.encoded_script ; if that evasion is not used enter anything')
    parser.add_argument('-ld', '--longdescriptions', required=False, default=False, action='store_true', help='Use long case descriptions')
    args = parser.parse_args()

    baseline = args.baseline
    cases_py = args.cases
    test_case = args.testcase
    baseline_case_host = args.bchost
    out_dir = args.outdir
    longdescriptions = args.longdescriptions
    script_encoder_server = args.scriptencodeserverhost # ip of server running "scripting_encoder_server.py" # needed for evasions.html.encoded_vbscript
    script_encoder_port = args.scriptencodeserverport # port of server running "scripting_encoder_server.py" # needed for evasions.html.encoded_vbscript
    import evasions.html
    evasions.html.encoded_script.SCRIPTING_ENCODER_SERVER = script_encoder_server
    evasions.html.encoded_script.SCRIPTING_ENCODER_PORT = script_encoder_port

    # import cases
    cases_module_directory = os.path.dirname(cases_py)
    sys.path.append(os.path.abspath(cases_module_directory))
    cases_module_name = os.path.splitext(os.path.basename(cases_py))[0]
    cases_module = importlib.import_module(cases_module_name)
    cases = cases_module.get_cases(long_descriptions=longdescriptions)

    try:
        os.mkdir(out_dir)
    except:
        pass

    # prep baseline file(s)
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

    testcases = []
    if test_case:
        if IsYaml(test_case):
            testcases.extend(ParseTestcaseYaml(test_case))
        else:
            tc = {
                "host": "",
                "path": "",
                "casename": test_case
            }
            testcases.append(tc)
    

    # apply cases
    for case in cases.values():
        case_args = []
        for bl in baselines:
            if not (not bl["host"] or bl["host"].lower() == baseline_case_host.lower()):
                continue
            if testcases and not any((not tc["host"] or tc["host"].lower() == baseline_case_host.lower()) and (not tc["path"] or tc["path"] == bl["path"]) and tc["casename"] == case.name for tc in testcases):
                continue
            file_ext = os.path.splitext(bl["filepath"])[-1]
            case_arg = TransformFunctionArgument(content=bl["content"], content_type=MIME_TYPE_MAP[file_ext])
            case_arg.metadata.http.host = bl["host"]
            case_arg.metadata.http.path = bl["path"]
            case_arg.metadata.http.server_header = True
            case_arg.metadata.http.server_header_value = "Apache/2.0.33"
            case_arg.metadata.http.content_type_header = True
            case_arg.metadata.http.content_length_header = True
            case_arg.metadata.http.connection_header = True
            case_args.append(case_arg)
        if not case_args:
            continue
        root_dir = os.path.join(out_dir, case.name)
        try:
            os.mkdir(root_dir)
        except:
            pass
        hosted_files = case(case_args)
        for hosted_file in hosted_files:
            hosted_filepath = os.path.join(root_dir, hosted_file.metadata.http.path[1:])
            try:
                os.makedirs(os.path.dirname(hosted_filepath))
            except OSError as e:
                pass
            if hosted_filepath.endswith("/") or hosted_filepath.endswith("\\"):
                hosted_filepath += "index.html"
            with open(hosted_filepath, "wb") as f:
                f.write(hosted_file.metadata.http.payload)
            with open(hosted_filepath + ".headers", "wb") as f:
                f.write(hosted_file.metadata.http.headers)
            with open(hosted_filepath + ".body", "wb") as f:
                f.write(hosted_file.metadata.http.body)

        print(case.name + ":\t" + case.description)
