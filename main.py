# import modules used to create program
import socket
import sys
from queue import Queue
import threading
from datetime import datetime

# target host to scan, also converts to ip from URL
host = socket.gethostbyname(input("Enter your target IP address or URL here: "))

# lock thread during print so we can get cleaner outputs
print_lock = threading.Lock()

# custom ports for user to scan later
startPort = 0
endPort = 0

# options for user to scan different ports
print("Select your scan type: ")
print("1: 1 to 1024 port")
print("2: 1 to 65535 port")
print("3: for custom port")
print("4: Exit")
# ask for input scan type
mode = int(input("Select any option: "))
# number of threads are we going to allow for
threadcount = int(input("Thread amount: "))

# if option 3 is selected user can enter the range of ports to start scan and end
if mode == 3:
    startPort = int(input("Enter starting port number: "))
    endPort = int(input("Enter ending port number: "))

# display target and sets starting time
print("-" * 50)
print(f"Target IP: {host}")
t1 = datetime.now()
print("Scanning started at: " + str(datetime.now()))
print("-" * 50)

# port scan fucntion
def scan(port):
    # creates a new socket and sets timeout to 0.5
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        # tries to connect to host
        s.connect((host, port))
        # no more sends/receives
        s.shutdown(socket.SHUT_RDWR)
        with print_lock:
          # display port that is open
            print(f"Port {port} is OPEN")
    except:
      # if port is closed, pass instead of returning error
        pass
    finally:
        # close the socket
        s.close()

# create the queue and threader
queue = Queue()

def getports(mode):
    # scanning port range from 1 to 1024
    if mode == 1:
        print("\nScanning Started")
        for port in range(1, 1024):
            queue.put(port)
    # scanning port range from 1 to 65535
    elif mode == 2:
        print("\nScanning Started")
        for port in range(1, 65535):
            queue.put(port)
    # scan custom ports
    elif mode == 3:
        print("\nScanning Started")
        for port in range(startPort, endPort):
            queue.put(port)
    # exiting
    elif mode == 4:
        print("Exiting")
        sys.exit()

# threader thread pulls a worker
# from a queue and processes it
def worker():
    while not queue.empty():
        # get a worker from the queue
        port = queue.get()
        if scan(port):
            print("Port {}".format(port))

# Creates, starts and manages our threads
# load ports depending on the mode
def run_scanner(threads, mode):
    getports(mode)
    # create a list for our threads
    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        # wait until thread terminates
        thread.join()

# run the thread count with the amount enter from user input and mode selected
run_scanner(threadcount, mode)

# stop the timer and print how long
print("-" * 50)
t2 = datetime.now()
stop = t2 - t1
print(f"Scanning complete in: {stop}")
