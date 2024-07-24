import requests
import socket
import time
import os
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict, deque

RESET = "\033[0m"
HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

def print_header(title):
    os.system("clear")
    print(HEADER + "="*50 + RESET)
    print(HEADER + f"{title}".center(50) + RESET)
    print(HEADER + "Author: dionealfarisi | Credit: Lab505" + RESET)
    print(HEADER + "Join Us: t.me/ninepillar | t.me/Lab505" + RESET)
    print(HEADER + "="*50 + RESET)

def connect_to_dns(host):
    try:
        ip_address = socket.gethostbyname(host)
        print(OKBLUE + f"Host: {RESET} {OKGREEN + host + RESET }")
        print(BOLD + f"IP Address: {ip_address}" + RESET)
        return ip_address
    except socket.gaierror as e:
        print(f"Failed to get IP address for {host}: {e}")
        return None

def find_pages(url, page_list, file_name, page_type):
    host = url.split("//")[-1].split("/")[0]
    
    ip_address = connect_to_dns(host)
    
    if not ip_address:
        return

    with open(file_name, "a") as file:
        file.write(f"\n{host}: {ip_address}\n")

    print(f"Searching for {page_type} pages...\n")
    found_any = False

    for link in page_list:
        url_link = url + link
        try:
            response = requests.get(url_link)
            status_code = response.status_code
            if status_code == 200:
                found_any = True
                with open(file_name, "a") as file:
                    file.write(f"\t=> URL: {url_link}\n\t=> STATUS: {status_code}\n")
                print(OKGREEN + f"[FOUND] {link} : {status_code}" + RESET)
            else:
                print(WARNING + f"[NOT FOUND] {link} : {status_code}" + RESET)
        except requests.exceptions.RequestException as e:
            print(FAIL + f"[ERROR] Failed to access {url_link}: {e}" + RESET)

    if not found_any:
        print(f"No {page_type} pages found.")

def find_admin_pages():
    print_header("Admin Page Finder")
    url = str(input("Enter URL for admin page search: "))
    admin_pages = [
        "/admin.php", "/admin", "/login", "/login.php", "/admin/index.php", "/login/index.php",
        "/admin/login", "/admin/login.php", "/administrator", "/administrator/index.php",
        "/administrator/login.php", "/admin1.php", "/admin2.php", "/admin3.php", "/admin4.php",
        "/admin5.php", "/usuarios", "/usuario", "/member", "/members", "/user", "/users",
        "/account", "/accounts", "/signin", "/sign_in", "/sign-in", "/signup", "/sign_up",
        "/sign-up", "/secure", "/webadmin", "/controlpanel", "/adminpanel", "/admin_area",
        "/admin_site", "/admincontrol", "/admincontrolpanel", "/admin-login", "/cpanel",
        "/kcfinder", "/panel", "/adminarea", "/adm", "/cms", "/admin/home", "/admin/dashboard",
        "/admin/portal", "/admin/system", "/admin/manage", "/management", "/admin-console",
        "/admin-console/login", "/admin-console/index", "/control", "/controlpanel/login",
        "/backend", "/backend/login", "/backend/index", "/cp", "/cp/login", "/cp/index",
        "/admin/home.php", "/admin/dashboard.php", "/admin/portal.php", "/admin/system.php",
        "/admin/manage.php", "/management.php", "/admin-console.php", "/admin-console/login.php",
        "/admin-console/index.php", "/control.php", "/controlpanel/login.php", "/backend.php",
        "/backend/login.php", "/backend/index.php", "/cp.php", "/cp/login.php", "/cp/index.php",
        "/admin_area/login", "/admin_area/index", "/admin_area/admin.php", "/admin_area/dashboard",
        "/admin_login", "/admin_login.php", "/admin_login/index.php", "/admin_login/login",
        "/admin_login/dashboard", "/admin_portal", "/admin_portal.php", "/admin_portal/index",
        "/admin_portal/login", "/admin_portal/dashboard", "/portal", "/portal/login", "/portal/index",
        "/portal/admin", "/portal/admin.php", "/adminsys", "/adminsys/login", "/adminsys/index",
        "/adminsys/admin.php", "/adminsys/dashboard", "/sysadmin", "/sysadmin/login", "/sysadmin/index",
        "/sysadmin/admin.php", "/sysadmin/dashboard", "/administration", "/administration/login",
        "/administration/index", "/administration/admin.php", "/administration/dashboard",
        "/webmaster", "/webmaster/login", "/webmaster/index", "/webmaster/admin.php", "/webmaster/dashboard",
        "/moderator", "/moderator/login", "/moderator/index", "/moderator/admin.php", "/moderator/dashboard",
        "/root", "/root/login", "/root/index", "/root/admin.php", "/root/dashboard", "/superadmin",
        "/superadmin/login", "/superadmin/index", "/superadmin/admin.php", "/superadmin/dashboard"
    ]
    find_pages(url, admin_pages, "admin_url_list.txt", "admin")

def find_upload_pages():
    print_header("Upload Page Finder")
    url = str(input("Enter URL for upload page search: "))
    upload_pages = [
        "/upload.php", "/upload", "/file_upload", "/file_upload.php", "/uploadfile", "/uploadfile.php",
        "/uploads", "/uploads.php", "/fileuploads", "/fileuploads.php", "/uploader", "/uploader.php",
        "/fileuploader", "/fileuploader.php", "/file_uploads", "/file_uploads.php", "/media_upload",
        "/media_upload.php", "/image_upload", "/image_upload.php", "/img_upload", "/img_upload.php",
        "/photo_upload", "/photo_upload.php", "/video_upload", "/video_upload.php", "/doc_upload",
        "/doc_upload.php", "/documents_upload", "/documents_upload.php", "/file_manager", "/file_manager.php",
        "/media_manager", "/media_manager.php", "/document_manager", "/document_manager.php", "/upload_files",
        "/upload_files.php", "/upload_images", "/upload_images.php", "/upload_videos", "/upload_videos.php",
        "/upload_docs", "/upload_docs.php", "/upload_documents", "/upload_documents.php"
    ]
    find_pages(url, upload_pages, "upload_url_list.txt", "upload")

def find_config_pages():
    print_header("Configuration Page Finder")
    url = str(input("Enter URL for configuration page search: "))
    config_pages = [
        "/config.php", "/config", "/settings.php", "/settings", "/configuration.php", "/configuration",
        "/admin/config.php", "/admin/config", "/admin/settings.php", "/admin/settings", "/admin/configuration.php",
        "/admin/configuration", "/system/config.php", "/system/config", "/system/settings.php", "/system/settings",
        "/system/configuration.php", "/system/configuration"
    ]
    find_pages(url, config_pages, "config_url_list.txt", "configuration")

def find_docs_pages():
    print_header("Documentation Page Finder")
    url = str(input("Enter URL for documentation page search: "))
    docs_pages = [
        "/docs", "/docs.php", "/documentation", "/documentation.php", "/api", "/api/docs", "/api/docs.php",
        "/manual", "/manual.php", "/guide", "/guide.php", "/help", "/help.php", "/support", "/support.php",
        "/wiki", "/wiki.php", "/info", "/info.php"
    ]
    find_pages(url, docs_pages, "docs_url_list.txt", "documentation")

def find_login_pages():
    print_header("Login Page Finder")
    url = str(input("Enter URL for login page search: "))
    login_pages = [
        "/login", "/login.php", "/user/login", "/user/login.php", "/admin/login", "/admin/login.php",
        "/signin", "/signin.php", "/account/login", "/account/login.php", "/auth/login", "/auth/login.php"
    ]
    find_pages(url, login_pages, "login_url_list.txt", "login")

def find_register_pages():
    print_header("Register Page Finder")
    url = str(input("Enter URL for register page search: "))
    register_pages = [
        "/register", "/register.php", "/user/register", "/user/register.php", "/signup", "/signup.php",
        "/account/register", "/account/register.php", "/auth/register", "/auth/register.php"
    ]
    find_pages(url, register_pages, "register_url_list.txt", "register")

def find_reset_password_pages():
    print_header("Reset Password Page Finder")
    url = str(input("Enter URL for reset password page search: "))
    reset_password_pages = [
        "/reset-password", "/reset-password.php", "/user/reset-password", "/user/reset-password.php",
        "/password-reset", "/password-reset.php", "/account/reset-password", "/account/reset-password.php",
        "/auth/reset-password", "/auth/reset-password.php"
    ]
    find_pages(url, reset_password_pages, "reset_password_url_list.txt", "reset password")

def extract_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        hrefs = [link['href'] for link in links]
        return hrefs
    except requests.exceptions.RequestException as e:
        print(FAIL + f"Failed to retrieve links from {url}: {e}" + RESET)
        return []

def build_tree(hrefs):
    tree = defaultdict(list)
    for href in hrefs:
        parts = href.strip('/').split('/')
        if parts:
            tree[parts[0]].append('/'.join(parts[1:]))
    return tree

def print_tree(tree, indent=0):
    for key, values in tree.items():
        print(' ' * indent + OKGREEN + key + RESET)
        sub_tree = build_tree(values)
        if sub_tree:
            print_tree(sub_tree, indent + 2)

def find_website_structure(url, max_depth=2, retry_attempts=3):
    visited = set()
    queue = deque([(url, 0)])
    site_structure = defaultdict(list)
    while queue:
        current_url, depth = queue.popleft()

        if depth > max_depth:
            continue

        if current_url in visited:
            continue

        for attempt in range(retry_attempts):
            try:
                response = requests.get(current_url, timeout=10)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Attempt {attempt + 1} failed to access {current_url}: {e}")
                time.sleep(2) 
        else:
            print(f"[ERROR] All attempts failed for {current_url}")
            continue

        visited.add(current_url)
        print(f"{'  ' * depth}Page: {current_url}")

        try:
            hrefs = extract_links(current_url)
            for href in hrefs:
                full_url = urljoin(current_url, href)
                parsed_url = urlparse(full_url)
                if parsed_url.netloc == urlparse(url).netloc:
                    site_structure[current_url].append(full_url)
                    queue.append((full_url, depth + 1))
        except Exception as e:
            print(f"[ERROR] Failed to parse website structure: {e}")

    if site_structure:
        print("\nWebsite Structure:")
        print_tree(build_tree([url for url_list in site_structure.values() for url in url_list]))
    else:
        print("No structure could be built. Please check the URL or try again later.")

def run_hammer():
    print_header("Hammer Script")
    print("Ensure you have 'headers.txt' in the same directory.")
    host = input("IP address: ")
    port = input("Port (default 80): ")
    port = port if port else '80'
    turbo = input("Threads (default 135): ")
    turbo = turbo if turbo else '135'
    
    command = f"python3 hammer.py -s {host} -p {port} -t {turbo}"
    print(f"Running...")
    
    subprocess.run(command, shell=True)

def main():
    while True:
        print_header("Website Page Finder")
        print(OKBLUE + "Choose an option:" + RESET)
        print(OKBLUE + "1. Find Admin Pages" + RESET)
        print(OKBLUE + "2. Find Upload Pages" + RESET)
        print(OKBLUE + "3. Find Configuration Pages" + RESET)
        print(OKBLUE + "4. Find Documentation Pages" + RESET)
        print(OKBLUE + "5. Find Login Pages" + RESET)
        print(OKBLUE + "6. Find Register Pages" + RESET)
        print(OKBLUE + "7. Find Reset Password Pages" + RESET)
        print(OKBLUE + "8. Find Website Structure Pages" + RESET)
        print(OKBLUE + "9. DDOS using Hammer" + RESET)
        print(OKBLUE + "0. Exit" + RESET)
        choice = input("Enter your choice: ")

        if choice == '1':
            find_admin_pages()
        elif choice == '2':
            find_upload_pages()
        elif choice == '3':
            find_config_pages()
        elif choice == '4':
            find_docs_pages()
        elif choice == '5':
            find_login_pages()
        elif choice == '6':
            find_register_pages()
        elif choice == '7':
            find_reset_password_pages()
        elif choice == '8':
            url = str(input(OKGREEN + "\nEnter URL: " + RESET))
            find_website_structure(url , max_depth=2)
        elif choice == '9':
            run_hammer()
        elif choice == '0':
            print(OKGREEN + "Exiting program. Goodbye!" + RESET)
            break
        else:
            print(FAIL + "Invalid choice. Please try again." + RESET)

if __name__ == "__main__":
    main()