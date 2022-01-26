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
    try:
        receipt = substrate.submit_extrinsic(
            extrinsic, wait_for_inclusion=True)
        print(
            f"Extrinsic '{receipt.extrinsic_hash}' sent and included in block '{receipt.block_hash}'")

    except SubstrateRequestException as e:
        print(f"Failed to send: {e}")


def generate_list_calls(
        nfts_for_listing,
        ksm_price,
        version,
        batch_amount=100):
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


def generate_send_calls(nfts_to_send_dict, version, batch_amount=100):
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


def generate_emote_calls(nfts_to_emote, emote_list, version, batch_amount=100):
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


def send_generated_calls(generated_calls, keypair):
    for generated_call in generated_calls:
        extrinsic = substrate.create_signed_extrinsic(
            call=generated_call,
            keypair=keypair,
        )
        send_extrinsic(extrinsic)


def send_send_extrinsics(nfts_to_send_dict, version, keypair):
    generated_calls = generate_send_calls(
        nfts_to_send_dict, version, send_batch_amount)
    send_generated_calls(generated_calls, keypair)


def send_emote_extrinsics(nfts_to_emote, emote_list, version, keypair):
    generated_calls = generate_emote_calls(
        nfts_to_emote, emote_list, version, emote_batch_amount)
    send_generated_calls(generated_calls, keypair)


def send_list_extrinsics(nfts_for_listing, ksm_price, version, keypair):
    generated_calls = generate_list_calls(
        nfts_for_listing, ksm_price, version, list_batch_amount)
    send_generated_calls(generated_calls, keypair)


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
    send_extrinsic(extrinsic)


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
    send_extrinsic(extrinsic)


def generate_collection_id(keypair, collection_symbol):
    pub_key = keypair.public_key.hex()
    return pub_key[:10] + pub_key[-8:] + '-' + collection_symbol.upper()


def mint_collection(name, symbol, metadata, version, keypair, max_amount=0):
    mint_json = {
        "name": name,
        "max": max_amount,
        "issuer": str(ss58_encode(keypair.public_key, 2)),
        "symbol": symbol.upper(),
        "id": generate_collection_id(keypair, symbol),
        "metadata": metadata
    }
    extrinsic_text = f"RMRK::MINT::{version}::{urllib.parse.quote_plus(json.dumps(mint_json, separators=(',', ':')))}"
    send_system_extrinsic(extrinsic_text, keypair)
