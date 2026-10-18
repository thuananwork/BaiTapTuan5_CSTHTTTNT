# CLAUDE.md: Bài tập tuần 5, môn "Cơ sở Toán học cho Trí tuệ nhân tạo"

Đọc kỹ tệp này trước khi viết bài, viết code hoặc trả lời bất cứ điều gì trong thư mục BaiTapTuan5. Đây là bài tập tuần 5, tách riêng với đồ án cuối kỳ (họ CCA, nằm ở `../DoAnMonHoc/CLAUDE.md`). Đừng trộn hai đề tài.

## 1. Người dùng và bối cảnh
- Người làm: Nguyễn Thuận An, học viên cao học CNTT, làm NLP, có dạy học sinh. An phải tự trình bày lại cho thầy, nên giải thích phải dễ hiểu cho người mới học.
- Đề bài nằm trong tệp `docs/de_bai_cua_thay.docx` (tên tệp gợi ý bài nhóm; chưa xác nhận là nhóm hay cá nhân).
- Thời hạn rất gấp: khoảng 2 giờ, tính từ sáng 18/10/2026. Ưu tiên ra bài viết đủ ý trước, trau chuốt sau.

## 2. Đề bài tóm tắt (từ `docs/de_bai_cua_thay.docx`)
Chủ đề: phân tích và ứng dụng cơ sở toán học trong xây dựng mô hình AI. Chọn một bài toán thực tế và một bộ dữ liệu thật, rồi giải thích toán ở toàn bộ quy trình. Tám mục bắt buộc:
- 2.1 Phát biểu và mô hình hóa bài toán (đầu vào, đầu ra, không gian đặc trưng, mục tiêu tối ưu, ràng buộc).
- 2.2 Thống kê mô tả (trung bình, trung vị, phương sai, phân vị; tần suất biến định tính; phân bố lớp; thiếu, ngoại lệ, mất cân bằng, thang đo; tương quan; bảng và biểu đồ).
- 2.3 Đại số tuyến tính (vector, ma trận, tích vô hướng, chuẩn, khoảng cách, độ tương đồng, phân rã nếu có; ít nhất một ví dụ tính tay gắn với thuật toán).
- 2.4 Giải tích và hàm mất mát (đạo hàm, gradient, quy tắc dây chuyền; quan hệ giữa cực tiểu hóa mất mát và việc học).
- 2.5 Thuật toán tối ưu (công thức cập nhật, tốc độ học, hội tụ, tiêu chuẩn dừng; **thực nghiệm thay đổi ít nhất một yếu tố của quá trình tối ưu**).
- 2.6 Xác suất thống kê (phân phối, kỳ vọng, xác suất có điều kiện, ước lượng tham số; chia train/test; overfitting, underfitting, tổng quát hóa).
- 2.7 Xây dựng mô hình và thực nghiệm (tiền xử lý có cơ sở toán; Python; độ đo có công thức; **ít nhất hai cấu hình** để thấy ảnh hưởng của một thành phần toán học; bảng, biểu đồ, nhận xét có căn cứ).
- 2.8 Thảo luận và kết luận (vai trò từng mảng toán, giải thích kết quả bằng toán, hạn chế và giả định).

Yêu cầu chung: dữ liệu thật có nguồn rõ; công thức nào cũng phải giải thích ký hiệu, ý nghĩa, vai trò; không trình bày lý thuyết rời rạc; phần toán nào không dùng trực tiếp thì nói rõ vì sao; khuyến khích tự tính lại một số bước để đối chiếu với thư viện. Mục tiêu là chiều sâu hiểu toán, không phải độ phức tạp hay độ chính xác.

## 3. Ý của thầy (luôn bám)
- **Đi từ bài toán gốc ra vấn đề.** Mỗi mảng toán phải xuất hiện vì bài toán buộc phải có nó, không phải vì đề liệt kê. Chỉ quan tâm số liệu thật sự cần cho thuật toán.
- **Hiểu là chính, code không quan trọng.** Code chỉ để chạy ra vài bảng và biểu đồ minh họa.
- **Ví dụ trò chơi dò mìn của thầy:** phải định nghĩa rõ thành công và thất bại ngay từ đầu. Nhấn trúng ô an toàn là đạt mục tiêu; trúng mìn là thất bại. Mô hình phải đoán ô nào có mìn *trước khi* nhấn.

## 4. Đề tài đã chốt
**"Nghiên cứu cơ sở toán học của mô hình TabICLv2 và ứng dụng dự đoán nguy cơ sinh viên bỏ học."**

### 4.1 Dữ liệu
**Predict Students' Dropout and Academic Success** (Realinho, Martins, Machado, Baptista; tạp chí *Data*, 2022).
- UCI (nguồn chính thức, trích dẫn bản này): https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success
- Bản sao trên Kaggle: https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention (chưa mở trực tiếp để kiểm tra link).
- Viện Bách khoa Portalegre (Bồ Đào Nha), 17 ngành đại học, 2008 đến 2019. 4.424 sinh viên, 36 đặc trưng, không có giá trị thiếu.
- Nhãn `Target`: Dropout 1.421, Enrolled 794, Graduate 2.209 (số lớp lấy theo arXiv 2310.10987; kiểm tra lại khi tải dữ liệu).

### 4.2 Ánh xạ nhãn (đề của thầy nhắc ví dụ dò mìn; slide và báo cáo hiện KHÔNG dùng ẩn dụ này, người dùng đã yêu cầu bỏ)
- **Trúng mìn** là Dropout (bỏ học), y = 1. **Ô an toàn** là Graduate (tốt nghiệp), y = 0.
- **Enrolled là ô chưa lật:** các em còn đang học, chưa biết kết cục, nên loại khỏi bài toán. Còn 3.630 sinh viên, khoảng 39% là mìn (hơi mất cân bằng).
- Bỏ sót một em sắp bỏ học (FN) đắt hơn báo nhầm (FP), nên độ đo quan trọng nhất là **Recall của lớp Dropout**. Accuracy một mình dễ đánh lừa.

### 4.3 Số liệu cần cho thuật toán (bộ đặc trưng gọn)
- Tài chính: `Tuition fees up to date`, `Debtor`, `Scholarship holder`.
- Học lực năm nhất: `Curricular units 1st sem (approved)`, `(grade)`, `Curricular units 2nd sem (approved)`, `(grade)`.
- Hoàn cảnh: `Age at enrollment`.
Các cột vĩ mô (GDP, lạm phát, thất nghiệp) và mã nghề bố mẹ tạm bỏ, kèm lý do: không cần để trả lời câu hỏi gốc. Đề cho phép nêu lý do không dùng.

### 4.4 Mô hình TabICLv2
- Bài gốc: Qu, Holzmüller, Varoquaux, Le Morvan (INRIA Saclay), *TabICLv2: A Better, Faster, Scalable, and Open Tabular Foundation Model*, ICML 2026, PMLR 306:102477–102555. arXiv: https://arxiv.org/abs/2602.11139 ; PMLR: https://proceedings.mlr.press/v306/qu26a.html
- Code: https://github.com/soda-inria/tabicl (`pip install tabicl`, lớp `TabICLClassifier`, checkpoint mặc định `tabicl-classifier-v2-20260212.ckpt`, tham số `n_estimators` mặc định 8, chạy được trên CPU). Bản cài đặt giáo dục ngắn: https://github.com/soda-inria/nanotabicl
- Phạm vi tiền huấn luyện: khoảng 300 đến 48K mẫu, 2 đến 100 cột. Bộ dữ liệu này (3.630 mẫu, ≤ 36 cột) nằm gọn trong phạm vi.

Lõi của TabICLv2 (theo bài gốc, cần đối chiếu khi viết chính thức):
1. **Nhúng theo cột** (set transformer TF_col): mỗi đặc trưng thành vector; có gom nhóm đặc trưng lặp bằng dịch vòng.
2. **Tương tác theo hàng** (transformer TF_row với token [CLS]): gộp mỗi sinh viên thành một vector.
3. **Học trong ngữ cảnh theo tập dữ liệu** (TF_icl): hàng cần dự đoán "chú ý" vào các hàng huấn luyện đã có nhãn. Nhãn được cộng vào biểu diễn hàng huấn luyện (target-aware embedding).
4. **QASSMax:** softmax có tỉ lệ theo log n (n là số mẫu ngữ cảnh) và cổng phụ thuộc truy vấn, để attention không bị "loãng" khi ngữ cảnh rất dài.
5. **Tiền huấn luyện** trên dữ liệu tổng hợp với mục tiêu PFN: cực tiểu kỳ vọng của −log q_θ(y_test | x_test, D_train), tức cross-entropy. Tối ưu bằng **Muon** thay cho AdamW.
6. **Suy luận:** một lượt lan truyền thuận, **không cập nhật trọng số** trên dữ liệu của mình. Độ phức tạp O(n² + n·m²).

### 4.5 Gắn từng mục đề với TabICLv2 và cách xử lý điểm khó
- **2.3 Đại số tuyến tính:** sinh viên thành vector, cả lớp thành ma trận; Q = XW_Q, K = XW_K, V = XW_V; điểm tương đồng là tích vô hướng q·k. Ví dụ tính tay: một đầu attention trên 3–4 sinh viên.
- **2.4 Giải tích:** softmax, cross-entropy, gradient và quy tắc dây chuyền qua các lớp transformer (diễn ra lúc tiền huấn luyện).
- **2.5 Tối ưu, điểm khó nhất:** TabICLv2 không huấn luyện lại trên dữ liệu của mình, nên không thể thay đổi tốc độ học của Muon. Hướng xử lý:
  1. Trình bày Muon và mục tiêu PFN ở mức nguyên lý (đề cho phép với phương pháp tối ưu "thực tế được sử dụng").
  2. Thực nghiệm tối ưu trên một **mô hình đối chứng nhỏ, tự cài bằng NumPy**: Hồi quy Logistic + Gradient Descent trên cùng dữ liệu. Thử 3 tốc độ học, vẽ đường loss. Phép tính này cũng là "tự xây dựng bước cập nhật để kiểm chứng" mà đề khuyến khích.
  3. Với TabICLv2, thay đổi các yếu tố lúc suy luận: kích thước ngữ cảnh (số mẫu huấn luyện đưa vào) và `n_estimators`.
  Ghi rõ cách xử lý này trong bài, không giấu.
- **2.6 Xác suất:** đầu ra là P(bỏ học | x, D_train), một xác suất có điều kiện theo cả tập huấn luyện. Mục tiêu PFN là xấp xỉ suy luận Bayes trên một prior tổng hợp. Chia train/test 80/20 phân tầng; ở đây "học" là đưa train vào ngữ cảnh.
- **Ý dò mìn gắn với attention:** attention giống người chơi nhìn các ô hàng xóm đã lật. Sinh viên mới được so với những sinh viên cũ giống mình nhất, rồi "bỏ phiếu có trọng số" theo kết cục của họ.
- **2.7 Cấu hình thực nghiệm (ít nhất hai):**
  - Bộ đặc trưng gọn (khoảng 8 cột) so với đủ 36 cột.
  - Chỉ dữ liệu lúc nhập học so với thêm kết quả năm nhất: cảnh báo sớm nhưng kém chính xác, hay muộn nhưng chính xác hơn.
  - Kích thước ngữ cảnh khác nhau.
  - Mô hình đối chứng (Logistic Regression) so với TabICLv2.
  - Độ đo: Accuracy, Precision, Recall, F1 (nhấn mạnh Recall lớp Dropout), ROC-AUC, ma trận nhầm lẫn.
- **2.8 Hạn chế cần nêu:** mô hình là "hộp đen" khó diễn giải hơn Logistic Regression; dựa vào prior tổng hợp; không tinh chỉnh trên dữ liệu thật; dữ liệu chỉ từ một trường ở Bồ Đào Nha.

## 5. Quy tắc khi viết bài
- Tiếng Việt tự nhiên như người nói, giải thích như cho người mới học. Công thức chỉ bổ trợ, lời giải thích là chính. Hạn chế gạch đầu dòng trong phần giải thích.
- Bài đi theo mạch "từ bài toán gốc ra vấn đề": vấn đề ngoài đời → định nghĩa mìn → số liệu cần → biểu diễn bằng số → toán xuất hiện từng bước → kiểm tra trên "bàn mới" → đánh giá theo cái giá của việc bỏ sót.
- Không bịa số liệu, link hay kết quả. Việc chưa chạy hoặc chưa mở thì nói rõ. Số liệu ví dụ tự lập phải ghi là tự lập.
- Khi viết bài chính thức, nhắc đối chiếu công thức với bài gốc TabICLv2.
- Nếu yêu cầu chưa rõ, nêu giả định ngắn gọn rồi làm tiếp.

## 6. Quy tắc khi viết code (tối giản)
- Code chỉ phục vụ minh họa: thống kê mô tả, biểu đồ, bảng kết quả.
- Đặt seed cố định, cùng một cách chia train/test cho mọi cấu hình.
- Tự cài Logistic Regression bằng Gradient Descent và một đầu attention bằng NumPy; đối chiếu với sklearn.
- Lưu bảng vào `results/tables/` và hình vào `results/figures/`; bài viết chỉ trích số từ các tệp này.
- Không cài thêm gói hay tải dữ liệu lớn khi chưa nói trước (`tabicl` cần PyTorch và tự tải checkpoint lần đầu).

## 7. Đã chốt và tiến độ (cập nhật 18/10/2026)
- Bài **nhóm** (tên thành viên, giảng viên: còn để trống ở trang bìa Word và slide). Đầu ra: **Word theo 8 mục + slide** (14 slide, làm bằng loại Slides trên claude.ai).
- Dữ liệu: `data/data.csv` (dấu phân cách `;`, 4.424 dòng, 36 cột, đã kiểm tra khớp số lớp: Graduate 2.209, Dropout 1.421, Enrolled 794).
- Đã làm xong (xem README.md): `src/phan_tich.py` (thống kê, biểu đồ, Logistic tự cài, attention minh họa), `src/viet_bao_cao.py` (dựng Word), `report/BaoCao_TabICLv2_BoHoc.docx`, kết quả trong `results/`.
- **TabICLv2 đã chạy thật** (xem mục 8). `src/chay_tabicl.py` vẫn chưa chạy thử. Đừng bao giờ ghi kết quả TabICLv2 không có số thật.
- Mọi số liệu thực nghiệm hiện có đến từ Hồi quy Logistic đối chứng và attention tự viết (đã ghi rõ trong bài, không phải TabICLv2).
- Điều đã phát hiện cần giữ trong bài: điểm HK2 phần nào chứa sẵn đáp án (90,6% em có điểm HK2 = 0 đã bỏ học), nên cảnh báo sớm thật sự dùng cấu hình B1 (hết HK1); hai cột môn qua HK1/HK2 tương quan 0,92 gây trọng số HK1 dương khó đọc.

## 8. Cấu trúc thư mục (chuẩn hóa lại 18/10/2026)

```
BaiTapTuan5/
  README.md, CLAUDE.md, requirements.txt
  data/data.csv
  notebooks/01..06_*.ipynb           # 6 notebook Colab, mỗi cái một nhiệm vụ (đã chạy thử, trừ ô TabICLv2)
  notebooks/ban_khac/                # notebook khác của nhóm (3 lớp, mô phỏng numpy, không phải TabICLv2 thật)
  src/phan_tich.py, chay_tabicl.py, viet_bao_cao.py
  results/tables/, results/figures/
  report/BaoCao_TabICLv2_BoHoc.docx  # 8 mục + Phụ lục A (TabICLv2 từ số 0), B (thuật ngữ), C (chạy lại)
  slides/README.md                   # liên kết slide 16 trang, có kịch bản nói
  docs/de_bai_cua_thay.docx, TOM_TAT_NOI_DUNG.md, HUONG_DAN_CHAY_CODE.md, KICH_BAN_THUYET_TRINH.md, HoiDap_Thay.md
```

Tiến độ TabICLv2: đã chạy thật qua notebook 05 (Colab, tabicl 2.2.0, n_estimators=8, toàn bộ tập huấn luyện làm ngữ cảnh). Accuracy A/B1/B/C = 75,6/87,9/91,3/94,6%; AUC = 0,823/0,934/0,955/0,977; cao hơn Logistic ở AUC nhưng chênh Accuracy 0,1 đến 1,4 điểm, nhỏ hơn sai số ±2,2. Kết quả ở `results/tables/tabicl_ketqua.csv` và mục 7.5 Word. Chưa làm: khảo sát kích thước ngữ cảnh và n_estimators (cần `src/chay_tabicl.py`, chưa chạy thử), kiểm tra chéo.

Còn việc: điền tên thành viên, giảng viên ở bìa Word; Share slide; đối chiếu mô tả TabICLv2/Muon với bài gốc.
