import socket
import sys
from queue import Queue
import threading
from datetime import datetime

# target host to scan, also converts to IP from URL
host = socket.gethostbyname(input("Enter your target IP address or URL here: "))

# lock thread during print so we can get cleaner outputs
print_lock = threading.Lock()

# custom ports for user to scan later
startPort = 0
endPort = 0

# options for user to scan different ports
print("Select your scan type:")
print("1: 1 to 1024 ports")
print("2: 1 to 65535 ports")
print("3: Custom port range")
print("4: Exit")
# ask for input scan type
mode = int(input("Select an option: "))
# number of threads to allow
threadcount = int(input("Thread amount: "))

# if option 3 is selected, user can enter the range of ports to start and end scan
if mode == 3:
    startPort = int(input("Enter the starting port number: "))
    endPort = int(input("Enter the ending port number: "))

# display target and set starting time
print("-" * 50)
print(f"Target IP: {host}")
t1 = datetime.now()
print("Scanning started at: " + str(datetime.now()))
print("-" * 50)

# port scan function
def scan(port):
    # create a new socket and set timeout to 0.5 seconds
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        # try to connect to the host
        s.connect((host, port))
        # no more sends/receives
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        # if port is closed, pass instead of returning an error
        pass
    finally:
        # close the socket
        s.close()
    return False

# create the queue and threader
queue = Queue()

def get_ports(mode):
    # scanning port range from 1 to 1024
    if mode == 1:
        print("\nScanning Started")
        for port in range(1, 1025):
            queue.put(port)
    # scanning port range from 1 to 65535
    elif mode == 2:
        print("\nScanning Started")
        for port in range(1, 65536):
            queue.put(port)
    # scan custom ports
    elif mode == 3:
        print("\nScanning Started")
        for port in range(startPort, endPort + 1):
            queue.put(port)
    # exiting
    elif mode == 4:
        print("Exiting")
        sys.exit()

# threader thread pulls a worker from the queue and processes it
def worker():
    while True:
        # get a worker from the queue
        port = queue.get()
        if scan(port):
            with print_lock:
                print(f"Port {port} is OPEN")
        # mark task as done
        queue.task_done()

# create, start, and manage threads
def run_scanner(threads, mode):
    get_ports(mode)
    # create a list for our threads
    thread_list = []

    for _ in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    # block until all tasks are done
    queue.join()

# run the scanner
run_scanner(threadcount, mode)
# stop the timer and print how long
print("-" * 50)
t2 = datetime.now()
stop = t2 - t1
print(f"Scanning complete in: {stop}")
