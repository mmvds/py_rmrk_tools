# py_rmrk_tools
python rmrk tools

You have to set your mnemonic phrase in py_rmrk_tools_config.py
```python
wallet_mnemonic = '<wallet seed phrase>'
```
and Pinata API keys
```python
pinata_api_key = "pinata_api_key"
pinata_secret_api_key = "pinata_secret_api_key"
```

or Nft.storage API keys
```python
nft_storage_api_url = "https://api.nft.storage/upload"
nft_storage_api_key = "your_nft_storage_api_key"
```

Production nodes:
wss://kusama-rpc.polkadot.io/

# Examples
https://github.com/mmvds/py_rmrk_tools/tree/main/examples

## Pin to ipfs via nft.storage
```python
pin_nft_file(nft_image_path)
pin_nft_json(nft_json)
```

## List nfts
```python
keypair = keypair_from_mnemonic(wallet_mnemonic)

my_nfts = [
    '10807817-b2379dab465991a730-VICTOR R-TEST_NFT5_AI_GENERATED-0000000000000008',
    '10807796-b2379dab465991a730-VICTOR R-TEST_NFT4_AI_GENERATED-0000000000000007']

# list my nfts for 1.5 ksm
send_list_extrinsics(my_nfts, 1.5, '1.0.0', keypair)
```
## Send nfts
```python  
keypair = keypair_from_mnemonic(wallet_mnemonic)

nfts_to_send_dict = {
    '10807753-b2379dab465991a730-VICTOR R-TEST_NFT1_AI_GENERATED-0000000000000004': 'GbzZaxQG7d2M7ykb8CoofDvfn1t8iqzDHjvXPxnkiCTRmfJ',
    '10858569-b2379dab465991a730-VICTOR R-TEST_NFT7_AI_GENERATED-0000000000000010': 'GbzZaxQG7d2M7ykb8CoofDvfn1t8iqzDHjvXPxnkiCTRmfJ',
}

# send nfts according to a dict
send_send_extrinsics(nfts_to_send_dict, '1.0.0', keypair)
```
## Emote nfts
```python 
keypair = keypair_from_mnemonic(wallet_mnemonic)
emote_nfts = ['10807817-b2379dab465991a730-VICTOR R-TEST_NFT5_AI_GENERATED-0000000000000008', '10807796-b2379dab465991a730-VICTOR R-TEST_NFT4_AI_GENERATED-0000000000000007']
my_emotes = ['1F638','1F44D'] 

# send 😸 and 👍 for emote_nfts list
send_emote_extrinsics(emote_nfts, my_emotes, '1.0.0', keypair)
```
## Buy nft
```python
keypair = keypair_from_mnemonic(wallet_mnemonic)

# buy 10807786-b2379dab465991a730-VICTOR R-TEST_NFT3_AI_GENERATED-0000000000000006 nft 
# for 0.01 KSM 
# from GbzZaxQG7d2M7ykb8CoofDvfn1t8iqzDHjvXPxnkiCTRmfJ
# without market fee ;)

send_buy_extrinsic('10807786-b2379dab465991a730-VICTOR R-TEST_NFT3_AI_GENERATED-0000000000000006', 'GbzZaxQG7d2M7ykb8CoofDvfn1t8iqzDHjvXPxnkiCTRmfJ', 0.01, '1.0.0', keypair, False)
```
## Mint collection
v1 https://github.com/mmvds/py_rmrk_tools/blob/main/examples/mint_collection_v1.py

v2 https://github.com/mmvds/py_rmrk_tools/blob/main/examples/mint_collection_v2.py

## Mass mint nfts
v1 https://github.com/mmvds/py_rmrk_tools/blob/main/examples/mint_nfts_v1.py

v2 https://github.com/mmvds/py_rmrk_tools/blob/main/examples/mint_nfts_v2.py

## v2 Mint base example
https://github.com/mmvds/py_rmrk_tools/blob/main/examples/mint_base.py

## v2 res add example
```python
nfts_to_resadd_dict = {}
for nft_id in minted_nfts:
    slot_id = '_'.join(nft_id.split('-')[3].split('_')[1:3])
    nfts_to_resadd_dict[nft_id] = {
                                    "id":"TEST_COLLECTION_" + generate(size=8),
                                    "src":"ipfs://ipfs/" + img_slots_dict[slot_id],
                                    "thumb":"ipfs://ipfs/" + '<thumb_ipfs>',
                                    "slot": f"{base_id}.TEST_COLLECTION_SLOT_{slot_id}",
                                    "metadata": 'ipfs://ipfs/' + descriptions_dict[slot_id],
                                    }
send_resadd_extrinsics(nfts_to_resadd_dict, '2.0.0', keypair)
```
