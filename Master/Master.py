import os
import openpyxl
from random import choice
from socket import *
from xmlrpc.server import SimpleXMLRPCServer

masterServer = SimpleXMLRPCServer(('localhost', 9000), logRequests=True, allow_none=True)

def lock(filename):
    excel_file = "Primary_Metadata.xlsx"

    if os.path.exists(excel_file):
        workbook = openpyxl.load_workbook(excel_file)
        worksheet = workbook.active

        file_exists = False
        for row in worksheet.iter_rows(values_only=True):
            if row[1] == filename:
                file_exists = True
                break

        if file_exists:
            for row in worksheet.iter_rows():
                if row[1].value == filename:
                    if row[4].value == "unlocked":
                        row[4].value = "locked"
                        addr = row[2].value
                        port = row[3].value
                        # Save the changes to the Excel file
                        workbook.save(excel_file)
                        return True, addr, port
                    else:
                        return False, None, None
        else:
            server_file = "Servers.xlsx"
            if os.path.exists(server_file):
                server_workbook = openpyxl.load_workbook(server_file)
                server_worksheet = server_workbook.active
                server_rows = list(server_worksheet.iter_rows(values_only=True))
                chosen_server = choice(server_rows)
                addr = chosen_server[1]
                port = chosen_server[2]

                worksheet.append([generate_id(), filename, addr, port, "locked"])
                workbook.save(excel_file)

                return True, addr, port
            else:
                return False, None, None
    else:
        return False, None, None

def write(filename):
    success, addr, port = lock(filename)
    if success:
        return True, addr, port
    else:
        return False, None, None

def generate_id():
    return len(openpyxl.load_workbook("Primary_Metadata.xlsx").active['A']) + 1

masterServer.register_function(write, 'write')
print("Master server is running...")
masterServer.serve_forever()
