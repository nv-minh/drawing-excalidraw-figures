Tình huống giả định.
Người đọc: chị Thu, DBA PostgreSQL 8 năm kinh nghiệm, được nhờ review schema playlist của app nghe nhạc NhacViet trước khi lên production.

Yêu cầu nghiệp vụ (team backend viết):
- Mỗi user có 0 hoặc nhiều playlist; mỗi playlist thuộc đúng 1 user.
- Playlist có thứ tự, chứa tối đa 10 000 bài.
- Một bài hát được xuất hiện nhiều lần trong cùng một playlist: playlist 12 "Chạy bộ" có bài 501 "Lạc Trôi" ở vị trí 1 và vị trí 3, bài 733 "Nơi này có anh" ở vị trí 2.
- Một bài hát có thể nằm trong 0 hoặc nhiều playlist.

Bản nháp 1: bảng playlist_tracks(playlist_id FK, track_id FK, position), khoá chính (playlist_id, track_id).
Khi INSERT (12, 501, 3), PostgreSQL báo lỗi 23505 duplicate key value violates unique constraint "playlist_tracks_pkey".
Bản nháp 2: khoá chính đổi thành (playlist_id, position); track_id chỉ là FK thường, không UNIQUE.
Ba hàng (12, 501, 1), (12, 733, 2), (12, 501, 3) cùng ghi được.
Các bảng còn lại: users(id PK, email UNIQUE), playlists(id PK, user_id FK, name), tracks(id PK, title, duration_s).
Chèn một bài vào giữa (hoặc kéo đổi chỗ) phải dời position của các hàng phía sau, ví dụ UPDATE ... SET position = position + 1.
PK thường (không DEFERRABLE) được PostgreSQL kiểm tra trùng ngay sau từng hàng, nên lệnh dời này có thể báo 23505 giữa chừng.
Cách xử lý: khai báo PK là DEFERRABLE; khi đó (mặc định INITIALLY IMMEDIATE) việc kiểm tra trùng dời tới cuối câu lệnh, đủ cho một lệnh UPDATE. Chỉ cần INITIALLY DEFERRED (kiểm lúc COMMIT) khi việc dời trải qua nhiều câu lệnh trong một transaction.
PK mới bắt đầu bằng playlist_id nên không giúp tìm theo track_id: cần thêm index trên playlist_tracks(track_id), nếu không thì xoá một track sẽ quét cả bảng để kiểm FK.
Đổi lại, PK DEFERRABLE không dùng được làm arbiter cho INSERT ... ON CONFLICT và không làm đích cho FK của bảng khác.
