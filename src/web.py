"""Dung trang web xem ket qua du an va mo trinh duyet.

    python src/web.py              # dung results/index.html, mo http://localhost:8000
    python src/web.py --build-only # chi dung index.html, khong mo server
Chi dung thu vien chuan cua Python va pandas. Doc cac bang o results/tables va hinh o results/figures.
"""
import base64, html, os, sys, threading, webbrowser, http.server, socketserver
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB, FIG = os.path.join(ROOT, "results", "tables"), os.path.join(ROOT, "results", "figures")
OUT = os.path.join(ROOT, "results", "index.html")


def csv(name):
    p = os.path.join(TAB, name)
    return pd.read_csv(p) if os.path.exists(p) else None


def table(df, pct=(), dec=3):
    if df is None:
        return "<p class=note>(Chua co du lieu: hay chay phan_tich.py truoc.)</p>"
    df = df.copy()
    for c in df.columns:
        if c in pct:
            df[c] = df[c].map(lambda v: f"{100 * v:.1f}%")
        elif df[c].dtype.kind == "f":
            df[c] = df[c].map(lambda v: "" if pd.isna(v) else f"{v:.{dec}f}")
    return df.to_html(index=False, border=0, classes="t", na_rep="")


def img(name, cap):
    p = os.path.join(FIG, name)
    if not os.path.exists(p):
        return ""
    b64 = base64.b64encode(open(p, "rb").read()).decode()
    return f'<figure><img src="data:image/png;base64,{b64}"><figcaption>{html.escape(cap)}</figcaption></figure>'


def section(title, body, note=""):
    n = f"<p class=note>{note}</p>" if note else ""
    return f"<section><h2>{title}</h2>{n}{body}</section>"


def build():
    lg, tb = csv("cau_hinh_logistic.csv"), csv("tabicl_ketqua.csv")
    S = []
    S.append(section("1. Bai toan va du lieu",
        img("h1_phan_bo_nhan.png", "Phan bo nhan sau khi bo nhom dang hoc") + img("h4_ty_le_theo_nhom.png", "Ty le bo hoc theo tien bac") +
        table(csv("thong_ke_dinh_tinh.csv"), pct=("ty_le", "ty_le_bo_hoc")),
        "Moi sinh vien la mot o tren ban do min: tot nghiep = an toan (0), bo hoc = min (1), dang hoc = o chua lat nen loai ra. 3.630 em, 39,1% bo hoc."))
    S.append(section("2. Thong ke mo ta", table(csv("thong_ke_dinh_luong.csv")) + img("h2_boxplot.png", "Boxplot bien dinh luong") + img("h3_tuong_quan.png", "Tuong quan"),
        "Diem hoc ky 2 bang 0 thuong la em da nghi (khoang 91% bo hoc), nen du lieu hoc ky 2 phan nao chua san dap an."))
    sk = None
    p = os.path.join(TAB, "so_dieu_kien.json")
    if os.path.exists(p):
        import json
        j = json.load(open(p))
        sk = pd.DataFrame([{"du lieu": k, "tri rieng lon nhat": v["lam_max"], "so dieu kien": v["so_dieu_kien"], "toc do hoc an toan toi da": v["lr_on_dinh_toi_da_2_over_L"]} for k, v in j.items()])
    S.append(section("3. Toi uu: Gradient Descent va toc do hoc", table(csv("toi_uu_toc_do_hoc.csv"), dec=4) + img("h5_duong_loss.png", "Duong mat mat theo toc do hoc") + table(sk, dec=4) +
        table(csv("doi_chieu_tu_cai_sklearn.csv"), dec=4),
        "Khong chuan hoa: toc do hoc 0,1 dao dong, 1,0 phan ky. Giai thich bang so dieu kien (67 so voi 30.622). Ban tu cai khop sklearn den 0,0005."))
    if lg is not None:
        ten = {"A": "A. Luc nhap hoc (8 cot)", "B1": "B1. Het HK1 (6 cot)", "B": "B. Het HK2 (8 cot)", "C": "C. Day du 35 cot"}
        order = {"A": 0, "B1": 1, "B": 2, "C": 3}

        def chuan(df, ten_mh):
            d = df[["cau_hinh", "accuracy", "precision", "recall", "f1", "auc"]].copy()
            d["k"] = d["cau_hinh"].str.split(".").str[0].str.strip()
            d["cau_hinh"] = d["k"].map(ten)
            d["o"] = d["k"].map(order) * 2 + (0 if ten_mh.startswith("Hoi") else 1)
            d.insert(1, "mo hinh", ten_mh)
            return d.drop(columns=["k"])
        c = chuan(lg, "Hoi quy Logistic")
        if tb is not None:
            c = pd.concat([c, chuan(tb, "TabICLv2")])
        c = c.sort_values("o").drop(columns=["o"])
        body = table(c, dec=4)
    else:
        body = table(None)
    S.append(section("4. Ket qua: Hoi quy Logistic va TabICLv2", body,
        "Tren cung cach chia (seed 42, 726 em kiem tra). Sai so Accuracy khoang +-2,2 diem. TabICLv2 co AUC cao hon, nhung chenh Accuracy nho hon sai so; moi chay mot lan."))
    S.append(section("5. Nguong bao dong va ma tran nham lan", img("h6_nguong.png", "Recall, Precision, Accuracy theo nguong") + img("h7_nhamlan.png", "Ma tran nham lan (cau hinh B)") + table(csv("nguong_quyet_dinh.csv")),
        "Bo sot dat hon bao nham: ha nguong tu 0,5 xuong 0,3 thi Recall tang, bo sot giam tu 41 xuong 24 em, bao nham tang tu 32 len 71."))
    S.append(section("6. Attention minh hoa (khong phai TabICLv2)", img("h8_attention.png", "Vi du attention") + table(csv("attention_ngu_canh.csv")),
        "Ban don gian tu viet, khong co trong so hoc duoc; chi de thay co che so sanh, softmax, bo phieu."))
    css = ("body{font-family:Segoe UI,Arial,sans-serif;max-width:1000px;margin:24px auto;padding:0 16px;color:#17243A;background:#F6F3EC}"
           "h1{font-size:28px}h2{border-bottom:2px solid #2F7A5E;padding-bottom:4px;margin-top:36px}.note{background:#fff;border-left:4px solid #B8452F;padding:8px 12px}"
           "table.t{border-collapse:collapse;margin:12px 0;font-size:13px;background:#fff}table.t th,table.t td{border:1px solid #ddd;padding:4px 8px;text-align:right}"
           "table.t th{background:#DCE6F1}table.t td:first-child{text-align:left}figure{margin:12px 0}img{max-width:100%;border:1px solid #ddd;background:#fff}figcaption{font-size:13px;color:#555}")
    page = f"<!doctype html><meta charset=utf-8><title>Du doan sinh vien bo hoc</title><style>{css}</style><h1>Du doan nguy co sinh vien bo hoc (Nhom 6)</h1><p>Ket qua sinh tu results/. Chay lai phan_tich.py de cap nhat.</p>{''.join(S)}"
    open(OUT, "w", encoding="utf-8").write(page)
    print("Da dung", OUT)


def serve(port=8000):
    os.chdir(os.path.join(ROOT, "results"))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), http.server.SimpleHTTPRequestHandler) as srv:
        url = f"http://localhost:{port}/index.html"
        print("Mo trang web:", url, "(nhan Ctrl+C de dung)")
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("Da dung.")


if __name__ == "__main__":
    build()
    if "--build-only" not in sys.argv:
        serve()
