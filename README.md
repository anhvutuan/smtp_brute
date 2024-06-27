# Mô tả về script
Script này có thể thực hiện hai loại tấn công brute force:

userbrute: Tấn công dò tìm tài khoản người dùng.
passwordspray: Tấn công dò tìm mật khẩu cho một danh sách người dùng.

## Các bước chuẩn bị

Cài đặt các thư viện cần thiết:
Script yêu cầu các thư viện smtplib, threading, time, colorama, và pyfiglet. Bạn có thể cài đặt các thư viện này bằng cách sử dụng pip:

pip install colorama pyfiglet

Chạy script:
Để chạy script, bạn cần sử dụng lệnh python3 và cung cấp các đối số cần thiết. Dưới đây là cú pháp chung:

##### python3 smtp-brute.py <mode> <wordlist> <user> <RHOST> <RPORT>

###### <mode>: Chế độ tấn công (userbrute hoặc passwordspray).
###### <wordlist>: Đường dẫn đến tệp chứa danh sách mật khẩu (hoặc người dùng nếu là chế độ passwordspray).
###### <user>: Tên tài khoản người dùng (đối với chế độ userbrute).
###### <RHOST>: Địa chỉ máy chủ SMTP.
###### <RPORT>: Cổng SMTP.
Ví dụ sử dụng
Giả sử bạn có một danh sách mật khẩu trong tệp passwordlist.txt, và bạn muốn thực hiện tấn công brute force trên máy chủ SMTP smtp.example.com qua cổng 465, đối với người dùng user@example.com. Bạn có thể chạy lệnh sau:

# python3 smtp-brute.py userbrute passwordlist.txt user@example.com smtp.example.com 465

# Lưu ý quan trọng

Bảo mật và pháp lý: Việc sử dụng script này để tấn công các hệ thống mà bạn không có quyền truy cập là trái pháp luật và có thể dẫn đến các hậu quả nghiêm trọng. Chỉ sử dụng script này trên các hệ thống mà bạn có quyền kiểm soát và đã được sự cho phép.
Kiểm tra và bảo trì: Đảm bảo rằng bạn đã kiểm tra và hiểu rõ các điều kiện và thông số của hệ thống mà bạn sẽ chạy script này.
