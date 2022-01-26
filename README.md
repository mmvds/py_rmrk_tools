# py_rmrk_tools
python rmrk tools

You have to set your mnemonic phrase in py_rmrk_tools_config.py
```python
wallet_mnemonic = '<wallet seed phrase>'
```
# Examples
https://github.com/mmvds/py_rmrk_tools/tree/main/examples

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
