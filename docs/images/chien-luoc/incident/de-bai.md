Tình huống giả định.
Người đọc: lập trình viên backend ở các team khác trong công ty; biết Postgres và log ở mức dùng hằng ngày, không trực vận hành.
Bối cảnh: bản postmortem nội bộ về sự cố cửa hàng online ngừng nhận đơn tối thứ Bảy (công ty và người trong bài đều là giả định).
Bộ hình đầy đủ có ba hình: (1) đĩa đầy dần theo thời gian, hình này; (2) cơ chế: vì sao Postgres dừng hẳn khi không ghi được WAL; (3) cách sửa: tách log ra đĩa riêng, trước và sau.

Nguồn (trích postmortem):
- Máy chủ Postgres có một đĩa 200 GB, chứa cả dữ liệu (120 GB, gần như không đổi trong ngày) lẫn file log của Postgres.
- Biểu đồ dung lượng đĩa được xem từ 12:00 đến 22:00. Bình thường log chỉ tăng khoảng 1 GB mỗi ngày và được dọn mỗi đêm.
- 13:00, để dò một truy vấn chậm, cấu hình log_min_duration_statement được đổi từ 1000 (chỉ ghi truy vấn chậm hơn 1 giây) thành 0 (ghi mọi truy vấn). Thay đổi không có hạn tự gỡ. Đây là tác nhân kích hoạt.
- Từ 13:00 log tăng 10 GB mỗi giờ.
- Nguyên nhân gốc: log và dữ liệu nằm chung một đĩa, và log không có giới hạn dung lượng, nên log ăn dần chỗ của dữ liệu.
- Cảnh báo đĩa chỉ đặt ở 95% (190 GB). 20:00 cảnh báo kêu; lúc đó chỉ còn 10 GB trống, tức 1 giờ. Người trực đang tìm nguyên nhân thì đĩa đầy.
- 21:00 đĩa đầy 200 GB. Postgres không ghi được WAL ("No space left on device") và dừng; mọi lệnh đặt hàng trả lỗi 500.
- 21:25 người trực xoá log cũ, giải phóng 70 GB (đĩa còn 130 GB) và trả log_min_duration_statement về 1000. 21:40 Postgres chạy lại, nhận đơn trở lại.
- Ảnh hưởng: 40 phút không nhận được đơn, khoảng 1 800 đơn thất bại.
- Hành động: chuyển log sang đĩa riêng giới hạn 20 GB; mọi thay đổi cấu hình để debug phải có hạn tự gỡ; thêm cảnh báo ở 80%.
