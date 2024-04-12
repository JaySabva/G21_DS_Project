import xmlrpc.client

def write_file(filename):
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000/", allow_none=True)
    response = proxy.write(filename)
    print(response)
    if (response[0] == True):
        addr = response[1]
        port = response[2]
        port = 9001
        proxy = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
        data = input("Enter the data to write to the file: ")
        response = proxy.write(filename, data, True)
        if response:
            print(f"Data written to {filename}")
        else:
            print(f"Failed to write data to {filename}")

if __name__ == "__main__":
    filename = input("Enter the filename: ")
    write_file(filename)
