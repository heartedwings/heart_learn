import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from utils.save_to_base64 import save_plot_to_base64


def get_learning_curve(xgb_best_model, X_train, y_train):
    # 学習曲線を計算
    train_sizes, train_scores, test_scores = learning_curve(
        estimator=xgb_best_model,  # 学習済みモデル (XGBoostモデルを想定)
        X=X_train,  # 学習データ
        y=y_train,  # 学習ラベル
        cv=5,  # 交差検証の分割数
        scoring="accuracy",  # 評価指標
        n_jobs=-1,  # 並列処理を使用
        train_sizes=np.linspace(0.1, 1.0, 10),  # 学習データの割合（10%から100%）
        random_state=42,  # 再現性のための乱数シード
    )

    # 平均と標準偏差の計算
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    # 学習曲線のプロット
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, label="Training Score", color="blue", marker="o")
    plt.fill_between(
        train_sizes,
        train_mean - train_std,
        train_mean + train_std,
        alpha=0.15,
        color="blue",
    )

    plt.plot(
        train_sizes,
        test_mean,
        label="Validation Score",
        color="orange",
        marker="o",
        linestyle="--",
    )
    plt.fill_between(
        train_sizes,
        test_mean - test_std,
        test_mean + test_std,
        alpha=0.15,
        color="orange",
    )

    # グラフの装飾
    plt.title("Learning Curve")
    plt.xlabel("Training Set Size")
    plt.ylabel("Accuracy")
    plt.legend(loc="best")
    plt.grid()
    learn_curve_image = save_plot_to_base64()

    return {"l_c_image": learn_curve_image}
