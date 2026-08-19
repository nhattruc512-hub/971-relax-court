# 971 RELAX COURT

Website gọi nước + đồ ăn qua QR, không yêu cầu khách đăng nhập.

## Trang
- `index.html`: trang khách gọi món
- `staff.html`: trang nhân viên nhận đơn và xem doanh thu
- PIN nhân viên: `270523`

## QR từng sân
Sau khi website có URL chính thức:
- `/?court=PICK1`
- `/?court=PICK2`
- `/?court=PICK3`
- `/?court=CL1`
- `/?court=CL2`

## Chức năng
- Menu Nước / Đồ ăn + Sữa chua
- Giỏ hàng chung
- Ghi chú khách
- Chuyển khoản QR MoMo hoặc tiền mặt
- Báo đơn mới cho nhân viên
- Tổng doanh thu ngày
- Doanh thu Ca 1 05:00–11:00
- Doanh thu Ca 2 14:00–18:00
- Doanh thu Ca 3 18:00–22:00

Backend: Supabase Edge Function `r971-api`.
