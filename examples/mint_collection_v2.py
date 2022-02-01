import sys
sys.path.append('../')
from pinatapy import PinataPy
from py_rmrk_tools import *
from py_rmrk_tools_config import *
import pinatapy


keypair = keypair_from_mnemonic(wallet_mnemonic)
pinata = PinataPy(pinata_api_key, pinata_secret_api_key)

external_url = "https://singular.rmrk.app"
collection_logo_filename = "./pics/test_logo.jpg"
collection_name = "Test collection #1"
collection_symbol = "TEST1"
max_amount = 500
description_text = "test collection #1"

pin_collection_logo = pinata.pin_file_to_ipfs(collection_logo_filename)
ipfs_collection_logo_url = 'ipfs://ipfs/' + pin_collection_logo['IpfsHash']

collection_json = {"description": description_text,
                   "name": collection_name,
                   "properties": {},
                   "external_url": external_url,
                   "image": ipfs_collection_logo_url}

pin_collection_info = pinata.pin_json_to_ipfs(collection_json)
ipfs_collection_info_url = 'ipfs://ipfs/' + pin_collection_info['IpfsHash']

mint_collection_v2(
    collection_symbol,
    ipfs_collection_info_url,
    keypair,
    max_amount)
