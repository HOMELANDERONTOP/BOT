import time
import requests

def ping_codespace(url, interval=300):
    """Ping the GitHub Codespace at regular intervals to keep it alive.
    
    Parameters:
        url (str): The URL of your Codespace to ping.
        interval (int): Number of seconds to wait between pings (default is 300 seconds, or 5 minutes).
    """
    while True:
        try:
            response = requests.get(url)  # Make a request to the specified URL
            print(f"Pinging Codespace... Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    codespace_url = 'https://hallowed-spell-q7p6xj5j4jw7f9xr4.github.dev/'  # Change this to your Codespace URL if necessary
    ping_codespace(codespace_url)