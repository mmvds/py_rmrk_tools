import psycopg2
import sys
sys.path.append('../')
from py_rmrk_tools_config import *
from py_rmrk_tools import *

keypair = keypair_from_mnemonic(wallet_mnemonic)

conn = psycopg2.connect(dbname=pg_db, user=pg_login,
                        password=pg_pass, host=pg_host)
conn.set_client_encoding('UTF8')
db = conn.cursor()

#send emotes for all nfts from collection '%6ec662611f161fd10a-DDWORLD%'
db.execute(f"SELECT id FROM nfts_vlite WHERE id like '%6ec662611f161fd10a-DDWORLD%';")
emote_nfts = [x[0] for x in db.fetchall()] 
# or just for a list:
# emote_nfts = ['10807817-b2379dab465991a730-VICTOR R-TEST_NFT5_AI_GENERATED-0000000000000008', '10807796-b2379dab465991a730-VICTOR R-TEST_NFT4_AI_GENERATED-0000000000000007']

my_emotes = ['1F638','1F44D'] 

# send 😸 and 👍 for emote_nfts list
send_emote_extrinsics(emote_nfts, my_emotes, '1.0.0', keypair)
conn.close()

