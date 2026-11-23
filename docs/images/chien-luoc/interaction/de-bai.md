Tình huống giả định.
Người đọc: Minh, lập trình viên web (Node.js), biết HTTP, redirect, cookie và JSON, nhưng chưa từng tự làm "Đăng nhập bằng Google".
Team muốn thêm nút này cho app shop.example (có backend riêng), theo OAuth 2.0 Authorization Code kèm PKCE.
Minh cần hiểu ai gửi gì cho ai, theo thứ tự nào, trước khi đọc code.

Ghi chú kỹ thuật của team:
- Người dùng bấm nút, trình duyệt gọi GET /login/google. Backend tạo state ngẫu nhiên và code_verifier ngẫu nhiên dài 43 đến 128 ký tự, cất cả hai trong session phía server; code_challenge = BASE64URL(SHA-256(code_verifier)). Trình duyệt chỉ giữ một cookie session id, đặt ở bước 302 kế tiếp với SameSite=Lax để trình duyệt gửi kèm khi Google chuyển về /callback.
- Backend trả 302, đưa trình duyệt sang https://accounts.google.com/o/oauth2/v2/auth kèm response_type=code, client_id, redirect_uri, scope "openid email", state, code_challenge và code_challenge_method=S256 (thiếu S256 thì Google coi là plain và bước đổi token thất bại).
- Người dùng đăng nhập Google và bấm "Cho phép". Google trả 302 về https://shop.example/callback?code=...&state=...
- Nếu người dùng bấm "Hủy", Google trả 302 về redirect_uri là /callback?error=access_denied&state=... (RFC 6749 mục 4.1.2.1); backend vẫn so state rồi hiện lại trang đăng nhập.
- Backend so state trên URL với state trong session; khác nhau thì trả 400 và dừng.
- Backend gọi thẳng POST https://oauth2.googleapis.com/token (server tới server, không qua trình duyệt), gửi grant_type=authorization_code, code, code_verifier, client_id, client_secret và redirect_uri.
- Google tính SHA-256 của code_verifier và so với code_challenge nhận ở bước đầu. Code chỉ dùng được 1 lần và hết hạn sau tối đa 10 phút.
- Google trả 200 với access_token, id_token (chứa email người dùng) và expires_in: 3599 (giây).
- Backend kiểm id_token (aud phải là client_id của app, iss là accounts.google.com, exp chưa qua), nhận diện user bằng claim sub trong id_token (id cố định của tài khoản Google), rồi tạo phiên đăng nhập, trả 302 về trang chủ kèm cookie phiên.
