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
        try:
            response = proxy1.write(filename, data, True, mode == 'a', response[3])  # Include timestamp
            if response:
                unlock = proxy.unlock(filename)
                print(f"Data written to {filename}")
            else:
                print(f"Failed to write data to {filename}")
        except Exception as e:
            unlock = proxy.unlock(filename)
            print(f"Error occurred while writing to {filename}: {e} - Primary server is down.")
    else:
        print(f"File {filename} is locked by another client.")

def read_file(filename):
    proxy = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:9000/", allow_none=True)
    try:
        response = proxy.read(filename)
        if response:
            for server in response:
                addr = server[0]
                port = server[1]
                proxy1 = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:{port}/", allow_none=True)
                try:
                    data = proxy1.read(filename)
                    if data:
                        print(f"Data in {filename}:")
                        print(data)
                        break
                except Exception as e:
                    print(f"Backup server {addr}:{port} is down. trying another backup server.")
            else:
                print(f"Data in {filename} not found. - Backup servers are down.")
        else:
            print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error occurred while accessing {filename}: {e}")

if __name__ == "__main__":
    while True:
        print("\nSelect an option:")
        print("1. Write to a file")
        print("2. Read from a file")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            filename = input("Enter the filename to write: ")
            mode = input("Enter 'w' for write or 'a' for append: ")
            while (mode != 'w') and (mode != 'a'):
                print("Invalid mode. Please enter 'w' or 'a'.")
                mode = input("Enter 'w' for write or 'a' for append: ")
                continue
            write_file(filename, mode)
        elif choice == '2':
            filename = input("Enter the filename to read: ")
            read_file(filename)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
