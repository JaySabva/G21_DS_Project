Instructions to Run

Prerequisites:

    Python 3.x installed on your system.
    Necessary permissions to run servers and the client application.

Setup:

    Clone the repository: 
	git clone https://github.com/JaySabva/IT559-G2_Remote_File_Operation.git

    Install dependencies:

	pip install openpyxl xmlrpc


Running the Servers:

    Master Server:
        Navigate to Master directory.
        Set hostID in Master.py.
        Run:

    python Master.py

Primary File Server:

    Navigate to FileServer_P directory.
    Set hostID in fileserver_P.py.
    Run:

    python Fileserver_P.py

Backup File Server:

    Navigate to FileServer_B directory.
    Set hostID in fileserver_B.py.
    Run:

        python fileserver_B.py

Running the Client Application:

    Client:
        Navigate to Client directory.
        Set SERVER_IP in client.py.
        Run:

        python client.py

Using the Client Application:

    Choose appropriate options to perform file operations.
    Follow on-screen instructions.