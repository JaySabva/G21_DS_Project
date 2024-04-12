import os
import openpyxl
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from random import choice


FileServer_P = SimpleXMLRPCServer(('localhost', 9001), logRequests=True, allow_none=True)

def write(filename, data, primary):
    file = open(filename, "w")
    if file:
        file.write(data)
        file.close()
        if primary == True:
            print("Sending data to backup servers - 1")
            server_file = "Servers.xlsx"
            if os.path.exists(server_file):
                server_workbook = openpyxl.load_workbook(server_file)
                server_worksheet = server_workbook.active
                server_rows = list(server_worksheet.iter_rows(values_only=True))
                print("File Server P: ", server_rows)

                for row in server_rows[1:]:
                    if row[2] != 9001:
                        addr = row[1]
                        port = row[2]
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
            print("Sending data to backup servers - 2")
            server_file = "Servers.xlsx"
            if os.path.exists(server_file):
                server_workbook = openpyxl.load_workbook(server_file)
                server_worksheet = server_workbook.active
                server_rows = list(server_worksheet.iter_rows(values_only=True))
                for row in server_rows:
                    if row[3] != 9001:
                        addr = row[2]
                        port = row[3]
                        proxy = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
                        proxy.write(filename, data, False)
            else:
                return False
        return True

FileServer_P.register_function(write, "write")

print("FileServer_P running on localhost:9001")
FileServer_P.serve_forever()
