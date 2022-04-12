# -*- coding: utf-8 -*-
"""
椭圆加密获取公、私钥，私钥签名、公钥验签
"""

import hashlib
from eth_account import Account
from eth_utils.hexadecimal import encode_hex
from eth_account.messages import encode_defunct


class passWord():
    def __init__(self):
        pass

    def get_key(self, key):
        """
        获取公钥私钥
        :return: 返回公钥、私钥
        """
        ac1 = Account.create(key)
        return {"prvkey": encode_hex(ac1.key), "address": ac1.address}

    def message_sign(self, text, prv_key):
        """
        基于私钥获取签名
        :param text: 待签名的文本
        :param prv_key: 私钥
        :return: 签名
        """
        try:
            message = encode_defunct(text=text)
            result = Account.sign_message(message, prv_key)
            result = str(result)
            result = result[result.find("'signature':"):result.find(')})')]
            return {"sign": result[result.find("('") + 2:].replace("'", '')}
        except:
            return {"error": '私钥格式不对'}

    def message_hash(self, text):
        s = hashlib.sha256()
        s.update(text.encode("utf8"))
        return {"hash":str(s.hexdigest())}

    def verifity(self, text, signature, address):
            """
            验证签名
            :param text: 原文本
            :param signature: 签名
            :param address: 公钥
            :return: 验证结果
            """
            try:
                message = encode_defunct(text=text)
                address_new = Account.recover_message(message, signature=signature)
                if address == address_new:
                    return {"status": '验证一致'}
                else:
                    return {"status": '验证失败'}
            except:
                return {"status": '格式错误'}

    def recover_address(self, prv_key):
        """
        基于私钥推出地址
        :param prv_key: 私钥
        :return: 地址
        """
        try:
            acct = Account.from_key(prv_key)
            return {"address": acct.address}
        except:
            return {"error": '格式错误'}

    def recover_transaction(self, transaction):
        """
        基于交易哈希推出地址
        :param prv_key: 交易哈希
        :return: 地址
        """
        try:
            acct = Account.recover_transaction(transaction)
            return {"address": acct}
        except:
            return {"error": '格式错误'}

    def sign_transaction(self, transaction, key):
        """
         transaction = {
            # Note that the address must be in checksum format or native bytes:
            'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
            'value': 1000000000,
            'gas': 2000000,
            'gasPrice': 234567897654321,
            'nonce': 0,
            'chainId': 1
        }
        {'hash': HexBytes('0x6893a6ee8df79b0f5d64a180cd1ef35d030f3e296a5361cf04d02ce720d32ec5'),
             'r': 4487286261793418179817841024889747115779324305375823110249149479905075174044,
             'rawTransaction': HexBytes('0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428'),  # noqa: E501
             's': 30785525769477805655994251009256770582792548537338581640010273753578382951464,
             'v': 37}
        基于公钥签名交易
        :param transaction: 交易dict
        :param key: 公钥
        :return: 签名结果
        """
        return {"sign":Account.sign_transaction(transaction, key)}
# print(get_key(123))
# # ('0x24b7d7d1727b7aebb518f76721f1f51e61ad10e355fa699c8bd62d0067a35f90', '0x4C967cf4321f14860F7f7c824855082B9FEd4982')
# print(message_sign("wdfewdw",'0x24b7d7d1727b7aebb518f76721f1f51e61ad10e355fa699c8bd62d0067a35f90'))
# print(verifity("wdfeewdw","0x9f6eb891fdbcdbc899e2973a55a6e2807526f8b33ba2fd86f6abe9b7420e39442538954c7dc93c9912a5c2258d270cb0015b7aaad82a28574c699b556fdf0c081c","0x4C967cf4321f14860F7f7c824855082B9FEd4982"))
# print(recover_address("0x24b7d7d1727b7aebb518f76721f1f51e61ad10e355fa699c8bd62d0067a35f90"))
# transaction = {
#     # Note that the address must be in checksum format or native bytes:
#     'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
#     'value': 1000000000,
#     'gas': 2000000,
#     'gasPrice': 234567897654321,
#     'nonce': 0,
#     'chainId': 1
# }
# print(recover_transaction(transaction))
