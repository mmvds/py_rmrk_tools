import sys
sys.path.append('../')
from rmrk_tools.rmrk_tools import *

keypair = keypair_from_mnemonic(wallet_mnemonic)

my_nfts = [
    '10807817-b2379dab465991a730-VICTOR R-TEST_NFT5_AI_GENERATED-0000000000000008',
    '10807796-b2379dab465991a730-VICTOR R-TEST_NFT4_AI_GENERATED-0000000000000007']

# list my nfts for 1.5 ksm
send_list_extrinsics(my_nfts, 1.5, '1.0.0', keypair)
