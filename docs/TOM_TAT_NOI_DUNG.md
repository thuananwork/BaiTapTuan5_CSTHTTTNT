# Tóm tắt nội dung chính

**Đề tài:** Nghiên cứu cơ sở toán học của mô hình TabICLv2 và ứng dụng dự đoán nguy cơ sinh viên bỏ học. Môn Cơ sở Toán học cho Trí tuệ nhân tạo. Nhóm 6. Lĩnh vực giáo dục.

## 1. Bài toán
- Mỗi sinh viên được mô tả bằng 8 chỉ số, mô hình đoán xác suất em đó bỏ học.
- Nhóm an toàn = tốt nghiệp (y = 0). Nhóm nguy cơ = bỏ học (y = 1). Đang học (794 em) bị loại khỏi bài toán vì chưa có kết cục.
- Việc của mô hình: nhìn các chỉ số của một sinh viên và đoán em đó có bỏ học không, trước khi chuyện xảy ra.
- Đầu ra là một xác suất bỏ học để nhà trường tự chọn mức báo động.
- Đây là bài toán phân loại nhị phân. Độ đo quan trọng nhất là Recall của lớp bỏ học, vì bỏ sót một em đắt hơn báo nhầm.

## 2. Dữ liệu
- Nguồn: UCI, "Predict Students' Dropout and Academic Success" (Realinho và cộng sự, Bồ Đào Nha, 2008 đến 2019). 4.424 sinh viên, 36 cột, không thiếu giá trị.
- Sau khi bỏ nhóm đang học: 3.630 em, 39,1% bỏ học. Đoán lười "ai cũng an toàn" vẫn đúng 61% mà không phát hiện được em bỏ học nào, nên không chỉ nhìn Accuracy.
- Giữ 8 chỉ số: đóng học phí đủ hạn, đang nợ, có học bổng, tuổi lúc nhập học, số môn qua và điểm học kỳ 1, số môn qua và điểm học kỳ 2. Các cột khác (nghề nghiệp bố mẹ, GDP, lạm phát...) để ngoài vì câu hỏi gốc không cần.
- Dữ liệu nói gì: chưa đóng đủ học phí bỏ học 94% so với 31%; đang nợ 76% so với 34%; có học bổng 14% so với 48%. Đây là tương quan, không phải nhân quả.
- Điểm học kỳ 2 bằng 0 có 802 em, 90,6% đã bỏ học, nên dữ liệu học kỳ 2 phần nào chứa sẵn đáp án.

## 3. Đại số tuyến tính: biến sinh viên thành số
- Vector: một sinh viên là dãy 8 số. Ma trận: cả lớp là bảng 3.630 × 8.
- Tích vô hướng: nhân từng chỉ số với trọng số rồi cộng, được "mức nguy hiểm" z = w₁x₁ + … + w₈x₈ + b. Trọng số lớn nghĩa là chỉ số đó nặng ký.
- Chuẩn hóa z-score để tuổi (17 đến 70) không lấn át cột chỉ có 0 và 1. Trung bình và độ lệch chuẩn chỉ tính trên tập huấn luyện để tránh rò rỉ dữ liệu.
- Số điều kiện (tỉ số trị riêng lớn nhất trên nhỏ nhất của XᵀX/n): 67 khi có chuẩn hóa, 30.622 khi không.
- Không dùng PCA hay SVD vì chỉ có 8 đặc trưng.

## 4. Xác suất và hàm mất mát
- Sigmoid p = 1/(1 + e^(−z)) đổi mức nguy hiểm thành xác suất từ 0 đến 1.
- Cross-entropy phạt −ln p nếu thật sự bỏ học, −ln(1−p) nếu thật sự an toàn. Đoán 0,99 mà sai bị phạt 4,605, đoán đúng chỉ 0,010, chênh hơn 400 lần.
- Cực tiểu hóa cross-entropy chính là làm dữ liệu thật có khả năng xảy ra cao nhất (ước lượng hợp lý cực đại).
- Mô hình không biết gì (luôn đoán 0,5) có mất mát 0,693 = ln 2.

## 5. Gradient và tối ưu
- Gradient là "la bàn" chỉ chiều làm mất mát tăng nhanh nhất; ta đi ngược lại. Nhờ quy tắc dây chuyền, gradient rất gọn: ∇L = Xᵀ(p − y)/n. Cập nhật: w ← w − η·∇L.
- Tốc độ học η nhỏ quá thì đi mãi, lớn quá thì nhảy qua đáy và có thể phân kỳ. Hàm là lồi nên chỉ có một đáy.
- Bản tự cài khớp sklearn, lệch tối đa 0,0005.
- Thí nghiệm đổi tốc độ học (0,001; 0,01; 0,1; 1,0), có và không chuẩn hóa: có chuẩn hóa, η = 1 chỉ cần 145 vòng tới sát đáy; không chuẩn hóa, η = 0,1 dao động còn η = 1 phân kỳ (mất mát gần 10, Accuracy 74%).
- Giải thích bằng toán: tốc độ học an toàn tối đa ≈ 2,17 khi có chuẩn hóa so với ≈ 0,009 khi không. Lý thuyết khớp thực nghiệm.
- Thí nghiệm làm trên Hồi quy Logistic vì TabICLv2 không huấn luyện lại trên dữ liệu của mình.

## 6. Chia dữ liệu và thống kê
- Chia 80/20 có phân tầng, seed 42: huấn luyện 2.904 em, kiểm tra 726 em.
- Accuracy huấn luyện 0,879, kiểm tra 0,899, không thấy dấu hiệu học vẹt.
- Sai số chuẩn của Accuracy ≈ 1,1 điểm, khoảng tin cậy 95% ≈ ±2,2 điểm. Hai cấu hình chênh dưới 2 điểm thì chưa kết luận được.

## 7. TabICLv2 (Qu, Holzmüller, Varoquaux, Le Morvan, ICML 2026)
- Học trong ngữ cảnh: mô hình đã học trước một lần trên rất nhiều bảng giả lập. Khi dùng, chỉ đưa các em đã biết kết cục làm ngữ cảnh, đoán em mới trong một lượt tính, không đổi trọng số.
- Attention gồm ba bước: so sánh em mới với từng em cũ, softmax đổi điểm giống nhau thành trọng số cộng bằng 1, rồi bỏ phiếu có trọng số. Ví dụ điểm 2, 1, 0, 0 cho trọng số 0,61 · 0,22 · 0,08 · 0,08; hai em đầu bỏ học thì P = 0,83.
- Q (truy vấn), K (khóa), V (giá trị) sinh từ ma trận học được: softmax(QKᵀ/√d)·V.
- Ba tầng: nhúng theo cột, gộp theo hàng, học trong ngữ cảnh theo cả bảng. QASSMax giữ sự chú ý tập trung khi ngữ cảnh dài.
- Huấn luyện trước trên dữ liệu giả lập từ mô hình nhân quả ngẫu nhiên, mục tiêu cross-entropy, bộ tối ưu Muon (thay AdamW, chỉ dùng lúc huấn luyện trước).
- Ví dụ attention tính tay trên dữ liệu thật của nhóm: bốn em đã biết (0;0) bỏ học 0,42, (6;6) an toàn 0,04, (2;1) bỏ học 0,44, (5;5) an toàn 0,10; em cần đoán qua (1;1) có P(bỏ học) ≈ 0,87, đúng với kết cục thật. Đây là bản minh họa tự viết, không phải TabICLv2.
- Kết quả TabICLv2 thật (notebook 05, tabicl 2.2.0, 8 ensemble, toàn bộ tập huấn luyện làm ngữ cảnh), Accuracy / Recall / AUC: A 75,6% / 62,7% / 0,823; B1 87,9% / 82,0% / 0,934; B 91,3% / 86,6% / 0,955; C 94,6% / 91,9% / 0,977. So với Hồi quy Logistic: AUC cao hơn ở cả bốn cấu hình, nhưng chênh Accuracy 0,1 đến 1,4 điểm, nhỏ hơn sai số ±2,2, và mới một lần chia nên chưa kết luận chính xác hơn. Mô tả TabICLv2 tóm tắt từ bài gốc, cần đối chiếu.

## 8. Kết quả (Hồi quy Logistic đối chứng)
- A. Lúc nhập học (8 cột): Accuracy 75,1%, Recall 58,1%, AUC 0,815
- B1. Đến hết học kỳ 1 (6 cột): 87,5%, 80,6%, 0,914
- B. Đến hết học kỳ 2 (8 cột): 89,9%, 85,6%, 0,940
- C. Đầy đủ 35 cột: 94,5%, 92,3%, 0,973
- Biết càng nhiều càng phát hiện được nhiều em bỏ học nhưng càng muộn. Cảnh báo sớm thật sự dùng B1 vì học kỳ 2 chứa sẵn đáp án.

## 9. Đổi ngưỡng báo động (cấu hình B)
- Ngưỡng 0,5: bỏ sót 41 em, báo nhầm 32 em, Recall 85,6%.
- Ngưỡng 0,3: bắt 91,5% em bỏ học, bỏ sót 24, báo nhầm 71.
- Báo nhầm chỉ tốn một buổi gặp mặt, bỏ sót là mất một sinh viên. Chọn ngưỡng là quyết định của nhà trường, không phải của thuật toán.
- AUC không đổi (0,940) khi đổi ngưỡng.

## 10. Kết luận
Trả lời bốn câu hỏi của đề:
1. Mô hình hóa: phân loại nhị phân, sinh viên là vector 8 chiều, đầu ra là xác suất bỏ học.
2. Toán quyết định cách hoạt động: đại số tuyến tính (biểu diễn), giải tích (đo sai, chỉ hướng sửa), tối ưu (tìm tham số), xác suất thống kê (tin được trên dữ liệu mới).
3. Học tham số: cực tiểu hóa cross-entropy bằng Gradient Descent; TabICLv2 học trước bằng Muon.
4. Giải thích kết quả: số điều kiện giải thích vì sao phải chuẩn hóa; ngưỡng giải thích cân bằng giữa bỏ sót và báo nhầm.

Hạn chế: TabICLv2 mới chạy một lần, cấu hình mặc định; điểm học kỳ 2 chứa sẵn đáp án; hai cột "môn qua" tương quan 0,92; chỉ chia dữ liệu một lần, chưa kiểm tra chéo.

Câu chốt: đoán đúng hay sai chưa đáng giá bằng việc biết cái giá của từng kiểu sai.

## Nguồn
- Realinho và cộng sự (2022). Predicting Student Dropout and Academic Success. UCI, DOI 10.24432/C5MC89.
- Qu, Holzmüller, Varoquaux, Le Morvan (2026). TabICLv2. ICML 2026, PMLR 306:102477–102555; arXiv 2602.11139; github.com/soda-inria/tabicl.
