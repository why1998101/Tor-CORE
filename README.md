## Tor@CORE
Final Works for Project Tor@CORE
### File Catalog
- code: contain implementations of client, relay, and directory authority, together with a naive echo server
- data: contain four test scripts, test result logs, a parser, and parsed logs
- screenshots: contain screenshots of each conponent running
- tor.xml: the CORE layout used throughout this project
- report.pdf: final report of this project
- presentation.pdf: slides used in presentation
### How to run the code
- **client:** *python3 pyclient.py <server_ip> <server_port>*
- **directory authority:** *python3 pydirectory.py*
- **relay:** *python3 pyrelay.py <my_port> <my_type: guard/middle/exit>*
- **server:** *python3 pyserver.py <my_port>*
- Note: pydirectory should be run directly in the root path of a virtual node since it uses relative path when creating the file to store relay info, if not run in root path, multiple DAs will end up sharing one file which is not desired and can cause errors
### References of the entire project not listed in final report
- https://svn-archive.torproject.org/svn/projects/design-paper/tor-design.html
- https://2019.www.torproject.org/docs/documentation.html.en
- https://blog.torproject.org/top-changes-tor-2004-design-paper-part-1/
- https://blog.torproject.org/top-changes-tor-2004-design-paper-part-2/
- https://blog.torproject.org/top-changes-tor-2004-design-paper-part-3/
- https://gitweb.torproject.org/torspec.git/tree/tor-spec.txt
- https://gitweb.torproject.org/tor.git/tree/
- https://www.freehaven.net/anonbib/cache/ndss13-relay-selection.pdf
- https://github.com/pycepa/pycepa
- https://github.com/torproject/tor
- https://github.com/mmcloughlin/pearl
 
