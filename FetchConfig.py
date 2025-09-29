import os
import re
import json
import logging
import random
import base64
import asyncio
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from telethon.tl.types import Message, MessageEntityTextUrl, MessageEntityUrl
from telethon.sessions import StringSession
from telethon.errors import ChannelInvalidError, PeerIdInvalidError
from statics import *


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = []
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "collector.log"), mode='w', encoding='utf-8')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
    

def load_channels():
    with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
        channels = json.load(f)
    logger.info(f"Loaded {len(channels)} channels from {CHANNELS_FILE}")
    return channels

def update_channels(channels):
    with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
        json.dump(channels, f, ensure_ascii=False, indent=4)
    logger.info(f"Updated {CHANNELS_FILE} with {len(channels)} channels")

if not os.path.exists(OUTPUT_DIR):
    logger.info(f"Creating directory: {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR)

def extract_proxies_from_message(message):
    proxies = []
    proxies += re.findall(PROXY_PATTERN, message.message or "")
    if hasattr(message, 'entities') and message.entities:
        text = message.message or ""
        for entity in message.entities:
            if isinstance(entity, (MessageEntityTextUrl, MessageEntityUrl)):
                if hasattr(entity, 'url'):
                    url = entity.url
                else:
                    offset = entity.offset
                    length = entity.length
                    url = text[offset:offset+length]
                if url.startswith("https://t.me/proxy?"):
                    proxies.append(url)
    return proxies

async def fetch_configs_and_proxies_from_channel(client, channel):
    configs = []
    proxies = []
    try:
        await client.get_entity(channel)
    except (ChannelInvalidError, PeerIdInvalidError, ValueError) as e:
        logger.error(f"Channel {channel} does not exist or is inaccessible: {str(e)}")
        return configs, proxies, False

    try:
        message_count = 0
        today = datetime.now().date()
        min_proxy_date = today - timedelta(days=1)

        async for message in client.iter_messages(channel, limit=200):
            message_count += 1
            if message.date:
                message_date = message.date.date()
            else:
                continue

            if message_date not in [today] and message_date < min_proxy_date:
                continue

            if isinstance(message, Message) and message.message:
                text = message.message

                for protocol, pattern in CONFIG_PATTERNS.items():
                    matches = re.findall(pattern, text)
                    if matches:
                        logger.info(f"Found {len(matches)} {protocol} configs in message from {channel}: {matches}")
                        configs.extend(matches)

                if message_date >= min_proxy_date:
                    proxy_links = extract_proxies_from_message(message)
                    if proxy_links:
                        logger.info(f"Found {len(proxy_links)} proxies in message from {channel}: {proxy_links}")
                        proxies.extend(proxy_links)
        logger.info(f"Processed {message_count} messages from {channel}, found {len(configs)} configs, {len(proxies)} proxies")
        return configs, proxies, True
    except Exception as e:
        logger.error(f"Failed to fetch from {channel}: {str(e)}")
        return configs, proxies, False

def save_configs(items, filename):
    output_file = os.path.join(OUTPUT_DIR, f"{filename}.txt")
    logger.info(f"Saving {filename} to {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        if items:
            for item in items:
                f.write(item + "\n")
            logger.info(f"Saved {len(items)} items to {output_file}")
        else:
            f.write(f"No items found for {filename}.\n")
            logger.info(f"No items found for {filename}, wrote placeholder to {output_file}")

def save_invalid_channels(invalid_channels):
    logger.info(f"Saving invalid channels to {INVALID_CHANNELS_FILE}")
    with open(INVALID_CHANNELS_FILE, "w", encoding="utf-8") as f:
        if invalid_channels:
            for channel in invalid_channels:
                f.write(f"{channel}\n")
            logger.info(f"Saved {len(invalid_channels)} invalid channels to {INVALID_CHANNELS_FILE}")
        else:
            f.write("No invalid channels found.\n")
            logger.info(f"No invalid channels found, wrote placeholder to {INVALID_CHANNELS_FILE}")

def save_channel_stats(stats):
    logger.info(f"Saving channel stats to {STATS_FILE}")
    stats_list = [{"channel": channel, **data} for channel, data in stats.items()]
    sorted_stats = sorted(stats_list, key=lambda x: x["score"], reverse=True)
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted_stats, f, ensure_ascii=False, indent=4)
    logger.info(f"Saved channel stats to {STATS_FILE}")

async def main():
    logger.info("Starting config+proxy collection process")
    invalid_channels = []
    channel_stats = {}

    if not SESSION_STRING:
        logger.error("No session string provided.")
        print("Please set TELEGRAM_SESSION_STRING in environment variables.")
        return
    if not API_ID or not API_HASH:
        logger.error("API ID or API Hash not provided.")
        print("Please set TELEGRAM_API_ID and TELEGRAM_API_HASH in environment variables.")
        return

    try:
        api_id = int(API_ID)
    except ValueError:
        logger.error("Invalid TELEGRAM_API_ID format. It must be a number.")
        print("Invalid TELEGRAM_API_ID format. It must be a number.")
        return

    TELEGRAM_CHANNELS = load_channels()
    session = StringSession(SESSION_STRING)

    try:
        async with TelegramClient(session, api_id, API_HASH) as client:
            if not await client.is_user_authorized():
                logger.error("Invalid session string.")
                print("Invalid session string. Generate a new one using generate_session.py.")
                return

            all_configs = []
            all_proxies = []
            valid_channels = []
            for channel in TELEGRAM_CHANNELS:
                logger.info(f"Fetching configs/proxies from {channel}...")
                print(f"Fetching configs/proxies from {channel}...")
                try:
                    channel_configs, channel_proxies, is_valid = await fetch_configs_and_proxies_from_channel(client, channel)
                    if not is_valid:
                        invalid_channels.append(channel)
                        channel_stats[channel] = {
                            "proxy_count": 0,
                            "total_configs": 0,
                            "score": 0,
                            "error": "Channel does not exist or is inaccessible"
                        }
                        continue

                    valid_channels.append(channel)
                    total_configs = len(channel_configs)
                    proxy_count = len(channel_proxies)
                    score = total_configs + proxy_count

                    channel_stats[channel] = {
                        "proxy_count": proxy_count,
                        "total_configs": total_configs,
                        "score": score
                    }
                    all_configs.extend(channel_configs)
                    all_proxies.extend(channel_proxies)
                except Exception as e:
                    invalid_channels.append(channel)
                    channel_stats[channel] = {
                        "proxy_count": 0,
                        "total_configs": 0,
                        "score": 0,
                        "error": str(e)
                    }
                    logger.error(f"Channel {channel} is invalid: {str(e)}")

            all_configs = list(set(all_configs))
            logger.info(f"Found {len(all_configs)} unique configs")
            all_proxies = list(set(all_proxies))

            save_configs(all_configs, FINAL_FETCH_FILE)
            save_configs(all_proxies, "proxies")
            save_invalid_channels(invalid_channels)
            save_channel_stats(channel_stats)
            update_channels(valid_channels)

    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
        print(f"Error in main loop: {str(e)}")
        return

    logger.info("Config+proxy collection process completed")

if __name__ == "__main__":
    asyncio.run(main())
