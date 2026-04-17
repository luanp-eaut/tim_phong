# Công cụ tìm phòng học trống tại EAUT

## Cài đặt & Chuẩn bị dữ liệu

Để ứng dụng chạy chính xác, hãy thực hiện đúng các bước sau:

1.  **Tải dữ liệu:** Tải file thông tin lịch học từ qldt về máy dưới dạng file **.csv**.
2.  **Chuyển đổi định dạng:** Mở file .csv và lưu lại (Save As) sang định dạng **.xlsx**. Đặt tên file là `lich_hoc.xlsx`. (Mở trực tiếp từ excel thì hơi phức tạp, phải dùng Get Data, tốt nhất là upload lên google drive, mở bằng google sheet rồi tải về dạng .xslx).
3.  **Làm sạch dữ liệu:**
    * **Xoá các dòng trống hoặc dòng tiêu đề phụ** ở đầu file để cho dòng chứa tiêu đề cột (Phòng học, T2, T3...) là dòng đầu tiên.
    * **Đổi tên các cột** ngày trong tuần thành đúng định dạng: `T2`, `T3`, `T4`, `T5`, `T6`, `T7`, `CN`.
4.  **Sắp xếp thư mục:** Tạo một thư mục có tên là `data` trong thư mục dự án và copy file `lich_hoc.xlsx` vào đó.
    * Cấu trúc: `[Thư mục dự án]/data/lich_hoc.xlsx`
5.  **Cài đặt thư viện:**
    ```bash
    pip install pandas openpyxl
    ```

## Chạy ứng dụng

Mở Terminal/Command Prompt tại thư mục dự án và chạy lệnh:
```bash
python app.py
```

Ứng dụng sẽ yêu cầu nhập thông tin qua các bước:

1.  **Sức chứa tối thiểu:** Nhập sức chứa tối thiểu (ví dụ: `50`).
2.  **Chọn ca học (T2 -> CN):**
    * Nhập danh sách ca (ví dụ: `1 2 5`).
    * Nhập `*` để chọn tất cả các ca trong ngày.
    * Nhập `0` nếu không muốn kiểm tra ngày đó.

## Kết quả
Sau khi hoàn thành, file **`result.xlsx`** sẽ được tạo ra tại thư mục data, liệt kê danh sách các phòng thỏa mãn điều kiện kèm theo chi tiết các ca trống.