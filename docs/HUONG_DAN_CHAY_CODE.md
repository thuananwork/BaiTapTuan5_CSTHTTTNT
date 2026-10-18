# Hướng dẫn chạy code

## Cách nhanh nhất: bấm đúp `run.bat`
`run.bat` ở thư mục gốc dự án tự làm hết: tìm Python (chưa có thì cài bằng winget), tạo `.venv`, cài thư viện (lần đầu), rồi hiện menu:
- **1**: chạy phân tích và mở trang web kết quả tại http://localhost:8000/index.html (khuyên dùng, khoảng 15 giây). Nhấn Ctrl+C trong cửa sổ để tắt web.
- **2**: chỉ mở trang web, không chạy lại phân tích.
- **3**: chạy TabICLv2 khảo sát (tự cài `tabicl` và PyTorch, cần internet, lâu).
- **4**: dựng lại báo cáo Word (ghi đè file Word, hỏi xác nhận).

`run.bat` đã được mở thử trên máy Windows của bạn: nó tìm thấy Python, dùng `.venv`, kiểm tra thư viện và hiện menu đúng. Các lựa chọn 1 đến 4 trong menu chưa được bấm thử trên máy đó (`phan_tich.py` và `web.py` thì đã chạy được riêng bằng Python). Nếu báo lỗi, chụp cửa sổ gửi lại. Phần dưới là cách chạy tay từng lệnh.

---

Notebook trong `notebooks/` chỉ để minh họa từng bước. Phần code chính của dự án nằm trong `src/`, chạy bằng dòng lệnh. Tất cả lệnh dưới đây chạy ở thư mục gốc dự án (`BaiTapTuan5`).

## Chạy tay: 0. Cài đặt một lần
Cần Python 3.10 trở lên. Mở Terminal (hoặc PowerShell) trong thư mục dự án:

```
python -m venv .venv
.venv\Scripts\activate          # Windows. Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```
`requirements.txt` có gói `tabicl` (kéo theo PyTorch, nặng, vài GB). Nếu chỉ chạy bước 1 và 2 thì có thể bỏ dòng `tabicl` trước khi cài.

## 1. Phân tích: `src/phan_tich.py`
```
python src/phan_tich.py
```
Làm gì: thống kê mô tả, vẽ biểu đồ, Hồi quy Logistic tự cài bằng Gradient Descent (đối chiếu với sklearn), thí nghiệm tốc độ học và chuẩn hóa, bốn cấu hình A, B1, B, C, ngưỡng, attention minh họa.
Kết quả: bảng trong `results/tables/`, hình trong `results/figures/`. Chạy mất khoảng 15 giây. Seed cố định 42, chạy lại ra đúng số cũ.
Dấu hiệu chạy đúng: có dòng khớp sklearn (lệch tối đa khoảng 0,0005) và các tệp mới xuất hiện trong `results/`.

## 2. Dựng báo cáo Word: `src/viet_bao_cao.py`
```
python src/viet_bao_cao.py
```
Đọc các bảng và hình trong `results/` rồi tạo lại `report/BaoCao_TabICLv2_BoHoc.docx`.
**Cẩn thận:** lệnh này ghi đè file Word. Mọi chỗ bạn đã sửa tay trong Word sẽ mất. Muốn có tên thành viên và giảng viên trên bìa thì điền vào hai biến `THANH_VIEN` và `GIANG_VIEN` ở đầu file `src/viet_bao_cao.py` rồi mới chạy. Nếu đã sửa tay trong Word rồi thì đừng chạy lại lệnh này.

## 3. TabICLv2: `src/chay_tabicl.py`
```
python src/chay_tabicl.py
```
Cần internet (lần đầu tự tải trọng số từ HuggingFace), nên có GPU nếu được. Nên chạy sau bước 1 vì cần `results/tables/split_seed42.json`.
Làm gì: chạy TabICLv2 cho bốn cấu hình, rồi khảo sát kích thước ngữ cảnh (50, 200, 800, toàn bộ) và số thành viên ensemble (1 và 8) ở cấu hình B.
Kết quả: `results/tables/tabicl_khao_sat.csv` (không ghi đè `tabicl_ketqua.csv`, là kết quả đã dùng trong báo cáo).
Lưu ý: script này **chưa từng được chạy thử** (nhưng cùng cách gọi `TabICLClassifier` đã chạy được trong notebook 05). Nếu báo lỗi tên tham số, gửi tôi dòng lỗi.

## Thứ tự gợi ý
`phan_tich.py` → (xem kết quả trong `results/`) → `chay_tabicl.py` → điền tên → `viet_bao_cao.py`.

## Hay gặp lỗi
- `ModuleNotFoundError`: chưa kích hoạt `.venv` hoặc chưa `pip install -r requirements.txt`.
- `FileNotFoundError: data/data.csv`: chưa chạy ở thư mục gốc dự án, hoặc thiếu `data/data.csv`.
- Không tải được trọng số TabICLv2: kiểm tra mạng, hoặc dùng notebook 05 trên Colab.
