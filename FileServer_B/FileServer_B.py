import os
import openpyxl
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from random import choice

# Code for FileServer_B.py

FileServer_B = SimpleXMLRPCServer(('localhost', 9002), logRequests=True, allow_none=True)

def write(filename, data, primary):
    print("Got")
    file = open(filename, "w")
    if file:
        file.write(data)
        file.close()
        if primary == True:
            print("Sending data to backup servers")
            server_file = "Servers.xlsx"
            if os.path.exists(server_file):
                server_workbook = openpyxl.load_workbook(server_file)
                server_worksheet = server_workbook.active
                server_rows = list(server_worksheet.iter_rows(values_only=True))
                for row in server_rows:
                    if row[3] != 9002:  # Check if the port is different from the primary server's port
                        addr = row[2]
                        port = row[3]
                        proxy = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
                        proxy.write(filename, data, False)
            else:
                return False
        return True
    else:
        file = open(filename, "x")
        file.write(data)
        file.close()
        if primary == True:
            print("Sending data to backup servers")
            server_file = "Servers.xlsx"
            if os.path.exists(server_file):
                server_workbook = openpyxl.load_workbook(server_file)
                server_worksheet = server_workbook.active
                server_rows = list(server_worksheet.iter_rows(values_only=True))
                for row in server_rows:
                    if row[3] != 9002:  # Check if the port is different from the primary server's port
                        addr = row[2]
                        port = row[3]
                        proxy = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
                        proxy.write(filename, data, False)
            else:
                return False
        return True

FileServer_B.register_function(write, "write")

print("FileServer_B running on localhost:9002")
FileServer_B.serve_forever()
