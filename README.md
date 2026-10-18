# Bài tập tuần 5: dự đoán nguy cơ sinh viên bỏ học

Môn Cơ sở Toán học cho Trí tuệ nhân tạo. Đề tài: nghiên cứu cơ sở toán học của mô hình TabICLv2 và ứng dụng dự đoán nguy cơ sinh viên bỏ học (giáo dục).

Ý tưởng một câu: mỗi sinh viên được mô tả bằng 8 chỉ số; mô hình đoán xác suất em đó bỏ học. Tốt nghiệp là nhóm an toàn (y = 0), bỏ học là nhóm nguy cơ (y = 1), đang học thì loại ra vì chưa có kết cục.

## Bắt đầu từ đâu

| Muốn | Mở |
|---|---|
| Hiểu từng bước để thuyết trình | `docs/TOM_TAT_NOI_DUNG.md` (hiểu toàn bộ dự án) và `notebooks/01` đến `06` (demo trên Google Colab) |
| Chạy code | bấm đúp `run.bat` (tự cài, chạy, mở web), hoặc xem `docs/HUONG_DAN_CHAY_CODE.md` |
| Luyện trả lời thầy | `docs/HoiDap_Thay.md` |
| Nộp báo cáo Word | `report/BaoCao_TabICLv2_BoHoc.docx` |
| Trình bày | `docs/KICH_BAN_THUYET_TRINH.md` (kịch bản nói, khớp file `slides/Bài thuyết trình (đã sửa) - thêm chú thích.pptx`, 16 trang) |

## Cấu trúc

```
BaiTapTuan5/
  README.md            tệp này
  CLAUDE.md            yêu cầu, quyết định và tiến độ (cho Claude Code)
  requirements.txt     thư viện Python
  run.bat              bấm đúp: tự cài Python/thư viện, chạy, mở trang web kết quả
  data/                data.csv (dấu phân cách ;)
  notebooks/           01 đến 06, mỗi notebook một nhiệm vụ; ban_khac/ là notebook khác của nhóm
  src/                 phan_tich.py, chay_tabicl.py, viet_bao_cao.py, web.py
  results/tables/      CSV, JSON do code sinh ra
  results/figures/     hình PNG do code sinh ra
  report/              BaoCao_TabICLv2_BoHoc.docx
  slides/              liên kết bộ slide
  docs/                de_bai_cua_thay.docx, TOM_TAT_NOI_DUNG.md, HUONG_DAN_CHAY_CODE.md, KICH_BAN_THUYET_TRINH.md, HoiDap_Thay.md
```

## Cách chạy

Cài một lần: `pip install -r requirements.txt`

1. `python src/phan_tich.py` thống kê, biểu đồ, Hồi quy Logistic tự cài bằng Gradient Descent, attention minh họa. Ghi vào `results/`. Hạt giống 42, chạy lại ra đúng kết quả cũ.
2. `python src/viet_bao_cao.py` dựng lại báo cáo Word từ `results/`.
3. TabICLv2 đã chạy qua notebook 05. `python src/chay_tabicl.py` là bản dòng lệnh (khảo sát thêm kích thước ngữ cảnh, số ensemble), cần internet, chưa chạy thử.
4. Notebook: mở từng tệp 01 đến 06 trên Google Colab (mỗi tệp chạy độc lập), chọn `data.csv` khi được hỏi. Trên máy cá nhân, đặt `data/data.csv` rồi chạy trong thư mục gốc dự án.

## Trạng thái

| Phần | Trạng thái |
|---|---|
| Thống kê, biểu đồ, Hồi quy Logistic tự cài (khớp sklearn, lệch tối đa 0,0005) | Xong |
| Notebook Colab từng bước | Xong, đã chạy thử |
| Báo cáo Word 8 mục + 2 phụ lục (giải thích từ số 0, thuật ngữ) | Xong, còn tên thành viên và giảng viên ở bìa |
| Slide 16 trang, có kịch bản nói | Xong, còn `[tên nhóm]` |
| **TabICLv2 thật** | Đã chạy trên Colab (notebook 05), bốn cấu hình, kết quả trong `results/tables/tabicl_ketqua.csv` và mục 7.5 của Word. Mới một lần chạy, một lần chia; `chay_tabicl.py` vẫn chưa chạy thử |

## Nguồn

- Dữ liệu: Predict Students' Dropout and Academic Success, UCI, DOI 10.24432/C5MC89. https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success
- Mô hình: Qu, Holzmüller, Varoquaux, Le Morvan (2026), TabICLv2, ICML 2026. https://proceedings.mlr.press/v306/qu26a.html ; mã nguồn https://github.com/soda-inria/tabicl
