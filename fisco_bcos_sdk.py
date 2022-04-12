# -*- coding: utf-8 -*-
'''
  数据存证，上下链查询
  @author: boblee
  @date: 2019-012-16
'''
from client.contractnote import ContractNote
from client.bcosclient import BcosClient
from client.datatype_parser import DatatypeParser


class ApiFiscoBcos():
    """
    使用 fisco-bcos数据存证及查询
    """

    def __init__(self):
        self.author = 'bob.lee'

    def deploy_contract(self, contract_bin, contract_name=None):
        """
        部署合约
        :param contract_bin: 合约二进制文件
        :param contract_name: 合约名字，默认可以不保存
        :return: 返回合约的结果
        """
        try:
            client = BcosClient()
            result = client.deploy(contract_bin)
            memo = "tx:" + result["transactionHash"]
            if contract_name:
                ContractNote.save_address(contract_name,
                                          result["contractAddress"],
                                          int(result["blockNumber"], 16), memo)
            client.finish()
            return result
        except Exception as e:
            return {'error': str(e)}

    def data_upload(self, args, to_address, contract_abi,function_):
        """
        调用部署好的合约上传数据
        :param args: 数据参数，格式[id，名字，文件哈希],例子：args = [1, 'q1.png', 'a482dedfb805dc46d2b96541f218987c']
        :param to_address: 合约地址
        :param contract_abi: 合约abi
        :return:  交易返回结果
        """
        try:
            client = BcosClient()
            data_parser = DatatypeParser()
            receipt = client.sendRawTransactionGetReceipt(to_address, contract_abi, function_, args)
            txhash = receipt['transactionHash']
            txresponse = client.getTransactionByHash(txhash)
            inputresult = data_parser.parse_transaction_input(txresponse['input'])
            # 解析该交易在receipt里输出的output,即交易调用的方法的return值
            outputresult = data_parser.parse_receipt_output(inputresult['name'], receipt['output'])[0]
            client.finish()
            receipt['output'] = outputresult
            return receipt
        except Exception as e:
            return {'error': str(e)}

    def data_download(self, args, to_address, contract_abi, function_):
        """
              调用部署好的合约查询链上数据
              :param args: 数据参数，格式[id],例子：args = [1]
              :param to_address: 合约地址
              :param contract_abi: 合约abi
              :return:  交易返回结果
              """
        try:
            client = BcosClient()
            data_parser = DatatypeParser()
            receipt = client.sendRawTransactionGetReceipt(to_address, contract_abi, function_, args)
            txhash = receipt['transactionHash']
            txresponse = client.getTransactionByHash(txhash)
            inputresult = data_parser.parse_transaction_input(txresponse['input'])
            # 解析该交易在receipt里输出的output,即交易调用的方法的return值
            outputresult = data_parser.parse_receipt_output(inputresult['name'], receipt['output'])
            # print("receipt output :", outputresult)
            client.finish()
            receipt['output'] = outputresult
            return receipt
        except Exception as e:
            return {'error': str(e)}
