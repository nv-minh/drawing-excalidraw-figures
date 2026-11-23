Tình huống giả định.
Người đọc: kỹ sư mạng và SRE chuyên về hiệu năng TCP, đọc tài liệu nội bộ về một lần đo; họ đã thuộc cwnd, ssthresh, RTT, RTO, dup ACK.
Bối cảnh: một luồng TCP Reno không bật SACK được đo trên đường truyền RTT 100 ms, cwnd tính bằng segment (MSS 1460 byte); tài liệu muốn đặt hai kiểu mất gói cạnh nhau trên cùng một lần đo.

Nguồn (trích ghi chép đo):
- Kết nối bắt đầu với cwnd ban đầu 10 segment (IW10, RFC 6928) và ssthresh ban đầu 80 segment (giả định của lần đo này).
- Slow start: cwnd nhân đôi mỗi RTT từ RTT 0, 10, 20, 40, 80 ở RTT 3; tới ssthresh 80 thì chuyển sang congestion avoidance.
- Congestion avoidance: cwnd tăng 1 segment mỗi RTT, 81, 82, 83, 84, 85.
- Ở RTT thứ 8 (cwnd 85) bên gửi nhận 3 dup ACK: fast retransmit rồi fast recovery; ssthresh = 85 / 2 = 42, cwnd = 42 (RFC 5681). Không có khoảng im lặng nào.
- Sau đó cwnd lại tăng 1 mỗi RTT: 43, 44, 45, 46, 47.
- Ở RTT thứ 13 (cwnd 47) đường truyền đứt ngắn và mất cả cửa sổ 47 gói đang bay: không gói nào tới bên nhận, nên không có dup ACK nào và cũng không gói nào được ACK; bên gửi phải chờ hết RTO. RTO lúc này là 1 s, mức tối thiểu của RFC 6298, tức 10 RTT không gửi gì, từ RTT 13 tới RTT 23. Trong lúc chờ, cwnd và ssthresh chưa đổi (cwnd vẫn 47, ssthresh vẫn 42); chúng chỉ đổi khi RTO hết hạn.
- Khi RTO hết hạn ở RTT 23: ssthresh = max(FlightSize / 2, 2 SMSS) theo RFC 5681; FlightSize = 47 vì cả cửa sổ chưa được ACK, nên ssthresh = 47 / 2 ≈ 23, cwnd = 1 segment. Chạy lại slow start từ RTT 23: 1, 2, 4, 8, 16, rồi 23 ở RTT 28 (chạm ssthresh), sau đó 24, 25 theo congestion avoidance tới RTT 30.
- Ghi chép vẽ fast recovery đơn giản: cwnd về thẳng 42, bỏ bước tạm cwnd = ssthresh + 3 trong lúc phục hồi.
- Kết luận của ghi chép: 3 dup ACK chỉ cắt một nửa và đi tiếp; timeout mất 1 s im lặng, rơi về 1 segment và phải leo lại từ đầu, chậm hơn nhiều.
