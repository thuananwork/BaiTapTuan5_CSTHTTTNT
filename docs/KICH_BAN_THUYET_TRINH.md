# Kịch bản thuyết trình – Nhóm 6

Khớp với file `slides/Bài thuyết trình (đã sửa) - thêm chú thích.pptx` (16 slide). Phần **Lời nói** lấy đúng từ ghi chú của từng slide trong file đó, nên bạn có thể mở chế độ Presenter View của PowerPoint và đọc cùng lúc.

**Thời lượng:** khoảng 20–22 phút nếu đọc đủ phần Lời nói (≈ 3.000 từ). Nếu chỉ có 10–12 phút thì bỏ bớt các câu chi tiết, giữ ý chính và con số in đậm ở mỗi slide. Slide 8 và 9 cần nhiều thời gian nhất, slide 1, 14, 16 ngắn nhất.

**Cách dùng:** đừng đọc nguyên văn. Đọc một lần để nắm ý, rồi nói bằng lời của mình. Mỗi slide chỉ cần nhớ **một ý chính** và **một con số**.

## Những điều không được nói quá

- TabICLv2 chỉ chạy **một lần**, một lần chia dữ liệu, cấu hình mặc định. Đừng nói "TabICLv2 tốt hơn". Hãy nói "AUC cao hơn ở cả bốn cấu hình, nhưng Accuracy chênh nhỏ hơn sai số ±2,2".
- Ví dụ attention ở slide 9 là phép tính tay để thấy cơ chế, không phải TabICLv2 thật.
- Số liệu ngưỡng ở slide 12 là của **Logistic** cấu hình B, không phải TabICLv2.
- Điểm HK2 phần nào đã chứa sẵn "đáp án" (em đã nghỉ thì không có điểm). Cảnh báo sớm thật sự là cấu hình B1 (hết HK1).
- Phần mô tả kiến trúc ở slide 8 (Set Transformer, token CLS, dữ liệu tổng hợp, tên tác giả và nơi công tác) viết theo bài báo nhưng **chưa được đối chiếu lại**. Nếu bị hỏi sâu, hãy nói "nhóm tóm tắt từ bài báo".

---

## Slide 1. Mở đầu

**Làm gì trên slide:** Chào, giới thiệu nhóm và đề tài. Chưa cần công thức.

**Lời nói:**

> Xin chào thầy cô và các bạn. Nhóm 6 xin trình bày đề tài: Cơ sở toán học của TabICLv2, ứng dụng vào bài toán dự đoán nguy cơ sinh viên bỏ học.
> Bài gồm ba phần: (1) bài toán và bộ dữ liệu; (2) nền tảng toán học: ma trận dữ liệu, chuẩn hóa, sigmoid, cross-entropy, gradient descent và cơ chế attention của TabICLv2; (3) kết quả so sánh TabICLv2 với Logistic Regression, cách chọn ngưỡng cảnh báo và các hạn chế.
> Câu hỏi xuyên suốt: làm sao từ vài con số về học phí, điểm số, tuổi... ta tính ra được xác suất một sinh viên sẽ bỏ học?

**Chuyển ý:** "Bắt đầu từ bài toán cụ thể nhé."

---

## Slide 2. Bài toán dự đoán nguy cơ bỏ học

**Làm gì trên slide:** Chỉ vào x ∈ ℝ⁸ → P(y=1|x) và con số 3.630.

**Lời nói:**

> Bài toán của nhóm: mỗi sinh viên được mô tả bằng một vector 8 chiều x. Mô hình nhận x và trả về xác suất bỏ học P(y = 1 | x), trong đó y = 1 là bỏ học, y = 0 là tốt nghiệp.
> Theo data.csv, bộ dữ liệu gốc có 4.424 sinh viên với ba nhãn: 2.209 tốt nghiệp, 1.421 bỏ học và 794 đang học. Nhóm loại 794 sinh viên đang học vì chưa biết kết cục cuối cùng của các em. Còn lại 3.630 sinh viên, và bài toán trở thành phân loại nhị phân.
> Vì sao ưu tiên Recall lớp bỏ học? Recall = số em bỏ học được phát hiện / tổng số em bỏ học. Bỏ sót một em có nguy cơ thì nhà trường mất cơ hội can thiệp; còn báo nhầm một em thì chỉ tốn thêm một buổi tư vấn. Hai loại sai này có cái giá khác nhau, và ý này sẽ quay lại ở phần chọn ngưỡng.

**Chuyển ý:** "Giờ xem dữ liệu thật trông thế nào."

---

## Slide 3. Bộ dữ liệu và 8 biến chọn lọc

**Làm gì trên slide:** Chỉ vào biểu đồ và 39,1%. Đọc 2–3 số, đừng đọc hết.

**Lời nói:**

> Bộ dữ liệu lấy từ UCI Machine Learning Repository: “Predict Students’ Dropout and Academic Success”, gồm 4.424 sinh viên, 36 biến đầu vào và không có giá trị thiếu.
> Nhóm chọn 8 biến theo ba nhóm: tài chính (học phí đúng hạn, nợ học phí, học bổng), học tập (điểm và số môn đạt ở HK1, HK2) và nhân khẩu (tuổi nhập học).
> Số liệu từ data.csv cho thấy vì sao chọn các biến này:
> • Không đóng học phí đúng hạn: 94,0% bỏ học, so với 30,7% ở nhóm đóng đúng hạn.
> • Đang nợ học phí: 75,5% bỏ học, so với 34,5% ở nhóm không nợ.
> • Có học bổng: chỉ 13,8% bỏ học, so với 48,4% ở nhóm không có học bổng.
> • Điểm trung bình HK2 (thang 20): nhóm bỏ học 5,9, nhóm tốt nghiệp 12,7. Số môn đạt HK2: 1,9 so với 6,2.
> • Tuổi nhập học trung bình: 26,1 ở nhóm bỏ học, 21,8 ở nhóm tốt nghiệp.
> Sau khi lọc, 1.421 / 3.630 = 39,1% là bỏ học. Lớp không quá lệch, nhưng một mô hình đoán “tốt nghiệp” cho tất cả vẫn đạt 60,9% accuracy, nên ta cần nhìn thêm Recall và AUC.

**Chuyển ý:** "Có dữ liệu rồi thì phải biến nó thành số máy tính xử lý được."

---

## Slide 4. Đại số tuyến tính: từ sinh viên đến ma trận

**Làm gì trên slide:** Chỉ vào hai số 67 và 30.622, nói 'chuẩn hóa giúp 450 lần'.

**Lời nói:**

> Bước đầu tiên là đưa dữ liệu về dạng ma trận. X có kích thước 3.630 × 8: mỗi hàng là một sinh viên, mỗi cột là một biến.
> Mô hình tuyến tính gán cho mỗi biến một trọng số: z = w₁x₁ + … + w₈x₈ + b, viết gọn z = Xw + b. z là “điểm nguy cơ” thô, chưa phải xác suất.
> Vấn đề: các biến có thang đo rất khác nhau. Tuổi tính bằng năm, điểm theo thang 20, còn học phí, nợ, học bổng chỉ là 0/1. Nếu để nguyên, trọng số của biến có thang lớn sẽ chi phối quá trình tối ưu.
> Giải pháp là chuẩn hóa z-score: x' = (x − μ) / σ, đưa mỗi cột về trung bình 0, độ lệch chuẩn 1.
> Con số chứng minh: số điều kiện κ của ma trận XᵀX/n giảm từ 30.622 xuống 67, tức khoảng 450 lần. κ đo độ “méo” của bề mặt loss: κ lớn thì bề mặt là một thung lũng hẹp và dài, gradient descent đi zig-zag và hội tụ chậm; κ nhỏ thì bề mặt gần tròn, đi thẳng về đáy.

**Chuyển ý:** "z mới là điểm thô. Giờ biến nó thành xác suất."

---

## Slide 5. Sigmoid biến điểm số thành xác suất

**Làm gì trên slide:** Chỉ vào hình sigmoid, rồi hai ví dụ 0,9 và 0,1 trong cross-entropy.

**Lời nói:**

> Điểm z có thể là bất kỳ số thực nào, nhưng ta cần một xác suất. Hàm sigmoid p = 1 / (1 + e⁻ᶻ) ép mọi z vào khoảng (0, 1).
> Vài giá trị để cảm nhận: z = 0 cho p = 0,5; z = 2 cho p ≈ 0,88; z = −2 cho p ≈ 0,12. Hàm đối xứng quanh 0,5 và tăng đơn điệu, nên z càng lớn thì nguy cơ bỏ học càng cao.
> Để đo mô hình sai bao nhiêu, ta dùng cross-entropy: L = −[y log(p) + (1−y) log(1−p)]. Với một em thực sự bỏ học (y = 1), L chỉ còn −log(p).
> Ví dụ: nếu mô hình nói p = 0,9 thì L ≈ 0,11; nếu nói p = 0,1, tức tự tin nhưng sai, thì L ≈ 2,30, lớn gấp khoảng 22 lần. Đó là ý “phạt rất mạnh dự đoán tự tin nhưng sai”.
> Thêm một góc nhìn xác suất: cross-entropy chính là log-likelihood âm của phân phối Bernoulli, nên tối thiểu hóa L tương đương ước lượng hợp lý cực đại. Và đạo hàm của L theo z rất gọn: ∂L/∂z = p − y. Kết quả này dẫn thẳng sang slide gradient tiếp theo.

**Chuyển ý:** "Có mức phạt rồi thì phải chỉnh trọng số cho phạt giảm."

---

## Slide 6. Gradient Descent: đi xuống bề mặt loss

**Làm gì trên slide:** Chỉ vào hình ba đường η nhỏ / vừa / lớn.

**Lời nói:**

> Có loss rồi, giờ cần tìm w làm loss nhỏ nhất. Áp dụng quy tắc chuỗi với ∂L/∂z = p − y ở slide trước, gradient trên toàn bộ dữ liệu là ∇L = Xᵀ(p − y) / n.
> Đọc công thức: (p − y) là sai số dự đoán của từng sinh viên; nhân với Xᵀ nghĩa là mỗi trọng số được điều chỉnh theo mức biến đó góp phần vào sai số. Chia n để lấy trung bình trên 3.630 sinh viên (trên thực tế là 2.904 sinh viên tập huấn luyện).
> Quy tắc cập nhật: w ← w − η·∇L, tức bước ngược hướng gradient, xuống dốc bề mặt loss. η là tốc độ học.
> Hình minh họa ba trường hợp: η nhỏ thì đi đúng hướng nhưng rất chậm; η vừa thì hội tụ nhanh về đáy; η lớn thì nhảy qua đáy, loss tăng dần và phân kỳ.
> Với Logistic Regression, cross-entropy là hàm lồi nên chỉ có một cực tiểu toàn cục, không lo kẹt ở cực tiểu địa phương. Liên hệ slide 4: κ lớn buộc ta chọn η nhỏ để không phân kỳ theo hướng dốc nhất; chuẩn hóa làm κ nhỏ nên có thể dùng η lớn hơn và đi đường thẳng hơn.

**Chuyển ý:** "Mô hình xong, giờ kiểm tra xem nó dùng được không."

---

## Slide 7. Chia dữ liệu & đánh giá hiệu năng

**Làm gì trên slide:** Chỉ vào hai cột 87,9% và 89,9%, rồi nói 'sai số ±2,2'. Nhớ số 2,2 này, còn dùng lại.

**Lời nói:**

> Để đánh giá công bằng, nhóm chia dữ liệu 80/20: 2.904 sinh viên để huấn luyện và 726 sinh viên để kiểm tra. Chia phân tầng (stratified) nên cả hai tập đều giữ tỷ lệ bỏ học khoảng 39,1%. Seed 42 giúp tái lập đúng kết quả.
> Tập kiểm tra chỉ có 726 em nên bản thân accuracy cũng có sai số. Sai số chuẩn SE = √(p(1−p)/n) = √(0,899 × 0,101 / 726) ≈ 0,011, tức khoảng 1,1 điểm phần trăm. Khoảng tin cậy 95% là ±1,96 × SE ≈ ±2,2 điểm.
> Ý nghĩa thực tế: hai mô hình chênh nhau dưới khoảng 2,2 điểm accuracy trên tập này thì chưa thể nói mô hình nào tốt hơn. Con số này sẽ dùng lại ở slide so sánh.
> Biểu đồ: accuracy huấn luyện 87,9%, kiểm tra 89,9%. Điểm kiểm tra không thấp hơn điểm huấn luyện, nên mô hình không học vẹt (overfitting). Chênh 2 điểm theo chiều ngược lại nằm trong sai số do chia ngẫu nhiên.

**Chuyển ý:** "Phần nền tảng xong. Giờ sang mô hình chính."

---

## Slide 8. TabICLv2 học ngay trong ngữ cảnh

**Làm gì trên slide:** Chỉ vào công thức attention nhưng đừng giải thích hết, để slide sau tính tay.

**Lời nói:**

> Bây giờ đến nhân vật chính: TabICLv2, của Jingang Qu và cộng sự tại INRIA Saclay, công bố ở ICML 2026. Đây là một “mô hình nền tảng cho dữ liệu bảng” (tabular foundation model).
> Khác biệt cốt lõi so với Logistic Regression: TabICLv2 không chạy gradient descent trên dữ liệu của nhóm. Mô hình là một Transformer đã được tiền huấn luyện sẵn trên rất nhiều bảng dữ liệu tổng hợp (sinh từ mô hình nhân quả cấu trúc), hoàn toàn không dùng dữ liệu thật. Khi dùng, ta đưa 2.904 sinh viên đã có nhãn vào làm “ngữ cảnh”, đưa sinh viên cần dự đoán làm “câu hỏi”, và chỉ một lượt lan truyền xuôi (forward pass) là ra xác suất. Đó là nghĩa của “học trong ngữ cảnh” (in-context learning).
> Kiến trúc gồm ba tầng: (1) nhúng theo cột bằng Set Transformer, mỗi biến được biểu diễn dựa trên phân phối của cả cột; (2) tương tác theo hàng bằng Transformer với token CLS, gộp 8 biến của một sinh viên thành một vector; (3) học trong ngữ cảnh theo tập dữ liệu: sinh viên mới “nhìn” sang các sinh viên huấn luyện qua attention.
> Công thức attention: Q (query) lấy từ sinh viên mới, K (key) và V (value) lấy từ các sinh viên trong ngữ cảnh, trong đó V mang thông tin nhãn. QKᵀ là tích vô hướng, đo mức giống nhau. Chia √d để tích vô hướng không quá lớn khi số chiều d lớn, tránh softmax bị bão hòa thành 0/1 và gradient biến mất lúc tiền huấn luyện.
> Vì vậy, thay vì một đường biên tuyến tính cố định như Logistic, dự đoán của TabICLv2 phụ thuộc vào việc sinh viên mới giống những ai trong dữ liệu.

**Chuyển ý:** "Công thức khó hình dung, nên làm một ví dụ tính tay."

---

## Slide 9. Attention: giống ai thì lắng nghe người đó

**Làm gì trên slide:** Đây là slide quan trọng nhất để người nghe hiểu. Chậm lại, đọc từng số 2, 1, 0, 0.

**Lời nói:**

> Slide này giải thích attention bằng một ví dụ tính tay. Giả sử có một sinh viên mới và 4 sinh viên trong ngữ cảnh. Điểm tương đồng QKᵀ/√d lần lượt là 2, 1, 0, 0.
> Softmax lấy e mũ rồi chuẩn hóa: e² ≈ 7,39; e¹ ≈ 2,72; e⁰ = 1; e⁰ = 1. Tổng ≈ 12,11. Chia ra được trọng số 0,61; 0,22; 0,08; 0,08, cộng lại bằng 1.
> Hai sinh viên đầu đã bỏ học (nhãn 1), hai sinh viên sau tốt nghiệp (nhãn 0). Xác suất bỏ học = 0,61 × 1 + 0,22 × 1 + 0,08 × 0 + 0,08 × 0 ≈ 0,83.
> Trực giác: “giống ai thì lắng nghe người đó”. Sinh viên mới giống em thứ nhất nhất, nên em đó có tiếng nói lớn nhất. Softmax khuếch đại khác biệt: điểm chỉ hơn 1 đơn vị nhưng trọng số gấp gần 3 lần.
> Trong TabICLv2 thật, quá trình này có nhiều head, nhiều lớp, và các vector Q, K, V được học trong lúc tiền huấn luyện chứ không phải điểm thô; nhưng phép toán ở mỗi bước đúng là phép tính trên slide.

**Chuyển ý:** "Giờ xem kết quả thật."

---

## Slide 10. Đối chứng: Logistic Regression

**Làm gì trên slide:** Chỉ vào biểu đồ, nói 4 cấu hình A, B1, B, C là 4 thời điểm cảnh báo.

**Lời nói:**

> Trước khi xem TabICLv2, nhóm dựng một mô hình đối chứng là Logistic Regression, chính là mô hình đã xây ở các slide 4 đến 6.
> Nhóm thử bốn cấu hình biến, tương ứng bốn thời điểm nhà trường có thể cảnh báo: A, lúc nhập học (8 biến, chưa có điểm đại học); B1, hết HK1 (6 biến); B, hết HK2 (8 biến đã chọn, cấu hình chính); C, đầy đủ 35 biến.
> Kết quả Logistic Regression: A đạt Accuracy 75,1%, Recall 58,1%, AUC 0,815. B1: 87,5%, 80,6%, 0,914. B: 89,9%, 85,6%, 0,940. C: 94,5%, 92,3%, 0,973.
> Thông điệp: càng có thêm dữ liệu học tập thì dự đoán càng chính xác. Nhưng cảnh báo càng sớm thì càng khó: lúc nhập học, mô hình chỉ bắt được khoảng 58% số em sẽ bỏ học. Đây là đánh đổi giữa “sớm” và “chính xác”.
> Lưu ý cách đọc biểu đồ: AUC được nhân 100 để cùng thang với hai chỉ số còn lại.

**Chuyển ý:** "Giờ đặt TabICLv2 cạnh Logistic."

---

## Slide 11. TabICLv2 so với Logistic Regression

**Làm gì trên slide:** Chỉ vào cột AUC trước, rồi nói Accuracy chênh nhỏ hơn ±2,2.

**Lời nói:**

> Bảng so sánh: mỗi ô ghi “Logistic Regression → TabICLv2”, cùng cách chia dữ liệu và cùng tập kiểm tra 726 sinh viên.
> AUC: TabICLv2 cao hơn ở cả bốn cấu hình, chênh +0,008 (A), +0,020 (B1), +0,015 (B) và +0,004 (C). AUC đo khả năng xếp hạng em có nguy cơ cao lên trên em nguy cơ thấp, xét trên mọi ngưỡng, nên đây là tín hiệu đáng tin hơn accuracy.
> Recall lớp bỏ học: tăng ở A (+4,6 điểm), B1 (+1,4) và B (+1,0), giảm nhẹ ở C (−0,4). Mức tăng lớn nhất nằm ở cấu hình A, khi dữ liệu ít nhất, phù hợp với việc TabICLv2 được thiết kế mạnh trên dữ liệu bảng nhỏ và vừa.
> Accuracy: chỉ chênh 0,1 đến 1,4 điểm, đều nhỏ hơn biên ±2,2 điểm đã tính ở slide 7. Vì vậy nhóm không kết luận TabICLv2 chính xác hơn về accuracy.
> Nói thẳng về giới hạn: TabICLv2 mới chạy một lần, cấu hình mặc định, trên một lần chia dữ liệu. Muốn khẳng định cần lặp nhiều seed hoặc kiểm tra chéo.

**Chuyển ý:** "Mô hình chỉ cho xác suất. Còn cảnh báo ở mức nào thì do người quyết."

---

## Slide 12. Ngưỡng cảnh báo là một quyết định

**Làm gì trên slide:** Chỉ vào hai khung ngưỡng 0,5 và 0,3. Nói rõ đây là số của Logistic cấu hình B.

**Lời nói:**

> Mô hình chỉ trả về xác suất; còn “bao nhiêu thì cảnh báo” là quyết định của con người. Số liệu trên slide là của Logistic Regression cấu hình B, trên 726 sinh viên kiểm tra, trong đó khoảng 284 em thực sự bỏ học.
> Ngưỡng 0,5: bỏ sót 41 em, báo nhầm 32 em, Recall 85,6%.
> Hạ ngưỡng xuống 0,3: bỏ sót còn 24 em, nhưng báo nhầm tăng lên 71 em, Recall 91,5%.
> Phép tính đánh đổi: ta phát hiện thêm 17 em có nguy cơ, đổi lại thêm 39 cảnh báo nhầm, tức khoảng 2,3 cảnh báo nhầm cho mỗi em được cứu thêm. Nếu nhà trường đánh giá việc để mất một sinh viên đắt hơn 2,3 buổi tư vấn thừa, thì ngưỡng 0,3 là lựa chọn hợp lý hơn.
> Ý chính: chọn ngưỡng là chọn cái giá của từng kiểu sai, không phải chi tiết kỹ thuật. Đây cũng là lý do ở slide 2 nhóm ưu tiên Recall.

**Chuyển ý:** "Tóm hai mô hình lại."

---

## Slide 13. TabICLv2 và Logistic Regression

**Làm gì trên slide:** Đọc ưu điểm trước, hạn chế sau, mỗi bên 2 ý.

**Lời nói:**

> Tóm lại hai hướng mô hình, mỗi bên có chỗ mạnh riêng.
> Logistic Regression: minh bạch, vì mỗi trọng số cho biết biến nào đẩy nguy cơ lên hay xuống; huấn luyện nhanh; và là một baseline mạnh, đã đạt AUC 0,940 ở cấu hình B. Hạn chế: đường biên quyết định là tuyến tính, và muốn bắt quan hệ phi tuyến thì phải tự tạo thêm biến (feature engineering).
> TabICLv2: học trong ngữ cảnh, không cần huấn luyện lại hay tinh chỉnh siêu tham số trên dữ liệu của nhóm; attention cho phép so sánh linh hoạt sinh viên mới với từng ví dụ đã biết; đạt AUC 0,955 ở cấu hình B. Hạn chế: mới chạy một lần, và lợi thế về accuracy chưa vượt sai số thống kê. Thêm nữa, mô hình khó giải thích hơn và nặng hơn về tính toán so với Logistic.
> Nếu cần giải thích cho phòng công tác sinh viên vì sao một em bị cảnh báo, Logistic dễ trình bày hơn; nếu ưu tiên xếp hạng nguy cơ tốt nhất, TabICLv2 có lợi thế về AUC.

**Chuyển ý:** "Đến kết luận."

---

## Slide 14. Kết luận chính

**Làm gì trên slide:** Chỉ vào ba ô 01, 02, 03 theo thứ tự.

**Lời nói:**

> Ba kết luận chính của nhóm:
> 01. Bài toán bỏ học được mô hình hóa gọn trong một vector 8 chiều cho mỗi sinh viên, và đầu ra là một xác suất bỏ học chứ không chỉ là nhãn có/không. Dữ liệu cho thấy tài chính (học phí, nợ, học bổng) và kết quả học tập hai học kỳ đầu là những tín hiệu mạnh nhất.
> 02. Toán học cốt lõi gồm bốn mảnh nối tiếp nhau: chuẩn hóa giảm số điều kiện từ 30.622 xuống 67; sigmoid biến điểm thành xác suất; cross-entropy đo sai lệch; gradient descent tìm trọng số tốt nhất. TabICLv2 bổ sung mảnh thứ năm: attention và softmax để so sánh với các ví dụ đã biết.
> 03. Logistic Regression là baseline mạnh. TabICLv2 nhỉnh hơn về AUC ở cả bốn cấu hình (ví dụ 0,955 so với 0,940 ở cấu hình B), nhưng chênh lệch accuracy còn nằm trong sai số ±2,2 điểm.

**Chuyển ý:** "Cuối cùng là những điều nhóm chưa làm được."

---

## Slide 15. Hạn chế mở ra câu hỏi tiếp theo

**Làm gì trên slide:** Nói chậm, đây là phần thể hiện nhóm hiểu giới hạn của mình.

**Lời nói:**

> Nhóm cũng muốn nói rõ các hạn chế, vì chúng chính là câu hỏi cho bước tiếp theo.
> 01. TabICLv2 mới chạy một lần với cấu hình mặc định, nên chưa biết kết quả dao động bao nhiêu giữa các lần chạy.
> 02. Tương quan cao. Theo data.csv, số môn đạt HK2 có tương quan −0,65 với nhãn bỏ học, điểm HK2 là −0,61. Số môn đạt HK1 và HK2 tương quan với nhau tới 0,92, điểm HK1 và HK2 là 0,85, tức có đa cộng tuyến. Điểm HK2 gần với “đáp án” vì sinh viên đã bỏ học thường không còn điểm ở học kỳ đó; nếu mục tiêu là cảnh báo sớm thì dùng biến này dễ làm kết quả đẹp hơn thực tế.
> 03. Mới chia dữ liệu một lần (seed 42), chưa kiểm tra chéo k-fold, nên các con số có thể thay đổi với cách chia khác.
> 04. Hướng tiếp theo: thêm dữ liệu hành vi như điểm danh, hoạt động trên hệ thống học trực tuyến, để cảnh báo được sớm hơn mà không cần chờ điểm HK2; và thử thêm các mô hình mới.
> Đọc câu trích dẫn trên slide: “Đoán đúng hay sai chưa đáng giá bằng việc biết cái giá của từng kiểu sai.” Câu này nối lại với slide chọn ngưỡng.

**Chuyển ý:** "Cảm ơn và mời hỏi."

---

## Slide 16. Cảm ơn và hỏi đáp

**Làm gì trên slide:** Dừng ở slide này khi hỏi đáp. Các câu trả lời mẫu nằm ngay dưới.

**Lời nói:**

> Phần trình bày của Nhóm 6 đến đây là hết. Cảm ơn thầy cô và các bạn đã lắng nghe. Tài liệu chính gồm bài báo TabICLv2 của Qu và cộng sự (ICML 2026), bộ dữ liệu UCI và giáo trình Deep Learning của Goodfellow, Bengio và Courville. Nhóm xin mời câu hỏi.
> Gợi ý trả lời các câu hỏi có thể gặp:
> • Vì sao loại 794 sinh viên đang học? Vì các em chưa có kết cục; gán nhãn “không bỏ học” cho các em sẽ làm sai nhãn.
> • TabICLv2 không huấn luyện thì “học” ở đâu? Phần học diễn ra lúc tiền huấn luyện trên dữ liệu tổng hợp; khi dùng, mô hình đọc 2.904 sinh viên có nhãn làm ngữ cảnh và suy luận trong một lượt forward pass.
> • Attention ở đây khác gì attention trong mô hình ngôn ngữ? Cùng công thức softmax(QKᵀ/√d)·V, nhưng “token” là sinh viên (hàng trong bảng) thay vì từ.
> • Vì sao không chỉ dùng accuracy? Với 39,1% bỏ học, đoán “tốt nghiệp” cho tất cả đã được 60,9%; Recall và AUC phản ánh đúng mục tiêu phát hiện em có nguy cơ.

---

## Nếu bị hỏi ngoài kịch bản

Xem thêm `docs/HoiDap_Thay.md`. Nếu không biết thì nói thẳng "phần này nhóm chưa kiểm tra" thay vì đoán.
