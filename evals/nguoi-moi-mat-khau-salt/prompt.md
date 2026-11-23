---
tags: [skill-creator, nguoi-moi]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tôi viết một bài ngắn cho phụ huynh và học sinh cấp 3 đọc, về chuyện vì sao trang web không lưu mật khẩu của họ. Vẽ giúp tôi một hình Excalidraw minh hoạ, chữ trong hình tiếng Việt. Đặt tên spec là mat-khau-salt.json, lưu spec và các file xuất ra vào thư mục hinh-ve/ ở thư mục làm việc.

<bai>
Khi bạn đăng ký với mật khẩu `meo123`, một trang web làm đúng cách sẽ không lưu chữ `meo123` ở đâu cả.
Nó sinh một chuỗi ngẫu nhiên gọi là salt (16 byte, mỗi tài khoản một salt khác nhau), ghép salt với mật khẩu, rồi đưa qua bcrypt - một hàm băm (hash) chậm có chủ ý, chỉ chạy một chiều: từ kết quả không tính ngược ra được mật khẩu.
Cơ sở dữ liệu chỉ giữ salt và kết quả băm, dạng `$2b$12$` + salt + hash.
Hai người cùng đặt `meo123` vẫn có hai dòng khác hẳn nhau trong cơ sở dữ liệu, vì salt khác nhau.

Lúc đăng nhập, trang web lấy salt đã lưu của tài khoản đó, băm lại mật khẩu bạn vừa gõ, rồi so hai kết quả băm. Giống nhau thì cho vào.

Nếu kẻ xấu lấy trộm được cơ sở dữ liệu, chúng không đọc được mật khẩu.
Chúng cũng không dùng được rainbow table - bảng tính sẵn kết quả băm của hàng triệu mật khẩu phổ biến - vì bảng đó được tính KHÔNG có salt, và với salt riêng cho từng người thì phải tính lại từ đầu cho từng tài khoản.
bcrypt lại chậm có chủ ý (cost 12, khoảng 0,25 giây mỗi lần thử), nên đoán thử hàng tỷ mật khẩu cho mỗi tài khoản là quá đắt.
Mật khẩu quá phổ biến như `123456` thì vẫn bị đoán ra sớm: salt không cứu được mật khẩu yếu.
</bai>
