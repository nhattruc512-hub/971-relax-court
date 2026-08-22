# 971 Relax Court — Auto Print KPOS Zy307

Cấu hình hiện tại:
- Máy in: KPOS Zy307 (ESC/POS, 80mm)
- IP: `192.168.1.199`
- Port: `9100`
- Máy Windows và máy in phải ở cùng mạng LAN/Wi-Fi.

## Cài đặt
1. Tải thư mục `print-bridge` về máy Windows tại quầy.
2. Cài Python 3 nếu máy chưa có (khi cài từ python.org nhớ chọn Add Python to PATH; Microsoft Store cũng được).
3. Nhấp đúp `CAI_DAT_WINDOWS.bat`.
4. Giữ cửa sổ `971 Relax Court - Auto Print` chạy. Bộ cài đã thêm chương trình vào Startup nên lần sau Windows bật lên nó sẽ tự chạy.
5. Nếu Windows Firewall hỏi, chọn Allow access.

## Kiểm tra mạng máy in
Mở Command Prompt và chạy:
`ping 192.168.1.199`

Có Reply là máy tính nhìn thấy máy in.

## Hoạt động
Print Bridge hỏi hàng đợi Supabase khoảng 2 giây/lần. Khi có print job mới, nó gửi ESC/POS trực tiếp tới `192.168.1.199:9100`, đánh dấu job đã in, rồi tiếp tục chờ.

Không chia sẻ BRIDGE_KEY ra bên ngoài; file bridge chỉ nên đặt trên máy quầy.
