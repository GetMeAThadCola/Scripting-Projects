import requests
from requests.exceptions import RequestException
import tkinter as tk
from scapy.layers.inet import traceroute
from urllib.parse import urlparse

def is_reachable(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except RequestException:
        return False

def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc  # Extract the domain or IP address
    return domain

def trace_route(url):
    domain = extract_domain(url)
    
    # Check if the domain is a valid IP address or domain name
    if re.match(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", domain) or re.match(r"^[a-zA-Z0-9.-]+$", domain):
        try:
            results, _ = traceroute([domain], maxttl=30)
            return results
        except Exception as e:
            return [str(e)]
    else:
        return ["Invalid domain or IP address"]
                
def is_reachable(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except RequestException:
        return False

def trace_route(url):
    try:
        results, _ = traceroute(url, maxttl=30)
        return results
    except Exception as e:
        return [str(e)]

def check_url_reachability():
    url = url_entry.get()
    if is_reachable(url):
        result_label.config(text=f"The URL {url} is reachable.")
        traceroute_results = trace_route(url)
        if len(traceroute_results) > 0:
            ip_label.config(text="IP addresses in the traceroute:")
            ip_listbox.delete(0, tk.END)
            for result in traceroute_results:
                ip_listbox.insert(tk.END, result)
    else:
        result_label.config(text=f"The URL {url} is not reachable.")
        ip_label.config(text="")
        ip_listbox.delete(0, tk.END)

# Create a GUI window
root = tk.Tk()
root.title("URL Reachability Checker")

# Create and configure widgets
url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root, width=40)
url_entry.pack()

check_button = tk.Button(root, text="Check Reachability", command=check_url_reachability)
check_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

ip_label = tk.Label(root, text="")
ip_label.pack()

ip_listbox = tk.Listbox(root, height=10, width=40)
ip_listbox.pack()

# Start the GUI application
root.mainloop()
