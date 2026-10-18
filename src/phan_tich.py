"""Bai tap tuan 5 - Co so Toan hoc cho AI.

Bai toan: du doan nguy co sinh vien bo hoc (Dropout=1 la "min", Graduate=0 la o an toan).
Chay het phan thong ke, mo hinh doi chung (Logistic tu cai bang Gradient Descent),
mo hinh attention nho de minh hoa hoc trong ngu canh, va luu ket qua vao results/.
"""
import os, warnings
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

import json, numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix)

SEED = 42
TAB = os.path.join(ROOT, "results", "tables") + os.sep
FIG = os.path.join(ROOT, "results", "figures") + os.sep
os.makedirs(TAB, exist_ok=True); os.makedirs(FIG, exist_ok=True)
DATA = os.path.join(ROOT, "data", "data.csv")
plt.rcParams.update({"figure.dpi": 130, "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False})

# ---------- 1. Doc du lieu, dinh nghia "min" ----------
raw = pd.read_csv(DATA, sep=";")
raw.columns = [c.strip() for c in raw.columns]
raw = raw.rename(columns={"Nacionality": "Nationality"})
d = raw[raw.Target != "Enrolled"].reset_index(drop=True)   # bo "o chua lat"
d["y"] = (d.Target == "Dropout").astype(int)

# bo dac trung gon (8 cot) va cac cau hinh khac
YEAR1 = ["Curricular units 1st sem (approved)", "Curricular units 1st sem (grade)",
         "Curricular units 2nd sem (approved)", "Curricular units 2nd sem (grade)"]
ENTRY = ["Tuition fees up to date", "Debtor", "Scholarship holder", "Age at enrollment"]
COMPACT = ENTRY + YEAR1
ADMISSION_ONLY = ["Admission grade", "Previous qualification (grade)", "Age at enrollment",
                  "Scholarship holder", "Debtor", "Tuition fees up to date", "Gender",
                  "Application order"]
ALL = [c for c in d.columns if c not in ("Target", "y")]

train_idx, test_idx = train_test_split(np.arange(len(d)), test_size=0.2,
                                       stratify=d.y, random_state=SEED)
ytr, yte = d.y.values[train_idx], d.y.values[test_idx]
json.dump({"train": train_idx.tolist(), "test": test_idx.tolist()},
          open(TAB + "split_seed42.json", "w"))

# ---------- 2. Thong ke mo ta ----------
info = {"n_raw": len(raw), "n_used": len(d), "n_features": len(ALL),
        "raw_counts": raw.Target.value_counts().to_dict(),
        "dropout_rate_used": float(d.y.mean()), "missing": int(raw.isna().sum().sum()),
        "n_train": len(train_idx), "n_test": len(test_idx),
        "dropout_rate_train": float(ytr.mean()), "dropout_rate_test": float(yte.mean())}

quant = ["Age at enrollment"] + YEAR1
desc = d[quant].describe(percentiles=[.25, .5, .75]).T
desc["variance"] = d[quant].var()
desc["median"] = d[quant].median()
desc = desc[["count", "mean", "median", "std", "variance", "min", "25%", "75%", "max"]]
desc.round(3).to_csv(TAB + "thong_ke_dinh_luong.csv")

# ngoai le theo IQR
out = {}
for c in quant:
    q1, q3 = d[c].quantile([.25, .75]); iqr = q3 - q1
    out[c] = int(((d[c] < q1 - 1.5 * iqr) | (d[c] > q3 + 1.5 * iqr)).sum())
info["outliers_iqr"] = out
info["zero_grade_sem2"] = int((d["Curricular units 2nd sem (grade)"] == 0).sum())
info["zero_grade_sem2_dropout_rate"] = float(
    d.loc[d["Curricular units 2nd sem (grade)"] == 0, "y"].mean())

rows = []
for c, names in [("Tuition fees up to date", {0: "Chua dong du", 1: "Da dong du"}),
                 ("Debtor", {0: "Khong no", 1: "Dang no"}),
                 ("Scholarship holder", {0: "Khong hoc bong", 1: "Co hoc bong"}),
                 ("Gender", {0: "Nu", 1: "Nam"})]:
    for v, nm in names.items():
        m = d[c] == v
        rows.append([c, nm, int(m.sum()), m.mean(), d.loc[m, "y"].mean()])
pd.DataFrame(rows, columns=["bien", "nhom", "so_sv", "ty_le", "ty_le_bo_hoc"]
             ).round(4).to_csv(TAB + "thong_ke_dinh_tinh.csv", index=False)

corr = d[COMPACT + ["y"]].corr()
corr.round(3).to_csv(TAB + "tuong_quan.csv")

# thang do
scale = d[COMPACT].agg(["min", "max", "mean", "std"]).T
scale.round(3).to_csv(TAB + "thang_do.csv")

# --- hinh thong ke ---
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
cnt = raw.Target.value_counts().reindex(["Graduate", "Dropout", "Enrolled"])
ax[0].bar(["Tốt nghiệp", "Bỏ học", "Đang học"], cnt.values,
          color=["#4C8C6B", "#C8553D", "#A0A0A0"])
for i, v in enumerate(cnt.values): ax[0].text(i, v + 30, str(v), ha="center")
ax[0].set_title("Nhãn gốc (4.424 sinh viên)")
c2 = d.y.value_counts().sort_index()
ax[1].bar(["An toàn (0)", "Bỏ học (1)"], c2.values, color=["#4C8C6B", "#C8553D"])
for i, v in enumerate(c2.values): ax[1].text(i, v + 30, f"{v}\n({v/len(d):.1%})", ha="center")
ax[1].set_title("Sau khi bỏ nhóm 'đang học' (3.630)"); ax[1].set_ylim(0, 2600)
plt.tight_layout(); plt.savefig(FIG + "h1_phan_bo_nhan.png"); plt.close()

fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
for a, c, t in zip(ax, ["Curricular units 1st sem (approved)",
                        "Curricular units 2nd sem (approved)", "Age at enrollment"],
                   ["Số môn qua HK1", "Số môn qua HK2", "Tuổi lúc nhập học"]):
    a.boxplot([d.loc[d.y == 0, c], d.loc[d.y == 1, c]], tick_labels=["An toàn", "Bỏ học"],
              patch_artist=True, boxprops=dict(facecolor="#DDE8E0"),
              medianprops=dict(color="#C8553D"))
    a.set_title(t)
plt.tight_layout(); plt.savefig(FIG + "h2_boxplot.png"); plt.close()

fig, ax = plt.subplots(figsize=(6.2, 5))
im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
short = ["Đóng học phí", "Nợ", "Học bổng", "Tuổi", "Qua HK1", "Điểm HK1",
         "Qua HK2", "Điểm HK2", "Bỏ học (y)"]
ax.set_xticks(range(len(short))); ax.set_xticklabels(short, rotation=45, ha="right")
ax.set_yticks(range(len(short))); ax.set_yticklabels(short)
for i in range(len(short)):
    for j in range(len(short)):
        ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center", fontsize=7)
plt.colorbar(im, shrink=.8); ax.set_title("Ma trận tương quan")
plt.tight_layout(); plt.savefig(FIG + "h3_tuong_quan.png"); plt.close()

fig, ax = plt.subplots(figsize=(5.5, 3.4))
g = pd.read_csv(TAB + "thong_ke_dinh_tinh.csv")
lab = ["Chưa đóng\nđủ học phí", "Đã đóng\nđủ", "Không nợ", "Đang nợ",
       "Không\nhọc bổng", "Có\nhọc bổng"]
sel = g.iloc[:6]
ax.bar(range(6), sel.ty_le_bo_hoc * 100,
       color=["#C8553D", "#4C8C6B", "#4C8C6B", "#C8553D", "#C8553D", "#4C8C6B"])
for i, v in enumerate(sel.ty_le_bo_hoc * 100): ax.text(i, v + 1, f"{v:.0f}%", ha="center")
ax.set_xticks(range(6)); ax.set_xticklabels(lab, fontsize=8)
ax.axhline(d.y.mean() * 100, ls="--", color="gray"); ax.set_ylabel("Tỉ lệ bỏ học (%)")
ax.set_title("Tỉ lệ bỏ học theo từng nhóm"); plt.tight_layout()
plt.savefig(FIG + "h4_ty_le_theo_nhom.png"); plt.close()


# ---------- 3. Logistic Regression tu cai ----------
def sigmoid(z):
    return np.where(z >= 0, 1 / (1 + np.exp(-np.clip(z, -500, 500))),
                    np.exp(np.clip(z, -500, 500)) / (1 + np.exp(np.clip(z, -500, 500))))

def bce(p, y):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

def fit_gd(X, y, lr, iters=2000, tol=0.0):
    n, m = X.shape
    w, b = np.zeros(m), 0.0
    hist = []
    for t in range(iters):
        p = sigmoid(X @ w + b)
        loss = bce(p, y); hist.append(loss)
        if not np.isfinite(loss): break
        gw = X.T @ (p - y) / n          # gradient: X^T (p - y) / n
        gb = np.mean(p - y)
        w -= lr * gw; b -= lr * gb
        if tol and t > 0 and abs(hist[-2] - loss) < tol: break
    return w, b, np.array(hist)

def metrics(y, p, thr=0.5):
    yh = (p >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, yh).ravel()
    return dict(accuracy=accuracy_score(y, yh), precision=precision_score(y, yh, zero_division=0),
                recall=recall_score(y, yh), f1=f1_score(y, yh),
                auc=roc_auc_score(y, p), TP=int(tp), FN=int(fn), FP=int(fp), TN=int(tn))

def prep(cols, standardize=True):
    Xa = d[cols].values.astype(float)
    Xtr, Xte = Xa[train_idx], Xa[test_idx]
    if standardize:
        mu, sd = Xtr.mean(0), Xtr.std(0); sd[sd == 0] = 1
        Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    return Xtr, Xte

# 3a. Thi nghiem toi uu (muc 2.5): thay doi toc do hoc, co / khong chuan hoa
Xtr, Xte = prep(COMPACT, True)
ref = LogisticRegression(penalty=None, max_iter=5000).fit(Xtr, ytr)
loss_opt = bce(ref.predict_proba(Xtr)[:, 1], ytr)
info["sklearn_train_loss_optimum"] = loss_opt

rows, curves = [], {}
for std in [True, False]:
    Xa, Xb = prep(COMPACT, std)
    for lr in [0.001, 0.01, 0.1, 1.0]:
        w, b, h = fit_gd(Xa, ytr, lr, iters=2000)
        ok = np.isfinite(h[-1])
        pte = sigmoid(Xb @ w + b) if ok else np.full(len(yte), 0.5)
        reach = int(np.argmax(h <= loss_opt + 1e-3)) + 1 if (h <= loss_opt + 1e-3).any() else None
        osc = int(np.sum(np.diff(h) > 1e-9)) if ok else None
        mt = metrics(yte, pte) if ok else {}
        rows.append(dict(chuan_hoa=std, toc_do_hoc=lr, loss_cuoi=h[-1],
                         vong_lap_den_gan_toi_uu=reach, so_lan_loss_tang=osc,
                         test_accuracy=mt.get("accuracy"), test_recall=mt.get("recall"),
                         test_auc=mt.get("auc")))
        curves[(std, lr)] = h
pd.DataFrame(rows).round(4).to_csv(TAB + "toi_uu_toc_do_hoc.csv", index=False)

fig, ax = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
for a, std, t in zip(ax, [True, False], ["Có chuẩn hóa dữ liệu", "Không chuẩn hóa"]):
    for lr, col in zip([0.001, 0.01, 0.1, 1.0], ["#A0A0A0", "#6C8EBF", "#4C8C6B", "#C8553D"]):
        h = curves[(std, lr)]
        a.plot(np.arange(1, len(h) + 1), np.minimum(h, 3), color=col, label=f"lr = {lr}")
    a.axhline(loss_opt, ls="--", color="k", lw=.8)
    a.set_xscale("log"); a.set_title(t); a.set_xlabel("Số vòng lặp")
ax[0].set_ylabel("Hàm mất mát (cross-entropy)"); ax[0].legend(); ax[0].set_ylim(0.3, 1.0)
plt.tight_layout(); plt.savefig(FIG + "h5_duong_loss.png"); plt.close()

# 3b. Doi chieu ban tu cai voi sklearn
w, b, h = fit_gd(Xtr, ytr, 1.0, iters=5000, tol=1e-12)
cmp = pd.DataFrame({"dac_trung": COMPACT, "w_tu_cai": w, "w_sklearn": ref.coef_[0]})
cmp.loc[len(cmp)] = ["(bias)", b, ref.intercept_[0]]
cmp.round(4).to_csv(TAB + "doi_chieu_tu_cai_sklearn.csv", index=False)
info["max_abs_diff_weights"] = float(np.abs(cmp.w_tu_cai - cmp.w_sklearn).max())
info["gd_iters_to_converge"] = int(len(h))

# 3c. Cac cau hinh dac trung (muc 2.7)
cfg = {"A. Luc nhap hoc (8 cot)": ADMISSION_ONLY,
       "B1. Nhap hoc + het HK1 (6 cot)": ENTRY + YEAR1[:2],
       "B. Nhap hoc + het HK2 (8 cot gon)": COMPACT,
       "C. Day du 35 cot": ALL}
rows, probs = [], {}
for name, cols in cfg.items():
    Xa, Xb = prep(cols, True)
    m = LogisticRegression(penalty=None, max_iter=5000).fit(Xa, ytr)
    ptr, pte = m.predict_proba(Xa)[:, 1], m.predict_proba(Xb)[:, 1]
    mt = metrics(yte, pte); mt_tr = metrics(ytr, ptr)
    rows.append(dict(cau_hinh=name, so_cot=len(cols), train_acc=mt_tr["accuracy"],
                     train_loss=bce(ptr, ytr), test_loss=bce(pte, yte), **mt))
    probs[name] = pte
pd.DataFrame(rows).round(4).to_csv(TAB + "cau_hinh_logistic.csv", index=False)

# ngưỡng quyết định (mục ngưỡng): đổi ngưỡng để tăng Recall
Xa, Xb = prep(COMPACT, True)
m = LogisticRegression(penalty=None, max_iter=5000).fit(Xa, ytr)
pte = m.predict_proba(Xb)[:, 1]
thr_rows = []
for thr in [0.2, 0.3, 0.4, 0.5, 0.6]:
    mt = metrics(yte, pte, thr); mt["nguong"] = thr; thr_rows.append(mt)
pd.DataFrame(thr_rows).round(4).to_csv(TAB + "nguong_quyet_dinh.csv", index=False)
fig, ax = plt.subplots(figsize=(5.4, 3.4))
t = pd.DataFrame(thr_rows)
ax.plot(t.nguong, t.recall, "o-", color="#C8553D", label="Recall (phát hiện em bỏ học)")
ax.plot(t.nguong, t.precision, "s-", color="#6C8EBF", label="Precision")
ax.plot(t.nguong, t.accuracy, "^-", color="#4C8C6B", label="Accuracy")
ax.set_xlabel("Ngưỡng báo 'nguy cơ bỏ học'"); ax.legend(); ax.set_title("Đánh đổi khi đổi ngưỡng")
plt.tight_layout(); plt.savefig(FIG + "h6_nguong.png"); plt.close()

cm = confusion_matrix(yte, (pte >= 0.5).astype(int))
fig, ax = plt.subplots(figsize=(3.6, 3.2))
ax.imshow(cm, cmap="Greens")
for i in range(2):
    for j in range(2): ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=14)
ax.set_xticks([0, 1]); ax.set_xticklabels(["Dự đoán\nan toàn", "Dự đoán\nbỏ học"])
ax.set_yticks([0, 1]); ax.set_yticklabels(["Thật:\nan toàn", "Thật:\nbỏ học"])
ax.set_title("Ma trận nhầm lẫn (cấu hình B)"); plt.tight_layout()
plt.savefig(FIG + "h7_nhamlan.png"); plt.close()

# ---------- 4. Attention nho (minh hoa hoc trong ngu canh, KHONG phai TabICLv2) ----------
def attn_predict(Xc, yc, Xq, tau):
    """Mot dau attention khong co trong so hoc: q.k = -||q-k||^2/2, softmax(./tau), phieu theo nhan."""
    d2 = ((Xq[:, None, :] - Xc[None, :, :]) ** 2).sum(-1)
    s = -d2 / (2 * tau)
    s -= s.max(1, keepdims=True)
    a = np.exp(s); a /= a.sum(1, keepdims=True)       # trong so attention
    return a @ yc                                      # P(bo hoc) = tong trong so cua cac nhan

rng = np.random.RandomState(SEED)
Xa, Xb = prep(COMPACT, True)
rows = []
for n_ctx in [50, 200, 800, len(ytr)]:
    idx = rng.choice(len(ytr), n_ctx, replace=False) if n_ctx < len(ytr) else np.arange(len(ytr))
    for tau in [0.05, 0.5, 2.0, 8.0]:
        p = attn_predict(Xa[idx], ytr[idx].astype(float), Xb, tau)
        mt = metrics(yte, p)
        rows.append(dict(so_mau_ngu_canh=n_ctx, tau=tau, **{k: mt[k] for k in
                    ["accuracy", "precision", "recall", "f1", "auc"]}))
pd.DataFrame(rows).round(4).to_csv(TAB + "attention_ngu_canh.csv", index=False)
att = pd.DataFrame(rows)
fig, ax = plt.subplots(figsize=(5.6, 3.4))
for tau, col in zip([0.05, 0.5, 2.0, 8.0], ["#C8553D", "#4C8C6B", "#6C8EBF", "#A0A0A0"]):
    s = att[att.tau == tau]
    ax.plot(s.so_mau_ngu_canh, s.auc, "o-", color=col, label=f"τ = {tau}")
ax.set_xscale("log"); ax.set_xlabel("Số sinh viên đưa vào ngữ cảnh"); ax.set_ylabel("AUC trên tập test")
ax.legend(); ax.set_title("Attention minh họa: ngữ cảnh càng nhiều càng tốt"); plt.tight_layout()
plt.savefig(FIG + "h8_attention.png"); plt.close()

# Vi du tinh tay: 1 sinh vien can du doan, 3 sinh vien trong ngu canh, 2 dac trung (da chuan hoa)
f2 = ["Curricular units 1st sem (approved)", "Curricular units 2nd sem (approved)"]
Xall = d[f2].values.astype(float)
mu, sd = Xall[train_idx].mean(0), Xall[train_idx].std(0)
Z = (Xall - mu) / sd
ex = {}
# chon 3 sv ngu canh tu tap train: 2 bo hoc / 1 an toan, 1 sv truy van tu test
def pick(pool, y, a, b):
    return [i for i in pool if d.y[i] == y and Xall[i, 0] == a and Xall[i, 1] == b][:1]
ctx = (pick(train_idx, 1, 0, 0) + pick(train_idx, 0, 6, 6) + pick(train_idx, 1, 2, 1)
       + pick(train_idx, 0, 5, 5))
q = pick(test_idx, 1, 1, 1)
Zc, Zq = Z[ctx], Z[q]
tau = 1.0
sc = -((Zq[:, None, :] - Zc[None]) ** 2).sum(-1) / (2 * tau)
a = np.exp(sc - sc.max()); a /= a.sum()
pq = float(a[0] @ d.y.values[ctx])
ex = dict(ngu_canh_idx=[int(i) for i in ctx], truy_van_idx=int(q[0]),
          raw_ctx=Xall[ctx].tolist(), raw_q=Xall[q][0].tolist(),
          z_ctx=Zc.round(3).tolist(), z_q=Zq[0].round(3).tolist(),
          nhan_ctx=d.y.values[ctx].tolist(), diem=sc[0].round(3).tolist(),
          trong_so=a[0].round(3).tolist(), p_bo_hoc=round(pq, 3),
          nhan_that=int(d.y[q[0]]), mu=mu.round(3).tolist(), sd=sd.round(3).tolist(), tau=tau)
json.dump(ex, open(TAB + "vi_du_attention.json", "w"), indent=1)

json.dump(info, open(TAB + "thong_tin_chung.json", "w"), indent=1, default=float)
print(json.dumps(info, indent=1, default=float))
print(desc.round(2)); print(pd.read_csv(TAB + "toi_uu_toc_do_hoc.csv"))
print(pd.read_csv(TAB + "cau_hinh_logistic.csv").T)
print(pd.read_csv(TAB + "nguong_quyet_dinh.csv"))
print(att.round(3).to_string()); print(json.dumps(ex, indent=1))
print(cmp.round(3))

# ---------- 5. So dieu kien (giai thich vi sao khong chuan hoa thi GD dao dong) ----------
cond = {}
for std in [True, False]:
    Xa, _ = prep(COMPACT, std)
    A = np.hstack([Xa, np.ones((len(Xa), 1))])
    ev = np.linalg.eigvalsh(A.T @ A / len(A))
    L = 0.25 * ev.max()                     # hang so Lipschitz cua gradient (cross-entropy logistic)
    cond["chuan_hoa" if std else "khong_chuan_hoa"] = dict(
        lam_max=float(ev.max()), lam_min=float(ev.min()), so_dieu_kien=float(ev.max() / ev.min()),
        lr_on_dinh_toi_da_2_over_L=float(2 / L))
json.dump(cond, open(TAB + "so_dieu_kien.json", "w"), indent=1)
print(json.dumps(cond, indent=1))
