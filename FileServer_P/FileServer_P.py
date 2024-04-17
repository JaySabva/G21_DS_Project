import os
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import openpyxl
from random import choice
import threading
import time

FileServer_P = SimpleXMLRPCServer(('localhost', 9001), logRequests=True, allow_none=True)

def write(filename, data, primary, flag, timestamp=None):
    mode = 'a' if (os.path.exists(filename) and flag == True) else 'w'
    with open(filename, mode) as file:
        file.write(data + "\n")
    if primary:
        backup_thread = threading.Thread(target=send_to_backups, args=(filename, data, mode, timestamp))
        backup_thread.start()
        return True
    return True

def send_to_backups(filename, data, mode, timestamp):
#     time.sleep(10)
    backup_servers = []
    print("Sending data to backup servers")
    server_file = "Servers.xlsx"
    if os.path.exists(server_file):
        server_workbook = openpyxl.load_workbook(server_file)
        server_worksheet = server_workbook.active
        server_rows = list(server_worksheet.iter_rows(values_only=True))
        for row in server_rows[1:]:
            if row[2] != 9001:
                addr = row[1]
                port = row[2]
                proxy = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
                response = proxy.write(filename, data, False, mode == 'a', timestamp)
                if response:
                    backup_servers.append((filename, addr, port, timestamp))
    else:
        return False

    master_proxy = xmlrpc.client.ServerProxy("http://localhost:9000/", allow_none=True)
    master_proxy.send_backup_servers(backup_servers)
    return True

def read(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        return False

FileServer_P.register_function(write, "write")
FileServer_P.register_function(read, "read")

print("FileServer_P running on localhost:9001")
FileServer_P.serve_forever()
