<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** ZwCreatePhoton, htmlmth, @ZwCreatePhoton, email, HTMLMTH, Web server that applies HTML & HTTP evasions dynamically
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!--
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ZwCreatePhoton/htmlmth">
<!--    <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  </a>

  <h3 align="center">HTMLMTH</h3>

  <p align="center">
    Web server that applies HTML & HTTP evasions dynamically
    <br />
<!--    <a href="https://github.com/ZwCreatePhoton/htmlmth"><strong>Explore the docs »</strong></a> -->
    <br />
    <br />
    <!--
    <a href="https://github.com/ZwCreatePhoton/htmlmth">View Demo</a>
    ·
    -->
    <a href="https://github.com/ZwCreatePhoton/htmlmth/issues">Report Bug</a>
    ·
    <a href="https://github.com/ZwCreatePhoton/htmlmth/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->

HTMLMTH is a web server that applies HTML & HTTP evasions dynamically to outgoing traffic.


<!-- 
### Built With

* []()
* []()
* []()

-->



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

```bash
sudo apt update
sudo apt install -y libtidy-dev
sudo apt install -y git
git clone git@github.com:ZwCreatePhoton/htmlmth.git
sudo apt install -y curl
sudo apt install -y python2.7
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py | python2.7
python2.7 -m pip install virtualenv
python2.7 -m virtualenv venv_htmlmth
./venv_htmlmth/bin/python2 -m pip install --ignore-installed -r htmlmth/requirements.txt 
```

<!-- USAGE EXAMPLES -->
## Usage

There are three scripts of interest: [_output_cases.py_](htmlmth/output_cases.py), [_EvasionHTTPServer.py_](htmlmth/EvasionHTTPServer.py), and  [_scripting_encoder_server.py_](htmlmth/scripting_encoder_server.py)


**EvasionHTTPServer.py**

This script implements the HTTP(S) server that applies lists of evasions (AKA "cases") dynamically.

EvasionHTTPServer Usage Example 1

```bash
./venv_htmlmth/bin/python2 htmlmth/htmlmth/EvasionHTTPServer.py -i 0.0.0.0 -p 8000 -ipv 4 -sesh 127.0.0.1 -sesp 5000 -b htmlmth/examples/baselines/example.html -c htmlmth/examples/cases/example.py -tc example-middle-011
```

Host an Evasion HTTP server instance on 0.0.0.0:8000 that hosts the file [_examples/baselines/example3.html_](examples/examples/baselines/example3.html) as the baseline content and uses the case [*example-middle-011* from examples/cases/example.py](https://github.com/ZwCreatePhoton/htmlmth/blob/main/examples/cases/example.py#L15) as the applied evasion.

When http://SERVERIP:8000/ is visited, the returned content should be the baseline with the following modifications (example-middle-011):

1. HTML comments removed AKA the evasion: `htmlmth.evasions.html.remove_html_comments`
2. 414 HTTP status code AKA evasion: `htmlmth.evasions.http.status_code_4xx.parameterize(statuscode=414)`


EvasionHTTPServer Usage Example 2

```bash
./venv_htmlmth/bin/python2 htmlmth/htmlmth/EvasionHTTPServer.py -i 0.0.0.0 -p 8000 -ipv 4 -sesh 127.0.0.1 -sesp 5000 -b htmlmth/examples/baselines/example3.yaml -c htmlmth/examples/cases/example.py -tc htmlmth/examples/cases/example3.yaml
```

Host an Evasion HTTP server instance on 0.0.0.0:8000 that hosts the baseline HTTP resources defined in [_examples/baselines/example3.yaml_](examples/examples/baselines/example3.yam;) as the baseline contents and uses the cases listed in [*examples/cases/example3.yaml*](https://github.com/ZwCreatePhoton/htmlmth/blob/main/examples/cases/example3.yaml) and defined in [*examples/cases/example.py*](https://github.com/ZwCreatePhoton/htmlmth/blob/main/examples/cases/example.py#L14) as the applied evasions.

When http://SERVERIP:8000/example.html is visited, the returned content should be the baseline with the following modifications (example-middle-011):

1. HTML comments removed AKA the evasion: `htmlmth.evasions.html.remove_html_comments`
2. 414 HTTP status code AKA evasion: `htmlmth.evasions.http.status_code_4xx.parameterize(statuscode=414)`

When http://abc.com:8000/ is visited (where abc.com points to SERVERIP), the returned content should be the baseline with the following modifications (example-null-001):
1. No modifications


**output_cases.py**

This script serializes evaded content to disk.

output_cases Usage Example 1

```bash
rm -r out ; mkdir out ; ./venv_htmlmth/bin/python2 htmlmth/htmlmth/output_cases.py -sesp 5000 -sesh 127.0.0.1 -sesp 5000 -o out -b htmlmth/examples/baselines/example3.yaml -c htmlmth/examples/cases/example.py -bch abc.com -ld
```

Serialize the evaded content to the _out_ directory using the baseline HTTP resources defined in [_examples/baselines/example3.yaml_](examples/examples/baselines/example3.yaml) as the baseline contents and all the cases defined in [*examples/cases/example.py*](https://github.com/ZwCreatePhoton/htmlmth/blob/main/examples/cases/example.py#L14) as the applied evasions. Content is served up as if it were accessed using the hostname *abc.com*. Long descriptions will be printed to stdout.


**scripting_encoder_server.py**

Some evasions utilize a closed source vbscript/jscript encoder by Microsoft. This script acts as a server that uses the encoder to return back encoded content. The server is required by some evasions to generate the evaded content. This script must run on a Windows host accessible from the machine running *output_cases.py* or *EvasionHTTPServer.py*.

When using *output_cases.py* or *EvasionHTTPServer.py*, specify the ip (using the **-sesh** parameter) and the port (using the **-sesp** parameter) that the script is listening on. The default port is 5000.  

If an evasion uses scripting_encoder_server.py and it is not accessible, a requests.exceptions.ConnectionError will occur.

```bash
python.exe -m pip install flask
set FLASK_APP=scripting_encoder_server.py
python.exe -m flask run --host=0.0.0.0
```

_To see the available evasions, please refer to the [evasions](htmlmth/evasions) directory._

_To see practical examples of cases, please refer to the [HtmlmthCases](https://github.com/ZwCreatePhoton/htmlmthcases) repo._



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

ZwCreatePhoton - [@ZwCreatePhoton](https://twitter.com/ZwCreatePhoton)

Project Link: [https://github.com/ZwCreatePhoton/htmlmth](https://github.com/ZwCreatePhoton/htmlmth)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ZwCreatePhoton/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/ZwCreatePhoton/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ZwCreatePhoton/repo.svg?style=for-the-badge
[forks-url]: https://github.com/ZwCreatePhoton/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/ZwCreatePhoton/repo.svg?style=for-the-badge
[stars-url]: https://github.com/ZwCreatePhoton/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/ZwCreatePhoton/repo.svg?style=for-the-badge
[issues-url]: https://github.com/ZwCreatePhoton/repo/issues
[license-shield]: https://img.shields.io/github/license/ZwCreatePhoton/repo.svg?style=for-the-badge
[license-url]: https://github.com/ZwCreatePhoton/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ZwCreatePhoton
