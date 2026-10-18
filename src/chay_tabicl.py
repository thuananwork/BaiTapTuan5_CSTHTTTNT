"""Chay TabICLv2 tren bo du lieu bo hoc, dung CUNG cach chia train/test (seed 42) voi phan con lai cua bai.

CACH CHAY (tren may co internet; lan dau se tu tai checkpoint tabicl-classifier-v2-20260212.ckpt tu HuggingFace):
    pip install tabicl scikit-learn pandas numpy
    python chay_tabicl.py

Ket qua ghi vao results/tables/tabicl_khao_sat.csv. (Khong ghi de tabicl_ketqua.csv la ket qua da dung trong bao cao.)
LUU Y: script nay chua duoc chay thu; cung cach goi TabICLClassifier da chay duoc trong notebook 05.
Neu bao loi ten tham so, doi chieu README cua https://github.com/soda-inria/tabicl.
"""
import json, time, os, warnings
import numpy as np, pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix)
from tabicl import TabICLClassifier

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
raw = pd.read_csv(os.path.join(ROOT, "data", "data.csv"), sep=";")
raw.columns = [c.strip() for c in raw.columns]
d = raw[raw.Target != "Enrolled"].reset_index(drop=True)      # bo nhom "dang hoc"
d["y"] = (d.Target == "Dropout").astype(int)

split = json.load(open(os.path.join(ROOT, "results", "tables", "split_seed42.json")))
tr, te = np.array(split["train"]), np.array(split["test"])

YEAR1 = ["Curricular units 1st sem (approved)", "Curricular units 1st sem (grade)",
         "Curricular units 2nd sem (approved)", "Curricular units 2nd sem (grade)"]
ENTRY = ["Tuition fees up to date", "Debtor", "Scholarship holder", "Age at enrollment"]
ADMISSION_ONLY = ["Admission grade", "Previous qualification (grade)", "Age at enrollment",
                  "Scholarship holder", "Debtor", "Tuition fees up to date", "Gender",
                  "Application order"]
ALL = [c for c in d.columns if c not in ("Target", "y")]
CFG = {"A. Luc nhap hoc (8 cot)": ADMISSION_ONLY,
       "B1. Nhap hoc + het HK1 (6 cot)": ENTRY + YEAR1[:2],
       "B. Nhap hoc + het HK2 (8 cot gon)": ENTRY + YEAR1,
       "C. Day du 35 cot": ALL}


def run(cols, n_ctx=None, n_est=8, seed=42):
    X = d[cols].values.astype(float)           # TabICL tu xu ly thang do, khong can chuan hoa
    y = d.y.values
    idx = tr
    if n_ctx is not None and n_ctx < len(tr):
        idx = np.random.RandomState(seed).choice(tr, n_ctx, replace=False)
    t0 = time.time()
    clf = TabICLClassifier(n_estimators=n_est, random_state=seed)
    clf.fit(X[idx], y[idx])                    # "fit" chi la dua ngu canh vao, khong cap nhat trong so
    p = clf.predict_proba(X[te])[:, 1]
    yh = (p >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y[te], yh).ravel()
    return dict(accuracy=accuracy_score(y[te], yh), precision=precision_score(y[te], yh),
                recall=recall_score(y[te], yh), f1=f1_score(y[te], yh),
                auc=roc_auc_score(y[te], p), TP=tp, FN=fn, FP=fp, TN=tn,
                giay=round(time.time() - t0, 1))


rows = []
for name, cols in CFG.items():                              # (1) cac cau hinh dac trung
    r = run(cols); r.update(thi_nghiem="cau_hinh", cau_hinh=name, so_mau_ngu_canh=len(tr), n_estimators=8)
    rows.append(r); print(r)
B = CFG["B. Nhap hoc + het HK2 (8 cot gon)"]
for n_ctx in [50, 200, 800, len(tr)]:                        # (2) kich thuoc ngu canh
    r = run(B, n_ctx=n_ctx); r.update(thi_nghiem="ngu_canh", cau_hinh="B", so_mau_ngu_canh=n_ctx, n_estimators=8)
    rows.append(r); print(r)
for n_est in [1, 8]:                                         # (3) so thanh vien ensemble
    r = run(B, n_est=n_est); r.update(thi_nghiem="n_estimators", cau_hinh="B", so_mau_ngu_canh=len(tr), n_estimators=n_est)
    rows.append(r); print(r)

out = pd.DataFrame(rows)
out.round(4).to_csv(os.path.join(ROOT, "results", "tables", "tabicl_khao_sat.csv"), index=False)
print("Da luu results/tables/tabicl_khao_sat.csv")
