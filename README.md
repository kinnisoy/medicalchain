# medicalchain

区块链在医疗行业的应用，web界面可视化展示

[界面在线预览](http://113.24.61.160:9001/html_web/)(ps：来自gitee用户：郭飞飞)

本项目fork自gitee[医学联盟](https://gitee.com/medical-alliance/medical-blockchain)

原项目部署后，web页面及静态资源访问出错，修改路由和文件目录结构后可以正常使用。

## Usage：

### 按照gitee的[配置步骤](./gitee_readme.md)：
    安装ficso
    安装python[3.6+]
    安装Python-sdk
    修改`app.py`文件中flask的`root_path`为自己的项目路径地址
    拉取本项目并运行app.py
### 使用docker部署：
##### 1.拉取镜像
```bash
docker push kinnisoy/medicalchain:tagname
```
##### 2.启动区块链
项目文件在home路径
首先在`/home/fisco`路径下运行:
```bash
bash nodes/127.0.0.1/start_all.sh
```
![image](https://user-images.githubusercontent.com/40685598/162930120-3d479930-3aa5-4168-ae2d-2f8a686dc1ec.png)

##### 3.将节点地址写入网站配置
节点启动后，回到`/home/medical-blockchian`路径下：
```python
python ficso_bcos_before.py
```
![image](https://user-images.githubusercontent.com/40685598/162930642-60b81530-315b-4fcb-aa6d-414d519b8ab2.png)

将结果地址填写到`client_config.py`的最后。


##### 4.网站启动
```python
python app.py
```



>Ps:docker中，可能有部分前端显示不是很完美，可以重新拉一下本仓库即可。
