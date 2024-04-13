import os
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import openpyxl
from random import choice

FileServer_B = SimpleXMLRPCServer(('localhost', 9002), logRequests=True, allow_none=True)

def write(filename, data, primary):
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode) as file:
        file.write(data + "\n")

    if primary:
        backup_servers = []
        print("Sending data to backup servers")
        server_file = "Servers.xlsx"
        if os.path.exists(server_file):
            server_workbook = openpyxl.load_workbook(server_file)
            server_worksheet = server_workbook.active
            server_rows = list(server_worksheet.iter_rows(values_only=True))

            for row in server_rows[1:]:
                if row[2] != 9002:
                    addr = row[1]
                    port = row[2]
                    proxy = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
                    response = proxy.write(filename, data, False)
#                     print(response)
                    if response:
                        backup_servers.append((filename, addr, port))
        else:
            return False

#         print(backup_servers)
        master_proxy = xmlrpc.client.ServerProxy("http://localhost:9000/", allow_none=True)
        master_proxy.send_backup_servers(backup_servers)
        return True

    return True

def read(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        return False

FileServer_B.register_function(write, "write")
FileServer_B.register_function(read, "read")

print("FileServer_B running on localhost:9002")
FileServer_B.serve_forever()
