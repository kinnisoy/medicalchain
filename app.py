# encoding: utf-8
import json
from flask import Flask, request, jsonify,redirect ,url_for,render_template
from flasgger import Swagger
from flask_cors import *
import time
from client_config import client_config
from ficsobcos_main import fiscobcos_deploy, fiscobcos_upload, fiscobcos_download
from encrypt_de import passWord

app = Flask(__name__,root_path = "/home/medical-blockchain/html_web")
# app = Flask(__name__,root_path = "D:\\medical-blockchain-master\\html_web")
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
# app.config['root_path'] = "D:\\medical-blockchain-master\\html_web"
CORS(app, suppors_credentials=True, resources={r'/*'})  # 设置跨域
swagger = Swagger(app)

# app = Flask(__name__)


@app.route('/api/p/medical/blockchain/deploy', methods=['GET'])
def deploy():
    deploy_result = fiscobcos_deploy()
    return jsonify(deploy_result)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/tools_html/blockchain/<var>', methods=['GET'])
def to(var):
    return render_template('tools_html/blockchain/'+var)


@app.route('/api/p/medical/blockchain/upload', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def upload_page():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    upload_result = fiscobcos_upload(client_config.contract_address,
                                     [str(data["file_data"]), data["file_hash"].encode(), str(int(time.time())),
                                      data["file_pubkey"],
                                      data["file_sign"]])
    return jsonify(upload_result)


@app.route('/api/p/medical/blockchain/download', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def download_page():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    download_result = fiscobcos_download(client_config.contract_address,
                                         [data["file_hash"].encode()])
    return jsonify(download_result)


@app.route('/api/p/medical/blockchain/crate', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def crate():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    result = passWord().get_key(data["key"])
    return jsonify(result)


@app.route('/api/p/medical/blockchain/sign', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def sign_():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    result = passWord().message_sign(data["text"], data["prvkey"])
    return jsonify(result)


@app.route('/api/p/medical/blockchain/verify', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def verify():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    result = passWord().verifity(data["text"], data["sign"], data["address"])
    return jsonify(result)


@app.route('/api/p/medical/blockchain/hash', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def data_hash():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    result = passWord().message_hash(data["text"])
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=client_config.config_port)
