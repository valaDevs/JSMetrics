import requests
import re
from colorama import Back, Fore, Style

logo = '''
       _______ __  ___     __       _          
      / / ___//  |/  /__  / /______(_)_________
 __  / /\__ \/ /|_/ / _ \/ __/ ___/ / ___/ ___/
/ /_/ /___/ / /  / /  __/ /_/ /  / / /__(__  ) 
\____//____/_/  /_/\___/\__/_/  /_/\___/____/  
                 Author: Vabro
                 Github: github.com/valaDevs                                          
'''

def find_js_files(url):
    response = requests.get(url)
    html_content = response.text

    # Find JavaScript file URLs in the HTML content
    js_files = re.findall(r'<script.*?src=["\'](.*?)["\']', html_content)

    # Filter out external URLs and get absolute URLs
    base_url = response.url
    js_files = [file if file.startswith('http') else base_url + file for file in js_files]

    return js_files

def find_event_listeners(js_files):
    event_files = []
    
    for file in js_files:
        response = requests.get(file)
        js_content = response.text
        
        # Search for addEventListener occurrences in the JavaScript file
        if re.search(r'\.addEventListener*\(', js_content):
            event_files.append(file)
    
    return event_files

# Main script
print(Fore.CYAN + logo)
url = input(Fore.GREEN + "[+] Enter target URL (with HTTPS): ")
js_files = find_js_files(url)
event_files = find_event_listeners(js_files)

if event_files:
    print(Fore.YELLOW + "[+] JavaScript files with addEventListeners:")
    print("")
    for file in event_files:
        print(file)
else:
    print(Fore.RED + "[-] No JavaScript files with addEventListeners found.")
