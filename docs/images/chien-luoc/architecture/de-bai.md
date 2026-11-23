Tình huống giả định.
Người đọc: Hà, sinh viên năm nhất ngành kinh tế, học môn Nhập môn CNTT.
Hà đọc báo trên điện thoại mỗi ngày nhưng chưa nghe tới CDN, load balancer, cache hay database.
Thầy giao câu hỏi: "Vì sao báo điện tử VnTin chịu được 2 triệu lượt đọc mỗi giờ?"

Mô tả hệ thống của VnTin (giả định):
- Khi người đọc mở một bài, ảnh, CSS và JavaScript lấy từ CDN: máy chủ đặt sẵn ở 3 thành phố (Hà Nội, Đà Nẵng, TP.HCM), trả ảnh trong khoảng 20 ms.
- Phần chữ của bài đi qua load balancer, chia đều cho 4 web server giống hệt nhau.
- Web server hỏi Redis (cache, giữ bài trong bộ nhớ) trước: cứ 10 lần thì 9 lần bài đã có sẵn, trả trong khoảng 1 ms.
- Nếu Redis chưa có, web server đọc bài từ PostgreSQL (database gốc, lưu trên đĩa), mất khoảng 30 ms, rồi chép bài vào Redis, giữ 5 phút.
- Nhờ vậy, cứ 10 lượt đọc bài thì chỉ 1 lượt phải hỏi tới PostgreSQL.
- Tức là trong 2 triệu lượt đọc mỗi giờ, chỉ khoảng 200 nghìn lượt (2 triệu × 1/10) phải hỏi tới PostgreSQL.
