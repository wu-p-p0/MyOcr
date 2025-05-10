import base64
import json
import os.path

from flask import Flask, request

from OCR_Server.core.ocr import OCR

ocr = OCR()
app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"


@app.route("/t", methods=["POST"])
def test():
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
        text = {"status": "OK", "text": result}
    except Exception as e:
        text = {"status": "NO", "text": e}

    return text


if __name__ == "__main__":
    app.run(debug=False, host="192.168.31.155")
