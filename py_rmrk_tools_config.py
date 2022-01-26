# substrate config
# wss_url = "wss://kusama-rpc.polkadot.io/"
wss_url = "wss://node.rmrk.app/"
ss58_format_id = 2

# your wallet
wallet_mnemonic = '<wallet seed phrase>'

# batch amounts limits per 1 block
send_batch_amount = 100
list_batch_amount = 100
emote_batch_amount = 100

# kanaria and singular marketplace fee
kanaria_fee = 5
singular_fee = 2
fee_dict = {'1.0.0': singular_fee, '2.0.0': kanaria_fee}

# emote nft extrinsics versions
emote_version_dict = {'1.0.0': '1.0.0', '2.0.0': '2.0.0::RMRK2'}

# postgres db (if you use rmrk2psql)
pg_login = "postgres"
pg_pass = "postpass"
pg_db = "rmrk"
pg_host = "localhost"
