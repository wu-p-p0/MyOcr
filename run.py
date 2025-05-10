import base64
import json
import os.path

from flask import Flask, request

from core import OCR, KeywordDetector

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
        file_name = data["name"]
        str_data = data["base64"]
        raw = base64.b64decode(str_data.encode("utf-8"))

        path = os.path.join("temp", file_name)
        with open(path, "wb") as f:
            f.write(raw)

        result = ocr.read(path)
        text = "".join(result)

        if not k_detector.contains_keywords(text):
            text = {"status": "OK", "text": result}
        else:
            text = {"status": "WARNING", "text": "文件包含敏感词，禁止识别"}
    except Exception as e:
        text = {"status": "NO", "text": e}

    return text


if __name__ == "__main__":
    print("初始化OCR...")
    ocr = OCR()
    print("-" * 100)

    print("初始化关键词检测...")
    k_detector = KeywordDetector()
    print("-" * 100)

    print("初始化WBE API...")
    app.run(debug=False, host="192.168.31.155")
    print("-" * 100)
