import sys
sys.path.append('../')
from rmrk_tools.rmrk_tools import *

keypair = keypair_from_mnemonic(wallet_mnemonic)

nfts_to_send_dict = {
    '10807753-b2379dab465991a730-VICTOR R-TEST_NFT1_AI_GENERATED-0000000000000004': 'GbzZaxQG7d2M7ykb8CoofDvfn1t8iqzDHjvXPxnkiCTRmfJ',
    '10858569-b2379dab465991a730-VICTOR R-TEST_NFT7_AI_GENERATED-0000000000000010': 'GbzZaxQG7d2M7ykb8CoofDvfn1t8iqzDHjvXPxnkiCTRmfJ',
}

# send nfts according to a list
send_send_extrinsics(nfts_to_send_dict, '1.0.0', keypair)
