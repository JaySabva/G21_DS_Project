import xmlrpc.client

# Define global variable for the IP address
SERVER_IP = "192.168.6.6"

def write_file(filename, mode):
    proxy = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:9000/")
    response = proxy.write(filename)
    if response[0]:
        addr = response[1]
        port = response[2]
        proxy1 = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:{port}/")
        data = input("Enter the data to write to the file: ")
        response = proxy1.write(filename, data, True, mode == 'a', response[3])  # Include timestamp
        if response:
            unlock = proxy.unlock(filename)
            print(f"Data written to {filename}")
        else:
            print(f"Failed to write data to {filename}")
    else:
        print(f"File {filename} is locked by another client.")

def read_file(filename):
    proxy = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:9000/", allow_none=True)
    response = proxy.read(filename)
    if response:
        for server in response:
            addr = server[0]
            port = server[1]
            proxy1 = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:{port}/", allow_none=True)
            data = proxy1.read(filename)
            if data:
                print(f"Data in {filename}:")
                print(data)
                break
        else:
            print(f"Data in {filename} not found.")
    else:
        print(f"File {filename} not found.")

if _name_ == "_main_":
    while True:
        print("\nSelect an option:")
        print("1. Write to a file")
        print("2. Read from a file")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            filename = input("Enter the filename to write: ")
            mode = input("Enter 'w' for write or 'a' for append: ")
            write_file(filename, mode)
        elif choice == '2':
            filename = input("Enter the filename to read: ")
            read_file(filename)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")