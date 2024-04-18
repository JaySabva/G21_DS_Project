import os
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import openpyxl
from random import choice
import threading
import time
import heapq

hostID = "192.168.6.6"
FileServer_P = SimpleXMLRPCServer((hostID, 9001), logRequests=True, allow_none=True)

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def peek(self):
        return self.heap[0] if self.heap else None

    def empty(self):
        return len(self.heap) == 0

server_heap = {}
server_file = "Servers.xlsx"  # Load the server.xlsx file once
if os.path.exists(server_file):
    server_workbook = openpyxl.load_workbook(server_file)
    server_worksheet = server_workbook.active
else:
    print("Server file not found!")

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
    backup_servers = []
    print("Sending data to backup servers")
    if os.path.exists(server_file):
        server_rows = list(server_worksheet.iter_rows(values_only=True))
        for row in server_rows[1:]:
            if row[2] != 9001:
                addr = hostID
                port = row[2]

                if (addr, port) not in server_heap:
                    server_heap[(addr, port)] = MinHeap()

                server_heap[(addr, port)].push((timestamp, filename, data, mode))
                try:
                    proxy = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
                    while not server_heap[(addr, port)].empty():
                        timestamp, filename, data, mode = server_heap[(addr, port)].peek()
                        response = proxy.write(filename, data, False, mode == 'a', timestamp)
                        if response:
                            server_heap[(addr, port)].pop()
                            backup_servers.append((filename, addr, port, timestamp))

                except Exception as e:
                    print(f"Error connecting to {addr}:{port}: {e}")
#                     if (addr, port) not in server_heap:
#                         server_heap[(addr, port)] = MinHeap()
#
#                     server_heap[(addr, port)].push((timestamp, filename, data, mode))

# for printing the heap
#                     temp = MinHeap()
#                     while not server_heap[(addr, port)].empty():
#                         timestamp, filename, data, mode = server_heap[(addr, port)].pop()
#                         print(timestamp, filename, data, mode)
#                         temp.push((timestamp, filename, data, mode))
#
#                     server_heap[(addr, port)] = temp

    else:
        return False

    master_proxy = xmlrpc.client.ServerProxy(f"http://{hostID}:9000/", allow_none=True)
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
