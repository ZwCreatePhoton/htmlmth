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
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
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

### Prerequisites

* Python2
* libtidy-dev


### Installation

1. Install libtidy-dev
   ```sh
   sudo apt install libtidy-dev
   ```
2. Install python requirements
   ```sh
   python -m pip install --ignore-installed -r requirements.txt
   ```
3. Clone the repo
   ```sh
   git clone https://github.com/ZwCreatePhoton/HTMLMTH.git
   ```

<!-- USAGE EXAMPLES -->
## Usage

There are three scripts of interest: [_output_cases.py_](htmlmth/output_cases.py), [_EvasionHTTPServer.py_](htmlmth/EvasionHTTPServer.py), and  [_scripting_encoder_server.py_](htmlmth/scripting_encoder_server.py)


**EvasionHTTPServer.py**

This script implements the HTTP server that applies lists of evasions (AKA "cases") dynamically.

EvasionHTTPServer Usage Example 1

```sh
python htmlmth/EvasionHTTPServer.py -i 0.0.0.0 -p 8000 -ipv 4 -sesh 127.0.0.1 -sesp 5000 -b baselines/example.html -c cases/example.py -tc example-middle-011
```

Host an Evasion HTTP server instance on 0.0.0.0:8000 that hosts the file [_baselines/example3.html_](baselines/example3.html) as the baseline content and uses the case [*example-middle-011* from cases/example.py](https://github.com/ZwCreatePhoton/htmlmth/blob/main/cases/example.py#L15) as the applied evasion.

When http://SERVERIP:8000/ is visited, the returned content should be the baseline with the following modifications (example-middle-011):

1. HTML comments removed AKA the evasion: `htmlmth.evasions.html.remove_html_comments`
2. 414 HTTP status code AKA evasion: `htmlmth.evasions.http.status_code_4xx.parameterize(statuscode=414)`


EvasionHTTPServer Usage Example 2

```sh
python htmlmth/EvasionHTTPServer.py -i 0.0.0.0 -p 8000 -ipv 4 -sesh 127.0.0.1 -sesp 5000 -b baselines/example3.yaml -c cases/example.py -tc cases/example3.yaml
```

Host an Evasion HTTP server instance on 0.0.0.0:8000 that hosts the baseline HTTP resources defined in [_baselines/example3.yaml_](baselines/example3.yam;) as the baseline contents and uses the cases listed in [*cases/example3.yaml*](https://github.com/ZwCreatePhoton/htmlmth/blob/main/cases/example3.yaml) and defined in [*cases/example.py*](https://github.com/ZwCreatePhoton/htmlmth/blob/main/cases/example.py#L14) as the applied evasions.

When http://SERVERIP:8000/example.html is visited, the returned content should be the baseline with the following modifications (example-middle-011):

1. HTML comments removed AKA the evasion: `htmlmth.evasions.html.remove_html_comments`
2. 414 HTTP status code AKA evasion: `htmlmth.evasions.http.status_code_4xx.parameterize(statuscode=414)`

When http://abc.com:8000/ is visited (where abc.com points to SERVERIP), the returned content should be the baseline with the following modifications (example-null-001):
1. No modifications


**output_cases.py**

This script serializes evaded content to disk.

output_cases Usage Example 1

```sh
rm -r out ; mkdir out ; ./htmlmth/output_cases.py -sesp 5000 -sesh 127.0.0.1 -sesp 5000 -o out -b baselines/example3.yaml -c cases/example.py -bch abc.com -ld
```

Serialize the evaded content to the _out_ directory using the baseline HTTP resources defined in [_baselines/example3.yaml_](baselines/example3.yaml) as the baseline contents and all the cases defined in [*cases/example.py*](https://github.com/ZwCreatePhoton/htmlmth/blob/main/cases/example.py#L14) as the applied evasions. Content is served up as if it were accessed using the hostname *abc.com*. Long descriptions will be printed to stdout.


**scripting_encoder_server.py**

Some evasions utilize a closed encoder by Microsoft. This script acts as a server that uses the encoder to return back encoded content. The server is required by some evasions to generate the evaded content. This script must run on a Windows host accessible from the machine running *output_cases.py* or *EvasionHTTPServer.py*.

When using *output_cases.py* or *EvasionHTTPServer.py*, specify the ip (using the **-sesh** parameter) and the port (using the **-sesp** parameter) that the script is listening on. The default port is 5000.  

If an evasion uses scripting_encoder_server.py and it is not accessible, a requests.exceptions.ConnectionError will occur.

```bash
python.exe -m pip install flask
set FLASK_APP=scripting_encoder_server.py
python.exe -m flask run --host=0.0.0.0
```

_To see the available evasions, please refer to the [evasions](htmlmth/evasions) directory._

_To see practical examples of cases, please refer to the [HtmlmthCases](https://github.com/ZwCreatePhoton/htmlmthcases) repo._



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/ZwCreatePhoton/htmlmth/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



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
