# 基于easy-orc和flask的文字识别服务

## 启动说明
1. ### 按照requirements.txt安装依赖
2. ### 根据需求修改config文件夹中的py文件
3. ### 运行run.py启动服务

## 请求用法
### 访问 http://host:port/orc（根据实际端口和地址调整）
```python
# 请求包必须含有的内容
unit.update({"base64": data})  # 图片的base64编码
unit.update({"name": file_name})  # 上传图片的文件名

data_json = json.dumps(unit)
response = requests.post("http://host:port/ocr", data=data_json)
```

### 解析负载
```python
data = json.loads(response.text)
text = data["text"]  # 识别内容或反馈
status = data["status"]  # 请求状态
```

### 状态status意义
```text
"OK"        ---         成功识别
"ERROR"     ---         识别失败，错误见“text”
“WARNING”   ---         识别内容包含keywords/keywords.csv中的违禁词
```

