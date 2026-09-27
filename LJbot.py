import time
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
MODEL_URL = "https://imlive.com/live-sex-chat/cam-girls/laurajones0/"  # MODEL_ID
TELEGRAM_TOKEN = "8667818371:AAGZiEu5LK3KjFnWztw9kfRfPn--8EkJu7E"                   # Put your fresh token here
TELEGRAM_CHAT_ID = "410050399"                       # Put your chat ID here

# When hosting online, checking every 3 to 5 minutes (180-300 seconds) prevents the website from blocking your cloud IP.
CHECK_INTERVAL = 180 

def send_telegram_alert(message):
    """Sends a direct notification to your Telegram app."""
    url = f"https://telegram.org8667818371:AAGZiEu5LK3KjFnWztw9kfRfPn--8EkJu7E/sendMessage"
    payload = {"chat_id": 410050399, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending alert: {e}")

def check_model_status():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(MODEL_URL, headers=headers, timeout=10)
        if response.status_code != 200:
            return False
            
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()
        
        # Returns True if online keywords are detected
        if "online" in page_text or "chat now" in page_text:
            return True
        return False
        
    except Exception as e:
        print(f"Error parsing page: {e}")
        return False

def main():
    print("Cloud tracker started successfully.")
    is_online_last_check = False
    
    while True:
        is_online_now = check_model_status()
        
        # Triggers exactly when status changes from Offline -> Online
        if is_online_now and not is_online_last_check:
            send_telegram_alert("LJ's ON!")
            is_online_last_check = True
        elif not is_online_now:
            is_online_last_check = False
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()