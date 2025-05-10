import base64
import json
import os.path
import hashlib

from flask import Flask, request


from core import OCR, KeywordDetector
from config import api_config

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"


@app.route("/ocr", methods=["POST"])
def img_ocr():

    os.makedirs("temp", exist_ok=True)
    for file in os.listdir("temp"):
        os.remove(os.path.join("temp", file))
    data = request.data.decode("utf-8")

    try:
        data = json.loads(data)

        file_ex = data["name"].split('.')[-1].lower()
        str_data = data["base64"]

        if file_ex in api_config.img_extensions:
            raw = base64.b64decode(str_data.encode("utf-8"))
            file_name = ".".join([hashlib.md5(raw).hexdigest()[:8], file_ex])

            path = os.path.join("temp", file_name)
            with open(path, "wb") as f:
                f.write(raw)

            result = ocr.read(path)
            content = "".join(result)

            if not k_detector.contains_keywords(content):
                text = {"status": "OK", "text": result}
            else:
                text = {"status": "WARNING", "text": "文件包含敏感词，禁止识别"}

        else:
            text = {"status": "ERROR", "text": "不支持的文件格式"}
    except Exception as e:
        text = {"status": "ERROR", "text": str(e)}

    return text


if __name__ == "__main__":
    print("初始化OCR...")
    ocr = OCR()
    print("-" * 100)

    print("初始化关键词检测...")
    k_detector = KeywordDetector()
    print("-" * 100)

    print("初始化WBE API...")
    app.run(debug=False, host=api_config.host, port=api_config.prot)
    print("-" * 100)
