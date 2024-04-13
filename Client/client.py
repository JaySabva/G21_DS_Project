import xmlrpc.client

def write_file(filename):
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000/", allow_none=True)
    response = proxy.write(filename)
    print(response)
    if response[0] == True:
        addr = response[1]
        port = response[2]

        proxy1 = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
        data = input("Enter the data to write to the file: ")

        response = proxy1.write(filename, data, True)
        if response:
            unlock = proxy.unlock(filename)
            print(f"Data written to {filename}")
        else:
            print(f"Failed to write data to {filename}")
    else:
        print(f"File {filename} is locked by another client.")

def read_file(filename):
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000/", allow_none=True)
    response = proxy.read(filename)
    print(response)
    for server in response:
        addr = server[0]
        port = server[1]

        proxy1 = xmlrpc.client.ServerProxy(f"http://{addr}:{port}/", allow_none=True)
        data = proxy1.read(filename)
        if data != False:
            print(f"Data in {filename}:")
            print(data)
            break

    if len(response) == 0:
        print(f"File {filename} not found.")


if __name__ == "__main__":
    filename = input("Enter the filename to write: ")
    write_file(filename)

#     add functionality for reading the file
    filename = input("Enter the filename to read: ")
    read_file(filename)
