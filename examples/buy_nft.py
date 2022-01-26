import sys
sys.path.append('../')
from py_rmrk_tools_config import *
from py_rmrk_tools import *

keypair = keypair_from_mnemonic(wallet_mnemonic)

# buy 10807786-b2379dab465991a730-VICTOR R-TEST_NFT3_AI_GENERATED-0000000000000006 nft 
# for 0.01 KSM 
# from GbzZaxQG7d2M7ykb8CoofDvfn1t8iqzDHjvXPxnkiCTRmfJ
# without market fee ;)

send_buy_extrinsic('10807786-b2379dab465991a730-VICTOR R-TEST_NFT3_AI_GENERATED-0000000000000006', 'GbzZaxQG7d2M7ykb8CoofDvfn1t8iqzDHjvXPxnkiCTRmfJ', 0.01, '1.0.0', keypair, False)
