#!/usr/bin/env python3
import json
import subprocess
import requests
import pprint
import re
from bs4 import BeautifulSoup


def get_smartnodesnr():
     source = requests.get("https://explorer.raptoreum.com/api/getmasternodecount").text
     soup = BeautifulSoup(source, 'html.parser')
     smartnodes = str(soup)
     smartnodesnr = int(smartnodes[0:3])
     return smartnodesnr

def get_rtm_supply():
    r = requests.get(url="https://explorer.raptoreum.com/api/supply")
    return r.json()


def get_btc_rate():
    r = requests.get(url="https://blockchain.info/ticker")
    rj = r.json()
    return rj


def get_rtm_btc():
    source = requests.get("https://tradeogre.com/api/v1/ticker/BTC-RTM").text
    soup = BeautifulSoup(source, 'html.parser')
    rtmbtc = str(soup)
    rtmbtcprice = float(rtmbtc[53:63])
    return rtmbtcprice


def convert_to(c, v):
    r = requests.get(url="https://blockchain.info/tobtc?currency=" + c + "&value=" + v)
    return r


def data_to_json(d):
    with open("data.json", "w") as f:
        json.dump(d, f)


def build_data():
    daily_blocks = 720
    smartnode_rewards_rtm = 1000
    rtm_btc = get_rtm_btc()
    btc_usd = get_btc_rate()['USD']['last']
    rtm_usd = btc_usd * rtm_btc
    smartnode_active = get_smartnodesnr()
    smartnode_reward_avg = (daily_blocks * smartnode_rewards_rtm) / smartnode_active
    data_pile = {
        "rtmdaily": smartnode_reward_avg,
        "usddaily": smartnode_reward_avg * rtm_usd,
        "usdprice": rtm_usd,
        "btcprice": rtm_btc,
        "mncount": smartnode_active,
        "totalsupply": get_rtm_supply(),
        "pricebtcusd": btc_usd
    }
    data_to_json(data_pile)


build_data()
