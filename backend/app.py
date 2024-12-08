from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd
from flask_cors import CORS
import traceback

from utils.xgb_model import process_csv_and_predict

app = Flask(__name__)

# アップロードされたファイルの保存先ディレクトリ
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
OUTPUT_FOLDER = os.path.join(os.getcwd(), "outputs")

# フォルダが存在しなければ作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Flaskの設定
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
# CORS設定
# CORS(app, resources={r"/upload_csv": {"origins": "http://localhost:8080"}})
CORS(app)


@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    """CSVファイルを受け取り、保存し、処理して結果を返却"""

    file = request.files["file"]

    # ファイル名を安全にして保存
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        # CSV処理と予測結果を取得
        result = process_csv_and_predict(file_path, app.config["OUTPUT_FOLDER"])
        return jsonify({"success": True, "result": result})
    except Exception as e:
        # エラーが発生した場合はスタックトレースをログに表示
        print(f"Error: {e}")
        traceback.print_exc()  # これで詳細なエラートレースを表示
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
