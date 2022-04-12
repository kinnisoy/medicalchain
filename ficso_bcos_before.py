from client_config import client_config
from ficsobcos_main import fiscobcos_deploy, fiscobcos_download, fiscobcos_upload

print(fiscobcos_deploy())
# download_result = fiscobcos_download('0x4608749177bdcea3f2fd13807f5412e6cde150b6',
#                                      ['lidunwei1'.encode()])
# print(download_result)
# upload_result = fiscobcos_upload('0x1f494c56c3ad1e6738f3500d19499cd3541160ea',
#                                      ['lidunwei1','lidunwei3'.encode(),'lidunwei1','lidunwei','lidunwei'])
# print(upload_result)
# {'blockHash': '0x02dbb6e6227a733370bfbde2af6fb6be874007c14e7c279df7f9358895cfb817', 'blockNumber': '0x3', 'gasUsed': '0x201d2', 'transactionHash': '0x3c0156f37897047df06aee2bd32585a97b907c816b5887a02cdad3c3767b74e8', 'contractname': '0x1f494c56c3ad1e6738f3500d19499cd3541160ea', 'error': '0'}
# download_result = fiscobcos_download('0x1f494c56c3ad1e6738f3500d19499cd3541160ea',
#                                      ['lidunwei3'.encode()])
# print(download_result)
