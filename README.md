# Hướng dẫn sử dụng PVO Community Version (PVOCV)
## Lưu ý trước khi sử dụng 
- Đây không phải một bản PVO Web chính thức của thầy Vũ.
- Hiện tại chỉ có cách chuyển dữ liệu từ PVO sang PVOCV chứ không có cách để chuyển dữ liệu từ PVOCV sang PVO. Mình sẽ cố gắng để có thể chuyển dữ liệu từ PVOCV sang PVO Web chính thức của thầy để đảm bảo quyền lợi cho người dùng, nhưng mình không hứa trước được.
## Đăng kí tài khoản
- Vào http://64.154.38.216:5000/
- Nhập username và password mà bạn muốn (lưu ý không nên chọn username / password liên quan đến thông tin cá nhân, đề phòng trường hợp bị kẻ xấu tấn công server).
- Nhấn Register để tạo tài khoản và tự động đăng nhập lần đầu.
- Lưu ý rằng nếu bạn quên tên tài khoản hoặc mật khẩu thì không có cách nào khôi phục lại tài khoản.
## Nạp dữ liệu từ PVO vào PVOCV
- Lưu ý: Khi nạp dữ liệu từ PVO vào PVOCV, dữ liệu hiện tại của bạn ở PVOCV sẽ bị xóa toàn bộ và được thay thế bằng dữ liệu trong PVO
- Tải tệp `converter.exe` tại [đây](https://drive.google.com/file/d/1yBGy-4lw7Pe4A546ei_G3lyRrdy3Onwg/view?usp=sharing)
- Đặt tệp này cùng với thư mục chứa tệp `.mdb` của bạn trong PVO. Thường tệp này có tên là `Default.mdb`
- Chạy file `converter.exe`, nhập tên tệp `.mdb` (bao gồm cả đuôi `.mdb`). Ví dụ: `Default.mdb`
- Chương trình sẽ xuất ra hai tệp `file1.csv` và `file2.csv` ở cùng thư mục với tệp `Default.mdb`. Dùng Notepad để mở hai tệp này (không mở hai tệp này bằng Excel)
- Đăng nhập vào [PVOCV](http://64.154.38.216:5000/), vào phần [Backup](http://64.154.38.216:5000/backup).
- Xóa nội dung hiện có trong hai ô trống, rồi nhập nội dung của hai file vào hai ô trống tương ứng, rồi nhấn `Load`.
- Đợi cho đến khi dòng chữ `Your data have been loaded` hiện ra
- Chuyển sang phần [Visualizer](http://64.154.38.216:5000/visualizer) để xem thành quả
## Các tính năng còn lại trên PVOCV
- Mình chưa có thời gian hướng dẫn, nên nếu bạn thích bạn có thể tự vọc.
- Lưu ý rằng bạn hoàn toàn có thể dùng PVO bản cũ, rồi chạy `converter.exe` để sinh `file1.csv` và `file2.csv` mới và nạp lại hai file này vào PVOCV 
