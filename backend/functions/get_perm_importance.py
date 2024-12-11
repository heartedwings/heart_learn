import pandas as pd
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
from utils.save_to_base64 import save_plot_to_base64
import shap


def get_perm_importance(xgb_best_model, X_test, y_test, data):
    # permutation_importanceの算出
    perm_importance = permutation_importance(
        xgb_best_model,
        X_test,
        y_test,
        scoring="accuracy",
        n_repeats=30,
        random_state=42,
    )

    # DataFrameで可視化用データを整形
    importance_data = pd.DataFrame(
        {
            "feature": [X_test.columns[i] for i in range(X_test.shape[1])],
            "importance": perm_importance.importances_mean,
            "std": perm_importance.importances_std,
        }
    ).sort_values(by="importance", ascending=False)

    # 特徴量重要度の棒グラフ
    plt.figure(figsize=(10, 6))
    bars = plt.barh(
        importance_data["feature"],
        importance_data["importance"],
        xerr=importance_data["std"],
        color="skyblue",
    )
    plt.xlabel("Permutation Importance")
    plt.ylabel("Features")
    plt.title("Feature Importance based on Permutation")
    plt.gca().invert_yaxis()
    plt.xlim(0, 0.17)
    # 各棒の横に標準偏差と重要度の実数値を表示
    for bar, importance, std in zip(
        bars, importance_data["importance"], importance_data["std"]
    ):
        plt.text(
            bar.get_width() + std,
            bar.get_y() + bar.get_height() / 2,
            f"  {importance:.3f} ± {std:.3f}",
            va="center",
        )
    perm_importance_image = save_plot_to_base64()

    # SHAP値の計算とプロット
    explainer = shap.Explainer(xgb_best_model, X_test)
    shap_values = explainer(X_test)
    plt.figure()  # SHAPプロット用の新しいFigureを作成
    shap.summary_plot(shap_values, X_test, feature_names=data.columns, show=False)
    shap_image = save_plot_to_base64()

    return {
        "importance_data": importance_data.to_dict(orient="list"),
        "p_i_image": perm_importance_image,
        "s_image": shap_image,
    }
