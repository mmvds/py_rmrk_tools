from rmrk_tools.pinata import Pinata_API
from rmrk_tools.rmrk_tools import *
from rmrk_tools.rmrk_tools_config import *
from rmrk_tools.utils import Files
from pathlib import Path
import re, time

keypair = keypair_from_mnemonic(wallet_mnemonic)
pinata = Pinata_API(pinata_api_key, pinata_secret_api_key)

# configurable parameters
local_collection_path = '../Collections/DigitalBugz/'
logo = f"{local_collection_path}/logo.png"
external_url = "https://singular.rmrk.app"
create_collection = False
collection_id = "beb8138cfe2250a03a-DBZ"  # Specify 'collection_id' if 'create_collection' is False
collection_name = "DigitalBugz"
collection_symbol = "DBZ"
max_assets = 50
description_text = "Bugz - Test Collection"

media = Files().get_local_media(filepath=local_collection_path)

if create_collection:
    pin_collection_logo = pinata.pin_file_to_ipfs(logo)
    ipfs_collection_logo_url = 'ipfs://ipfs/' + pin_collection_logo['IpfsHash']

    collection_json = {"description": description_text,
                       "name": collection_name,
                       "attributes": [],
                       "external_url": external_url,
                       "image": ipfs_collection_logo_url}

    pin_collection_info = pinata.pin_json_to_ipfs(collection_json)
    ipfs_collection_info_url = 'ipfs://ipfs/' + pin_collection_info['IpfsHash']

    collection = mint_collection(collection_name, collection_symbol, ipfs_collection_info_url, '1.0.0', keypair, max_assets)
    if 'id' not in collection:
        collection_id = collection['id']
        print(f"Something happened whilst minting... {collection}")
        exit()

nfts_info_dict = {}

# Generate NFT(s) info list from local media
for index, filepath in enumerate(media, start=1):
    nft_description = f"Collection item {index}/{len(media)}"
    nft_name = Path(filepath).with_suffix('').stem  # name of file without the type extension
    nft_instance = re.sub(
        '[^A-Za-z0-9]+',
        '_',
        nft_name).replace(
        '__',
        '_').upper()[
                   :20]
    nft_image_path = filepath
    nft_sn = str(index).zfill(16)

    nfts_info_dict[index] = {
        "collection": collection_id,
        "description": nft_description,
        "name": nft_name,
        "instance": nft_instance,
        "attributes": [],
        "image_path": nft_image_path,
        "transferable": 1,
        "sn": nft_sn}

# Pin images using Pinata
for i in nfts_info_dict:
    not_pinned = True
    pin_attempt = 0
    img_path = nfts_info_dict[i]['image_path']

    while not_pinned and pin_attempt < 3:
        pin_attempt += 1
        try:
            print(f"Pinning image {img_path}... Attempt: {pin_attempt}")
            pin_image = pinata.pin_file_to_ipfs(img_path)
            not_pinned = False
            nfts_info_dict[i]['image_ipfs'] = 'ipfs://ipfs/' + pin_image['IpfsHash']
        except Exception as e:
            time.sleep(pin_attempt * 3)

    if pin_attempt == 3:
        print(f"Image {img_path} wasn't pinned:\n{str(e)}")
        exit()
    time.sleep(0.5)

# Pin NFT(s) metadata
for i in nfts_info_dict:
    nft = nfts_info_dict[i]
    not_pinned = True
    pin_attempt = 0
    nft_metadata_json = {
        "description": nft['description'],
        "name": nft['name'],
        "attributes": nft['attributes'],
        "image": nft['image_ipfs']}

    while not_pinned and pin_attempt < 3:
        pin_attempt += 1
        try:
            print(f"Pinning metadata for nft {i}... Attempt: {pin_attempt}")
            pin_nft_metadata = pinata.pin_json_to_ipfs(nft_metadata_json)
            not_pinned = False
            nft['metadata'] = 'ipfs://ipfs/' + pin_nft_metadata['IpfsHash']
        except Exception as e:
            time.sleep(pin_attempt * 3)

    if pin_attempt == 3:
        print(f"Metadata for nft {i} wasn't pinned:\n{str(e)}")
        exit()
    time.sleep(0.5)

# Prepare NFT(s) for minting
nfts_info_to_mint = []
for i in sorted(nfts_info_dict):
    nft = nfts_info_dict[i]
    nft_info = {
        "collection": nft['collection'],
        "instance": nft['instance'],
        "name": nft['name'],
        "transferable": nft['transferable'],
        "sn": nft['sn'],
        "metadata": nft['metadata']
    }
    nfts_info_to_mint.append(nft_info)

# mint them all
send_mint_extrinsics(nfts_info_to_mint, '1.0.0', keypair)