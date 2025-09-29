import os

SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING", None)
API_ID = os.getenv("TELEGRAM_API_ID", None)
API_HASH = os.getenv("TELEGRAM_API_HASH", None)
CHANNELS_FILE = "telegram_channels.json"
LOG_DIR = "Logs"
OUTPUT_DIR = "Config"
INVALID_CHANNELS_FILE = os.path.join(LOG_DIR, "invalid_channels.txt")
STATS_FILE = os.path.join(LOG_DIR, "channel_stats.json")
CONFIG_PATTERNS = {
    "vless": r"vless://[^\s]+",
    "vmess": r"vmess://[^\s]+",
    "shadowsocks": r"ss://[^\s]+",
    "trojan": r"trojan://[^\s]+"
}
PROXY_PATTERN = r"https:\/\/t\.me\/proxy\?server=[^&\s\)]+&port=\d+&secret=[^\s\)]+"
FINAL_FETCH_FILE = "all_configs"
