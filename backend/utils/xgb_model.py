import matplotlib

matplotlib.use("Agg")  # GUI を無効化するバックエンドを設定
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
import os


def process_csv_and_predict(csv_path, output_folder):
    """
    CSVを処理し、予測結果を返却する関数
    """
    # CSVの読み込み
    data = pd.read_csv(csv_path)

    # 質的変数の前処理
    chest_map = {"ASY": 0, "NAP": 1, "ATA": 1, "TA": 1}
    resting_ecg_map = {"Normal": 0, "ST": 1, "LVH": 2}
    slope_map = {"Down": -1, "Flat": 0, "Up": 1}

    data["ChestPainType"] = data["ChestPainType"].map(chest_map).astype("int")
    data["RestingECG"] = data["RestingECG"].map(resting_ecg_map).astype("int")
    data["ST_Slope"] = data["ST_Slope"].map(slope_map).astype("int")

    # 説明変数と目的変数に分ける
    X_test = data.drop(columns=["HeartDisease"])
    y_test = data["HeartDisease"]

    # JSON形式で保存
    loaded_xgb_best_model = xgb.XGBClassifier()
    loaded_xgb_best_model.load_model("xgb_best_model.json")

    # 予測を実行
    predictions = loaded_xgb_best_model.predict(X_test)

    # 結果の表示
    accuracy = accuracy_score(y_test, predictions)
    accuracy_percentage = accuracy * 100
    conf_matrix = confusion_matrix(y_test, predictions)

    # 混同行列を可視化してPDFに保存
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix\nAccuracy: {accuracy_percentage:.2f}%")

    # PDF ファイルに保存
    output_pdf = os.path.join(output_folder, "confusion_matrix.png")
    plt.savefig(output_pdf, format="png")
    plt.close()  # プロットを閉じてメモリを解放
    image_url = f"/backend/outputs/confusion_matrix.png"

    print(f"Accuracy: {accuracy_percentage:.2f}%")
    print(f"Confusion Matrix:\n{conf_matrix}")

    # 結果を保存
    output_file = os.path.join(output_folder, "result.csv")
    result_df = pd.DataFrame({"Actual": y_test, "Predicted": predictions})
    result_df.to_csv(output_file, index=False)

    # 結果を返却
    return {
        "accuracy": accuracy_percentage,
        "confusion_matrix": {"data": conf_matrix.tolist(), "image": image_url},
    }


if __name__ == "__main__":
    # テスト用のコード
    test_csv_path = "test_data.csv"  # テスト用CSVのパス
    output_dir = "./output"  # 結果保存用ディレクトリ
    os.makedirs(output_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

    result = process_csv_and_predict(test_csv_path, output_dir)
    print("Prediction Result:", result)
