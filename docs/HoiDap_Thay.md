# Hỏi đáp: những câu thầy có thể hỏi

Trả lời ngắn, nói bằng lời của mình. Số liệu lấy từ `results/tables/` và notebook. Câu hỏi sắp theo thứ tự bài.

## Bài toán và dữ liệu
**Vì sao loại nhóm Enrolled (đang học)?** Họ chưa có kết cục, giống ô chưa lật. Đưa vào thì mô hình học từ nhãn chưa có kết luận.

**Dữ liệu lệch 39/61 có sao không?** Lệch nhưng chưa nặng. Điều cần tránh là chỉ nhìn Accuracy, vì luôn đoán "an toàn" đã đúng khoảng 61%. Ta nhìn Recall của lớp bỏ học.

**Sao chỉ dùng 8 cột?** Đó là những chỉ số có lý do giáo dục rõ (tiền bạc, học lực, tuổi) và đủ để trả lời câu hỏi gốc. Nhóm có thử cả 35 cột ở cấu hình C để so sánh.

**Tương quan có phải nhân quả không?** Không. Nợ học phí đi cùng bỏ học, nhóm không khẳng định nợ gây ra bỏ học.

**Điểm học kỳ 2 bằng 0 nghĩa là gì?** Phần lớn (khoảng 91%) là em đã bỏ học, nên dữ liệu học kỳ 2 phần nào chứa sẵn đáp án. Cảnh báo sớm thật sự dựa vào cấu hình B1 (đến hết học kỳ 1).

## Đại số tuyến tính
**Vì sao phải chuẩn hóa?** Để các cột cùng thang đo, và quan trọng hơn là để Gradient Descent chạy ổn: số điều kiện giảm từ khoảng 30.622 xuống khoảng 67.

**Vì sao chuẩn hóa chỉ dùng trung bình và độ lệch chuẩn của tập huấn luyện?** Nếu dùng cả tập kiểm tra thì thông tin của nó rò vào lúc huấn luyện (rò rỉ dữ liệu) và điểm bị đẹp giả.

**Tích vô hướng nghĩa là gì?** Nhân từng cặp chỉ số với trọng số rồi cộng: bỏ phiếu có trọng số của các chỉ số.

**Vì sao không dùng PCA hay SVD?** Chỉ có 8 đặc trưng và mô hình không cần giảm chiều. Đề cho phép nêu rõ phần toán không dùng.

**Số điều kiện, trị riêng liên quan gì?** Trị riêng của XᵀX/n cho biết độ dốc theo từng hướng; số điều kiện là tỉ số lớn nhất trên nhỏ nhất. Tốc độ học an toàn nhỏ hơn 2/L với L không vượt quá một phần tư trị riêng lớn nhất.

## Xác suất và hàm mất mát
**Vì sao cross-entropy, không dùng bình phương sai số?** Nó sinh ra từ ước lượng hợp lý cực đại (mô hình Bernoulli), phạt nặng sự tự tin sai, và cùng sigmoid cho gradient gọn (p − y).

**Sigmoid để làm gì?** Biến mức nguy hiểm tùy ý thành xác suất từ 0 đến 1.

**Mức phạt −ln p nghĩa là gì?** Độ "ngạc nhiên" của mô hình khi thấy kết cục thật. Đoán 0,99 mà sai bị phạt 4,6 so với 0,01 khi đúng, hơn 400 lần.

## Tối ưu
**Gradient là gì?** Vector các đạo hàm riêng, chỉ chiều làm hàm tăng nhanh nhất; ta đi ngược lại.

**Tốc độ học quá lớn thì sao?** Nhảy qua đáy, nếu vượt 2/L thì càng nhảy càng cao và phân kỳ. Trong thí nghiệm: không chuẩn hóa, η = 1 làm mất mát lên gần 10 và độ chính xác tụt còn 74%.

**Vì sao hàm này chỉ có một đáy?** Cross-entropy của Hồi quy Logistic là hàm lồi theo tham số. Mạng sâu như Transformer thì không lồi.

**Tiêu chuẩn dừng?** Mất mát giảm ít hơn 10⁻¹² giữa hai vòng, hoặc hết số vòng tối đa.

**Sao thí nghiệm tối ưu không làm trên TabICLv2?** TabICLv2 không huấn luyện lại trên dữ liệu của mình (đã học trước một lần bằng Muon). Nhóm nói thẳng và làm thí nghiệm trên Hồi quy Logistic.

## Xác suất, thống kê
**Vì sao giấu một phần dữ liệu?** Để có ước lượng không lạc quan về chất lượng trên dữ liệu chưa thấy.

**Làm sao biết quá khớp?** Điểm huấn luyện cao hẳn mà kiểm tra thấp. Ở đây 0,879 so với 0,899: không thấy dấu hiệu.

**Hai cấu hình chênh 2 điểm Accuracy có kết luận được không?** Chưa. Sai số chuẩn khoảng 1,1 điểm, khoảng tin cậy 95% khoảng ±2,2 điểm với 726 mẫu.

**Chia phân tầng để làm gì?** Giữ tỉ lệ nhãn như nhau ở hai tập.

## Đánh giá
**Vì sao Recall quan trọng hơn Accuracy ở bài này?** Bỏ sót một em sắp bỏ học đắt hơn báo nhầm một em ổn.

**Chọn ngưỡng thế nào?** Là quyết định của nhà trường. Hạ từ 0,5 xuống 0,3: Recall từ 85,6% lên 91,5%, bỏ sót từ 41 xuống 24, nhưng báo nhầm từ 32 lên 71.

**AUC khác Accuracy?** AUC đo khả năng xếp hạng nguy cơ, không phụ thuộc ngưỡng.

**Cấu hình nào dùng cho cảnh báo sớm?** B1 (hết học kỳ 1): Recall khoảng 80,6%, AUC 0,914.

**Hai cột môn qua tương quan 0,92 thì sao?** Cộng tuyến: không nên đọc riêng từng trọng số.

## TabICLv2
**Học trong ngữ cảnh khác huấn luyện thường ở đâu?** Huấn luyện thường cập nhật trọng số trên dữ liệu của mình. TabICLv2 đã học xong từ trước; khi dùng chỉ đưa các ví dụ có nhãn làm ngữ cảnh, suy luận một lượt, không đổi trọng số.

**Attention làm gì?** So sánh em mới với các em cũ, đổi độ giống thành trọng số bằng softmax, rồi bỏ phiếu có trọng số theo nhãn.

**Q, K, V là gì?** Truy vấn, khóa, giá trị: ba vector sinh ra từ mỗi em bằng ba ma trận trọng số học được. Công thức softmax(QKᵀ/√d)·V.

**TabICLv2 có mấy tầng?** Ba tầng: nhúng theo cột, tương tác theo hàng, học trong ngữ cảnh theo cả bảng.

**QASSMax để làm gì?** Softmax dễ bị loãng khi ngữ cảnh dài; QASSMax điều chỉnh theo kích thước ngữ cảnh để sự chú ý vẫn tập trung.

**Muon khác AdamW?** Muon trực giao hóa cập nhật gradient của các ma trận trọng số bằng phép lặp Newton–Schulz, cho phép tốc độ học cao hơn. Chỉ dùng lúc huấn luyện trước.

**Vì sao học trên dữ liệu giả lập vẫn dùng được cho dữ liệu thật?** Bảng giả sinh từ các mô hình nhân quả ngẫu nhiên rất đa dạng, nên mô hình học được kinh nghiệm chung. Nếu dữ liệu thật lạ hẳn thì có thể kém.

**Kết quả TabICLv2 của nhóm thế nào?** Nhóm đã chạy TabICLv2 thật (tabicl 2.2.0, 8 ensemble, toàn bộ tập huấn luyện làm ngữ cảnh) trên cùng cách chia và bốn cấu hình. Accuracy: A 75,6%, B1 87,9%, B 91,3%, C 94,6%. AUC cao hơn Hồi quy Logistic ở cả bốn (0,823; 0,934; 0,955; 0,977). Nhưng chênh Accuracy chỉ 0,1 đến 1,4 điểm, nhỏ hơn sai số ±2,2 điểm, và mới một lần chia, nên chưa kết luận TabICLv2 chính xác hơn. Mô tả TabICLv2 trong bài là tóm tắt từ bài gốc, cần đối chiếu.

**TabICLv2 hơn nhiều nhất ở cấu hình nào?** Ở A (Recall hơn 4,6 điểm), còn ở C ngang nhau. Nhóm đã dự đoán ngược lại (hơn nhiều nhất ở C) và nói thẳng điều đó; nguyên nhân chưa kiểm chứng.

**Attention minh họa của nhóm có phải TabICLv2 không?** Không. Đó là bản đơn giản không có trọng số học được, chỉ để thấy cơ chế.
