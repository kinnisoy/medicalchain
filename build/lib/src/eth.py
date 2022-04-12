"""
区块链浏览器加料版，除了查询还能交互，账户创建，数据上下链，无所不能。
@bob.lee
"""
from web3 import Web3, HTTPProvider
import requests
import json


def data_handle(data, max_len):
    len_data = len(data)
    if len_data > max_len:
        return {'error': 'string too long'}
    else:
        out_bytes = data.ljust(max_len, '0')
        out_bytes = bytes(out_bytes, 'utf-8')
        return {'data': out_bytes}


def post_method(url, method, params):
    """
    web3与geth交互,根据不同的方法，填不同的参数
    :param url:geth开启的url
    :param method:方法
    :param params:参数
    :return:返回值
    """
    session = requests.Session()
    payload = {"jsonrpc": "2.0",
               "method": method,
               "params": params,
               "id": 1}
    headers = {'Content-type': 'application/json'}
    response = session.post(url, json=payload, headers=headers)
    return response.json()


class Eth():
    """
    主api，参考https://web3py.readthedocs.io/en/stable/contracts.html#contract-factories
    封装参考:https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getbalance
    """

    def __init__(self, url):
        self.url = url

    def get_account(self):
        """
        获取账户，对应eth.accounts
        :return: 账户列表
        """
        w3 = Web3(HTTPProvider(self.url))
        return {"account": w3.eth.accounts}

    def get_block_number(self):
        """
        获取区块高度，对应eth.blockNumber
        :return:区块高度
        """
        w3 = Web3(HTTPProvider(self.url))
        return {"block_number": w3.eth.blockNumber}

    def create_account(self, password):
        """
        自定义创建新账户，对应personal.newAccount
        :param password:自定义密码
        :return:创建状态
        """
        result = post_method(self.url, 'personal_newAccount', [password])
        if 'result' in result:
            return {'status': 'success', 'result': result['result']}
        else:
            return {'status': 'fail'}

    def unlock_account(self, address, password):
        """
        根据密码，解锁账户，对应personal.unlockAccount
        :param address:地址
        :param password:密码
        :return:解锁状态
        """
        result = post_method(self.url, 'personal_unlockAccount', [address, password])
        if 'result' in result:
            return {'status': 'success'}
        else:
            return {'status': 'fail'}

    def create_key(self, password):
        """
        基于密码创建地址、私钥
        :param password: 密码
        :return: 地址及私钥
        """
        w3 = Web3()
        account = w3.eth.account.create(password)
        address = account.address
        private_key = account.privateKey.hex()
        return {"address": address, "private_key": private_key}

    def get_balance(self, address, type):
        """
        返回给定地址的帐户余额
        :param address:地址
        :param type: 三种类型"latest", "earliest" ,"pending"
        :return: 状态及余额
        """
        result = post_method(self.url, 'eth_getBalance', [address, type])
        if 'result' in result:
            return {'status': 'success', 'result': result['result']}
        else:
            return {'status': 'fail'}

    def get_traction_detail(self, address):
        """
        获取合约上链、转账后的具体信息
        :param address: 合约地址
        :return: 具体信息
        """
        result = post_method(self.url, 'eth_getTransactionByHash', [address])
        if 'result' in result:
            return {'status': 'success', 'result': result['result']}
        else:
            return {'status': 'fail'}

    def get_block_detail(self, block_hash):
        """
        获取区块的具体信息
        :param block_hash: 区块哈希
        :return: 区块具体内容
        """
        result = post_method(self.url, 'eth_getBlockByHash', [block_hash, True])
        if 'result' in result:
            return {'status': 'success', 'result': result['result']}
        else:
            return {'status': 'fail'}

    def wock_account(self):
        """
        获取当前的挖矿账户
        :return: 账户表
        """
        result = post_method(self.url, 'eth_coinbase', [])
        if 'result' in result:
            return {'status': 'success', 'result': result['result']}
        else:
            return {'status': 'fail'}

    def contract_data_upload(self, abi_location, byte_location, address, password):
        """
        上传智能合约记住先挖矿
        :param abi_location: 智能合约abi.json文件路径
        :param byte_location:  智能合约bin.json文件路径
        :param address: 节点账户地址
        :param password: 节点密码
        :return:合约地址
        """
        try:
            w3 = Web3(HTTPProvider(self.url))
            with open(abi_location, 'r') as abi_definition:
                abi = abi_definition.read()
            abi = abi.replace('\'', '\"')
            abi = json.loads(abi)
            with open(byte_location, 'r') as bytecode_definition:
                bytecode = json.load(bytecode_definition)["object"]
            all_account = w3.eth.accounts
            all_account_ = [str(i).upper() for i in all_account]
            if str(address).upper() in all_account_:
                w3.eth.defaultAccount = w3.eth.accounts[all_account_.index(str(address).upper())]
                result = post_method(self.url, 'personal_unlockAccount', [address, password])
                if 'result' in result:
                    Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)
                    tx_hash = Greeter.constructor().transact()
                    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                    return {'tx_hash': str(tx_receipt.contractAddress)}
                else:
                    return {"error": "unlock account fail"}
            else:
                return {'error': 'address not in ETH'}
        except Exception as e:
            return {'error': str(e)}

    def use_contract_upload(self, abi_location, contract_address, address, password, data_input):
        """
        基于https://web3py.readthedocs.io/en/stable/contracts.html提供的智能合约来测试
        :param abi_location: 智能合约abi.json文件路径
        :param contract_address:智能合约地址
        :param address:账户
        :param password:密码
        :param data_input:用户提交的字符串
        :return:结果（成功返回交易地址，及结果）
        """
        w3 = Web3(HTTPProvider(self.url))
        with open(abi_location, 'r') as abi_definition:
            abi = abi_definition.read()
        abi = abi.replace('\'', '\"')
        abi = json.loads(abi)
        all_account = w3.eth.accounts
        all_account_ = [str(i).upper() for i in all_account]
        if str(address).upper() in all_account_:
            w3.eth.defaultAccount = w3.eth.accounts[all_account_.index(str(address).upper())]
            result = post_method(self.url, 'personal_unlockAccount', [address, password])
            if 'result' in result:
                contract = w3.eth.contract(
                    address=contract_address,
                    abi=abi)
                # # update the greeting
                tx_hash = contract.functions.upload(data_input['id'], data_input['name'],
                                                    data_input['file_hash']).transact()
                w3.eth.waitForTransactionReceipt(tx_hash)
                contract_result = contract.functions.upload(data_input['id'], data_input['name'],
                                                            data_input['file_hash']).call()
                return {'load_tx_hash': tx_hash, 'contract_result': contract_result}

            else:
                return {"error": "unlock account fail"}
        else:
            return {'error': 'address not in ETH'}

    def use_contract_download(self, abi_location, contract_address, address, password, data_input):
        """
        基于https://web3py.readthedocs.io/en/stable/contracts.html提供的智能合约来测试
        :param abi_location: 智能合约abi.json文件路径
        :param contract_address:智能合约地址
        :param address:账户
        :param password:密码
        :param data_input:用户提交的字符串
        :return:结果（成功返回交易地址，及结果）
        """
        w3 = Web3(HTTPProvider(self.url))
        with open(abi_location, 'r') as abi_definition:
            abi = abi_definition.read()
        abi = abi.replace('\'', '\"')
        abi = json.loads(abi)
        all_account = w3.eth.accounts
        all_account_ = [str(i).upper() for i in all_account]
        if str(address).upper() in all_account_:
            w3.eth.defaultAccount = w3.eth.accounts[all_account_.index(str(address).upper())]
            result = post_method(self.url, 'personal_unlockAccount', [address, password])
            if 'result' in result:
                contract = w3.eth.contract(
                    address=contract_address,
                    abi=abi)
                tx_hash = contract.functions.download(data_input).transact()
                w3.eth.waitForTransactionReceipt(tx_hash)
                contract_result = contract.functions.download(data_input).call()
                return {'download_tx_hash': tx_hash, 'contract_result': contract_result}
            else:
                return {"error": "unlock account fail"}
        else:
            return {'error': 'address not in ETH'}