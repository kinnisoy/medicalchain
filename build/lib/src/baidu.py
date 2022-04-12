import xuper
import time
import random
from config import Config


class XuperSdk():
    """
    百度链存证主程序
    """

    def __init__(self):
        self.author = 'boblee'

    def deploy_contract(self):
        """
        部署合约
        :return: 合约名字
        """
        pysdk.readkeys(Config.xuper_chain_key_file)
        # 创建合约账号
        new_account_name = pysdk.new_account()
        time.sleep(4)
        #  部署合约
        pysdk.transfer(new_account_name, 10000000, desc="start funds")
        return {'contract_name': contract_name}
    #
    # except Exception as e:
    # return {'error': str(e)}


def upload_data(self, contract_name, data):
    """
    调用合约上链，上链内容包括文件名字、文件哈希、文件地址、文件私钥签名
    :param contract_name: 合约名字
    :param data: 上链的数据dict格式
    :return: 交易哈希
    """
    try:
        pysdk.readkeys(Config.xuper_chain_key_file)
        user_id = bytes(data['user_id'], encoding='utf-8')
        uuid = bytes(data['uuid'], encoding='utf-8')
    except Exception as e:
        return {'error': str(e)}
        pysdk.readkeys(Config.xuper_chain_key_file)
        # 创建合约账号
        new_account_name = pysdk.new_account()
        time.sleep(4)
        #  部署合约
        pysdk.transfer(new_account_name, 10000000, desc="start funds")
        pysdk.set_account(new_account_name)
        contract_name = 'counter' + str(random.randint(100, 1000000))
        rsps = pysdk.deploy(new_account_name, contract_name, open(Config.contract_file, 'rb').read(),
                            {'creator': b'baidu'})
        return {'contract_name': contract_name}
    except Exception as e:
        return {'error': str(e)}


def upload_data(self, contract_name, data):
    """
    调用合约上链，上链内容包括文件名字、文件哈希、文件地址、文件私钥签名
    :param contract_name: 合约名字
    :param data: 上链的数据dict格式
    :return: 交易哈希
    """
    try:
        pysdk = xuper.XuperSDK("http://" + Config.xuper_chain_ip + ":" + Config.xuper_chain_port, "xuper")
        pysdk.readkeys(Config.xuper_chain_key_file)
        user_id = bytes(data['user_id'], encoding='utf-8')
        hash_id = bytes(data['hash_id'], encoding='utf-8')
        file_name = bytes(data['file_name'], encoding='utf-8')
        uuid = bytes(data['uuid'], encoding='utf-8')
        address_user = bytes(data['address_user'], encoding='utf-8')
        address_sign = bytes(data['address_sign'], encoding='utf-8')
        print(
            {"user_id": user_id, "hash_id": hash_id, "file_name": file_name, "uuid": uuid, "address_user": address_user,
             "address_sign": address_sign})
        rsps = str(pysdk.invoke(contract_name, "storeFileInfo",
                                {"user_id": user_id, "hash_id": hash_id, "file_name": file_name, "uuid": uuid,
                                 "address_user": address_user, "address_sign": address_sign}))
        return {'tx_id': rsps[rsps.find("txid='") + 6:rsps.find("')")]}
    except Exception as e:
        return {'error': str(e)}


def download_data(self, contract_name, data):
    """
    调用合约，查询数据，输入文件名字
    :param contract_name: 合约名字
    :param data: 文件名字
    :return: 查询结果
    """
    try:
        pysdk = xuper.XuperSDK("http://" + Config.xuper_chain_ip + ":" + Config.xuper_chain_port, "xuper")
        pysdk.readkeys(Config.xuper_chain_key_file)
        name = bytes(data['hash_id'], encoding='utf-8')
        rsps = pysdk.invoke(contract_name, "queryFileInfoByHash", {"hash_id": name})
        return {'data': str(rsps[0][0], encoding="utf8")}
    except Exception as e:
        return {'error': str(e)}
