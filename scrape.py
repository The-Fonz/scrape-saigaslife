import argparse
import json
import logging
import os

import requests


URL = "https://www.saigaslife.nl/api/Post"

# Increment the version if making incompatible changes
LOCAL_STORE = os.path.join(os.path.dirname(__file__), "posts_seen_v001.json")


def get_msgs():
    return requests.get(URL).json()


def get_unseen(msgs_current):
    msgs_seen = list()
    if os.path.exists(LOCAL_STORE):
        with open(LOCAL_STORE, 'r') as f:
            msgs_seen = json.load(f)
            logging.debug("Opened local store %s with %d messages, "
                          "current messages are %d", LOCAL_STORE, len(msgs_seen), len(msgs_current))
    # Note: Set comprehension not dict!
    msg_ids_seen = {msg['id'] for msg in msgs_seen}
    msg_ids_current = {msg['id'] for msg in msgs_current}
    # Save all
    with open(LOCAL_STORE, 'w') as f:
        logging.debug("Saving to %s", LOCAL_STORE)
        json.dump(msgs_current, f)
    msg_ids_new = msg_ids_current - msg_ids_seen
    msgs_new = [msg for msg in msgs_current if msg['id'] in msg_ids_new]
    # Nice to return a sorted list with newest first
    return sorted(list(msgs_new ), key=lambda msg: msg['id'], reverse=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # Make a simple cmdline interface for easier debugging
    parser = argparse.ArgumentParser(
        description=f"Scrape the site {URL} for new messages and remember these in a local file.")
    parser.add_argument('--force-new', type=int,
                        help="Force the first n messages received to be new, for debugging purposes")
    args = parser.parse_args()

    msgs = get_msgs()
    msgs_unseen = get_unseen(msgs)

    if args.force_new:
        msgs_unseen = msgs[:args.force_new]

    # Print titles only
    print(", ".join([msg['title'] for msg in msgs_unseen]))
