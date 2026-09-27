import os
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
MODEL_URL = "https://imlive.com"

# Pulls your secure token from GitHub Secrets
TELEGRAM_TOKEN = os.environ.get("8667818371:AAGZiEu5LK3KjFnWztw9kfRfPn--8EkJu7E")
TELEGRAM_CHAT_ID = 410050399

def send_telegram_alert(message):
    """Sends a direct notification to your Telegram app."""
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable is missing.")
        return

    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Telegram alert sent successfully.")
        else:
            print(f"Telegram API responded with code: {response.status_code}")
    except Exception as e:
        print(f"Error sending alert: {e}")

def check_model_status():
    """Checks the target website for live indicators."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    # FIX: Added the missing try block to balance the except block below
    try:
        response = requests.get(MODEL_URL, headers=headers, timeout=10)   
        
        if response.status_code != 200:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()
        
        # If the direct indicator text is found, confirm she is offline
        if "currently offline" in page_text:
            print("Status: Offline")
            return False
            
        # Returns True if online keywords are detected
        if "online" in page_text or "chat now" in page_text:
            print("Status: Online!")
            return True
            
        return False
        
    except Exception as e:
        print(f"Error parsing page: {e}")
        return False

def main():
    print("Cloud tracker execution initiated.")
    
    # Executes exactly once per workflow trigger
    is_online_now = check_model_status()
    
    if is_online_now:
        send_telegram_alert("LJ's ON!")
    else:
        print("No status change detected. Exiting execution cleanly.")

if __name__ == "__main__":
    main()
