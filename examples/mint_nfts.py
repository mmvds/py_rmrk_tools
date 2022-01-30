import sys
sys.path.append('../')
import time
import pinatapy
from py_rmrk_tools_config import *
from py_rmrk_tools import *
from pinatapy import PinataPy
import re


keypair = keypair_from_mnemonic(wallet_mnemonic)
pinata = PinataPy(pinata_api_key, pinata_secret_api_key)

nfts_info_dict = {}

# generate nfts info list
collection_id = "c4ef7d5f96b88a6675-TST4"
for i in range(1, 11):
    nft_description = f"Bla-bla-bla {i}"
    nft_name = f"Best Test Nft {i}"
    nft_instance = re.sub(
        '[^A-Za-z0-9]+',
        '_',
        nft_name).replace(
        '__',
        '_').upper()[
            :20]
    nft_image_path = f"./pics/test_pic{i}.jpg"
    nft_sn = str(i).zfill(16)

    nfts_info_dict[i] = {
        "collection": collection_id,
        "description": nft_description,
        "name": nft_name,
        "instance": nft_instance,
        "attributes": [],
        "image_path": nft_image_path,
        "transferable": 1,
        "sn": nft_sn}

# pin images
for i in nfts_info_dict:
    not_pinned = True
    pin_attempt = 0
    img_path = nfts_info_dict[i]['image_path']

    while not_pinned and pin_attempt < 3:
        pin_attempt += 1
        try:
            print(f"Pinnig image {img_path}. Attempt {pin_attempt}")
            pin_image = pinata.pin_file_to_ipfs(img_path)
            not_pinned = False
            nfts_info_dict[i]['image_ipfs'] = 'ipfs://ipfs/' + \
                pin_image['IpfsHash']
        except Exception as e:
            time.sleep(pin_attempt * 3)

    if pin_attempt == 3:
        print(f"Image {img_path} wasn't pinned:\n{str(e)}")
        exit()
    time.sleep(0.5)

# pin nft metadata
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
            print(f"Pinnig metadata for nft {i}. Attempt {pin_attempt}")
            pin_nft_metadata = pinata.pin_json_to_ipfs(nft_metadata_json)
            not_pinned = False
            nft['metadata'] = 'ipfs://ipfs/' + pin_nft_metadata['IpfsHash']
        except Exception as e:
            time.sleep(pin_attempt * 3)

    if pin_attempt == 3:
        print(f"Metadata for nft {i} wasn't pinned:\n{str(e)}")
        exit()
    time.sleep(0.5)

# prepare nfts list
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
minted_nfts = send_mint_extrinsics(nfts_info_to_mint, '1.0.0', keypair)
print(minted_nfts)
with open('mint_log.txt', 'w') as f:
    for minted_nft in minted_nfts:
        f.write(f"{minted_nft}\n")
