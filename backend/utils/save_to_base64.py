import matplotlib.pyplot as plt
import base64
from io import BytesIO

def save_plot_to_base64():
    """現在のプロットをBase64形式で保存して返す"""
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close()  # メモリ節約のためプロットを閉じる
    return f"data:image/png;base64,{img_base64}"
