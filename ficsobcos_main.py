from fisco_bcos_sdk import ApiFiscoBcos
from client_config import client_config
import json
from client.datatype_parser import DatatypeParser
from client.bcosclient import BcosClient


def fiscobcos_deploy():
    try:
        Api = ApiFiscoBcos()
        with open(client_config.fiscobcos_bin_file, 'r') as load_f:
            contract_bin = load_f.read().replace("\n", '')
            load_f.close()
        deploy_result = Api.deploy_contract(contract_bin)
        return {'contract_address': deploy_result['contractAddress']}
    except Exception as e:
        return {'error': str(e)}


def fiscobcos_upload(contract_address, data):
    try:
        Api = ApiFiscoBcos()
        abi_file = client_config.fiscobcos_abi_file
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        contract_abi = data_parser.contract_abi
        result = Api.data_upload(data, contract_address, contract_abi, "upload")
        # print(result)
        if result['output'] == 3002:
            data_json = json.loads(json.dumps(result))
            if 'blockHash' in data_json:
                data_json = {"blockHash": data_json["blockHash"], "blockNumber": data_json['blockNumber'],
                             "gasUsed": data_json['gasUsed'], "transactionHash": data_json['transactionHash'],
                             "contractname": contract_address, 'error': '0'}
                tran_result = Api.data_upload([data_json['transactionHash'], data[1]], contract_address, contract_abi,
                                              "tran_upload")
                return data_json
            else:
                return result
        else:
            return {'error': '数据已经存在'}
    except Exception as e:
        return {'error': str(e)}


def fiscobcos_download(contract_address, data):
    try:
        Api = ApiFiscoBcos()
        abi_file = client_config.fiscobcos_abi_file
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        contract_abi = data_parser.contract_abi
        result = Api.data_download(data, contract_address, contract_abi, "tran_download")
        my_data = Api.data_download(data, contract_address, contract_abi, "download")
        client = BcosClient()
        if result['output'][0] != '':
            response = {"file_data": my_data['output'][0], "file_time": my_data['output'][2],
                        "file_pubkey": my_data['output'][3], "file_sign": my_data['output'][4]}
            hash_data = client.getTransactionReceipt(result['output'][0])
            response['blockHash'] = hash_data['blockHash']
            response['blockNumber'] = hash_data['blockNumber']
            response['contractAddress'] = contract_address
            response['gasUsed'] = hash_data['gasUsed']
            response['transactionHash'] = hash_data['transactionHash']
            response['transactionIndex'] = hash_data['transactionIndex']
            return response
        else:
            return {'error': '数据不存在'}
    except Exception as e:
        return {'error': str(e)}
