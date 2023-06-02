import sys
sys.path.append('../')
from py_rmrk_tools import *
from py_rmrk_tools_config import *

keypair = keypair_from_mnemonic(wallet_mnemonic)
img_type = "png"
symbol = "TEST_COLLECT"
version = "2.0.0"
parts = [
{"id":"TEST_COLLECT_BG1","type":"fixed","z":1,"src":"ipfs://ipfs/<background_ipfs>"},
{"id":"TEST_COLLECT_SLOT_1_01","type":"slot","equippable":["069c0e45bf74dbc77b-TEST_COLLECT_AVATAR"],"z":101},
{"id":"TEST_COLLECT_SLOT_1_02","type":"slot","equippable":["069c0e45bf74dbc77b-TEST_COLLECT_AVATAR"],"z":102},
{"id":"TEST_COLLECT_SLOT_1_03","type":"slot","equippable":["069c0e45bf74dbc77b-TEST_COLLECT_AVATAR"],"z":103},
{"id":"TEST_COLLECT_SLOT_1_04","type":"slot","equippable":["069c0e45bf74dbc77b-TEST_COLLECT_AVATAR"],"z":104},
{"id":"TEST_COLLECT_SLOT_1_05","type":"slot","equippable":["069c0e45bf74dbc77b-TEST_COLLECT_AVATAR"],"z":105},
{"id":"TEST_COLLECT_SLOT_1_06","type":"slot","equippable":["069c0e45bf74dbc77b-TEST_COLLECT_AVATAR"],"z":106},
{"id":"TEST_COLLECT_SLOT_1_07","type":"slot","equippable":["069c0e45bf74dbc77b-TEST_COLLECT_AVATAR"],"z":107},
]

print(mint_base(symbol, img_type, parts, version, keypair))
