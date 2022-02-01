import urllib
import json
from py_rmrk_tools_config import *
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from substrateinterface.utils.ss58 import ss58_decode, ss58_encode

substrate = SubstrateInterface(
    url=wss_url,
    ss58_format=ss58_format_id
)


def to_rmrk_price(ksm_price, version):
    return round(ksm_price * 10**12 * (1 - fee_dict[version] / 100))


def keypair_from_mnemonic(mnemonic_phrase):
    return Keypair.create_from_mnemonic(mnemonic_phrase)


def send_extrinsic(extrinsic):
    block_hash = ""
    try:
        receipt = substrate.submit_extrinsic(
            extrinsic, wait_for_inclusion=True)
        print(
            f"Extrinsic '{receipt.extrinsic_hash}' sent and included in block '{receipt.block_hash}'")
        block_hash = receipt.block_hash
    except SubstrateRequestException as e:
        print(f"Failed to send: {e}")
    return block_hash

def generate_list_calls(
        nfts_for_listing,
        ksm_price,
        version,
        batch_amount=list_batch_amount):
    rmrk_calls = []
    list_calls = []

    nfts_batch = []

    for nft_id in nfts_for_listing:
        rmrk_calls.append({
            'call_module': 'System',
            'call_function': 'remark',
            'call_args': {'remark': f'RMRK::LIST::{version}::{nft_id}::{to_rmrk_price(ksm_price, version)}'}
        })
        if len(rmrk_calls) >= batch_amount or nft_id == nfts_for_listing[-1]:
            list_calls.append(substrate.compose_call(
                call_module="Utility",
                call_function="batch",
                call_params={'calls': rmrk_calls}
            ))
            rmrk_calls = []
    return list_calls


def generate_send_calls(
        nfts_to_send_dict,
        version,
        batch_amount=send_batch_amount):
    rmrk_calls = []
    send_calls = []

    nfts_batch = []
    nft_ids = list(nfts_to_send_dict.keys())
    for nft_id in nft_ids:
        rmrk_calls.append({
            'call_module': 'System',
            'call_function': 'remark',
            'call_args': {'remark': f'RMRK::SEND::{version}::{nft_id}::{nfts_to_send_dict[nft_id]}'}
        })
        if len(rmrk_calls) >= batch_amount or nft_id == nft_ids[-1]:
            send_calls.append(substrate.compose_call(
                call_module="Utility",
                call_function="batch",
                call_params={'calls': rmrk_calls}
            ))
            rmrk_calls = []
    return send_calls


def generate_emote_calls(
        nfts_to_emote,
        emote_list,
        version,
        batch_amount=emote_batch_amount):
    rmrk_calls = []
    emote_calls = []

    nfts_batch = []
    for nft_id in nfts_to_emote:
        for emote in emote_list:
            rmrk_calls.append({
                'call_module': 'System',
                'call_function': 'remark',
                'call_args': {'remark': f'RMRK::EMOTE::{emote_version_dict[version]}::{nft_id}::{emote}'}
            })
            if len(rmrk_calls) >= batch_amount or (
                    nft_id == nfts_to_emote[-1] and emote == emote_list[-1]):
                emote_calls.append(substrate.compose_call(
                    call_module="Utility",
                    call_function="batch",
                    call_params={'calls': rmrk_calls}
                ))
                rmrk_calls = []
    return emote_calls


def generate_mint_calls(
        nfts_info_to_mint,
        version,
        recipient="",
        batch_amount=mint_batch_amount):
    rmrk_calls = []
    mint_calls = []
    nfts_in_block = []
    nfts_in_batch = []

    nfts_batch = []
    for nft_info_json in nfts_info_to_mint:
        rmrk_line = f"RMRK::{mintntf_operation_dict[version]}::{version}::{urllib.parse.quote(json.dumps(nft_info_json, separators=(',', ':')))}"
        if recipient:
            rmrk_line += f"::{recipient}"
        rmrk_calls.append({
            'call_module': 'System',
            'call_function': 'remark',
            'call_args': {'remark': rmrk_line}
        })
        
        nfts_in_block.append(f"{nft_info_json['collection']}-{nft_info_json['symbol']}-{nft_info_json['sn']}")
        if len(rmrk_calls) >= batch_amount or nft_info_json == nfts_info_to_mint[-1]:
            mint_calls.append(substrate.compose_call(
                call_module="Utility",
                call_function="batch",
                call_params={'calls': rmrk_calls}
            ))
            nfts_in_batch.append(nfts_in_block)
            rmrk_calls = []
            nfts_in_block = []
    return mint_calls, nfts_in_batch


def send_generated_calls(generated_calls, keypair):
    block_hashes = []
    for generated_call in generated_calls:
        extrinsic = substrate.create_signed_extrinsic(
            call=generated_call,
            keypair=keypair,
        )
        block_hashes.append(send_extrinsic(extrinsic))
    return block_hashes


def send_send_extrinsics(
        nfts_to_send_dict,
        version,
        keypair,
        batch_amount=send_batch_amount):
    generated_calls = generate_send_calls(
        nfts_to_send_dict, version, batch_amount)
    return send_generated_calls(generated_calls, keypair)

def send_emote_extrinsics(
        nfts_to_emote,
        emote_list,
        version,
        keypair,
        batch_amount=emote_batch_amount):
    generated_calls = generate_emote_calls(
        nfts_to_emote, emote_list, version, batch_amount)
    return send_generated_calls(generated_calls, keypair)


def send_list_extrinsics(
        nfts_for_listing,
        ksm_price,
        version,
        keypair,
        batch_amount=list_batch_amount):
    generated_calls = generate_list_calls(
        nfts_for_listing, ksm_price, version, batch_amount)
    return send_generated_calls(generated_calls, keypair)


def send_mint_extrinsics(
        nfts_info_to_mint,
        version,
        keypair,
        recipient="",
        batch_amount=mint_batch_amount):
    minted_nfts = []
    generated_calls, nfts_in_batch = generate_mint_calls(
        nfts_info_to_mint, version, recipient, batch_amount)
    for i in range(len(generated_calls)):
        generated_call = generated_calls[i]
        nfts_in_block = nfts_in_batch[i]
        try:
            extrinsic = substrate.create_signed_extrinsic(
                call=generated_call,
                keypair=keypair,
            )
            block_hash = send_extrinsic(extrinsic)
            block_number = substrate.get_block_number(block_hash)
            for nft_in_block in nfts_in_block:
                minted_nfts.append(f'{block_number}-{nft_in_block}')
        except Exception as e:
            print(f"Failed to mint: {e}")
            break
    return minted_nfts


def send_system_extrinsic(extrinsic_text, keypair):
    generated_call = substrate.compose_call(
        call_module='System',
        call_function='remark',
        call_params={'remark': extrinsic_text}
    )

    extrinsic = substrate.create_signed_extrinsic(
        call=generated_call,
        keypair=keypair,
    )
    return send_extrinsic(extrinsic)


def send_buy_extrinsic(
        nft_id,
        address,
        ksm_price,
        version,
        keypair,
        send_fee=False):
    rmrk_calls = [{
        'call_module': 'System',
        'call_function': 'remark',
        'call_args': {'remark': f'RMRK::BUY::{version}::{nft_id}'}
    },

        {
        'call_module': 'Balances',
        'call_function': 'transfer',
        'call_args': {
            'dest': address,
            'value': to_rmrk_price(ksm_price, version)
        }
    }
    ]
    if send_fee:
        rmrk_calls.append({'call_module': 'Balances',
                           'call_function': 'transfer',
                           'call_args': {'dest': rmrk_wallet_address,
                                          'value': round(to_rmrk_price(ksm_price,
                                                                       version) * (fee_dict[version] / 100))}})

    extrinsic = substrate.create_signed_extrinsic(
        call=substrate.compose_call(
            call_module="Utility",
            call_function="batch_all",
            call_params={'calls': rmrk_calls}
        ),
        keypair=keypair,
    )
    return send_extrinsic(extrinsic)


def generate_collection_id(keypair, collection_symbol):
    pub_key = keypair.public_key.hex()
    return pub_key[:10] + pub_key[-8:] + '-' + collection_symbol.upper()

# {
#   "name": "Dot Leap Early Promoters",
#   "max": 100,
#   "issuer": "CpjsLDC1JFyrhm3ftC9Gs4QoyrkHKhZKtK7YqGTRFtTafgp",
#   "symbol": "DLEP",
#   "id": "0aff6865bed3a66b-DLEP",
#   "metadata": "ipfs://ipfs/QmVgs8P4awhZpFXhkkgnCwBp4AdKRj3F9K58mCZ6fxvn3j"
# }

def mint_collection_v1(
        name,
        symbol,
        metadata,
        keypair,
        max_amount=0):
    mint_json = {
        "name": name,
        "max": max_amount,
        "issuer": str(ss58_encode(keypair.public_key, 2)),
        "symbol": symbol.upper(),
        "id": generate_collection_id(keypair, symbol),
        "metadata": metadata
    }
    extrinsic_text = f"RMRK::MINT::1.0.0::{urllib.parse.quote(json.dumps(mint_json, separators=(',', ':')))}"
    return send_system_extrinsic(extrinsic_text, keypair)


# {
#   "max": 100,
#   "issuer": "CpjsLDC1JFyrhm3ftC9Gs4QoyrkHKhZKtK7YqGTRFtTafgp",
#   "symbol": "DLEP",
#   "id": "0aff6865bed3a66b-DLEP",
#   "metadata": "ipfs://ipfs/QmVgs8P4awhZpFXhkkgnCwBp4AdKRj3F9K58mCZ6fxvn3j"
# }

def mint_collection_v2(
        symbol,
        metadata,
        keypair,
        max_amount=0):
    mint_json = {
        "max": max_amount,
        "issuer": str(ss58_encode(keypair.public_key, 2)),
        "symbol": symbol.upper(),
        "id": generate_collection_id(keypair, symbol),
        "metadata": metadata
    }
    extrinsic_text = f"RMRK::CREATE::2.0.0::{urllib.parse.quote(json.dumps(mint_json, separators=(',', ':')))}"
    return send_system_extrinsic(extrinsic_text, keypair)
