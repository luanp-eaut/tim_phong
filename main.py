import pandas as pd

def process_empty_slots(input_file, output_file):
    # 1. Đọc file excel
    # Lưu ý: Điều chỉnh sheet_name hoặc skip_rows nếu file của bạn có tiêu đề phụ
    df = pd.read_excel(input_file)

    # Định nghĩa các khung giờ tương ứng với 5 ca
    slots = {
        "Ca 1": "07:00-09:30",
        "Ca 2": "09:40-12:10",
        "Ca 3": "13:00-15:30",
        "Ca 4": "15:40-18:10",
        "Ca 5": "18:30-21:00"
    }

    days = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
    
    # Danh sách để chứa dữ liệu kết quả
    result_data = []

    # 2. Duyệt qua từng hàng (từng phòng học)
    for index, row in df.iterrows():
        room_info = {
            'Phòng học': row['Phòng học']
        }
        
        # Duyệt qua từng ngày trong tuần
        for day in days:
            content = str(row[day]) if pd.notna(row[day]) else ""
            empty_slots_in_day = []
            
            # Kiểm tra từng ca xem có xuất hiện trong nội dung không
            for slot_name, time_range in slots.items():
                if time_range not in content:
                    empty_slots_in_day.append(slot_name)
            
            # Nối các ca trống thành chuỗi để ghi vào cell
            room_info[day] = ", ".join(empty_slots_in_day) if empty_slots_in_day else "Full"
            
        result_data.append(room_info)

    # 3. Tạo DataFrame kết quả và xuất ra Excel
    result_df = pd.DataFrame(result_data)
    
    # Sắp xếp lại thứ tự cột cho đẹp
    cols = ['Phòng học'] + days
    result_df = result_df[cols]
    
    # Xuất file
    result_df.to_excel(output_file, index=False)
    print(f"Đã hoàn thành! File lưu tại: {output_file}")

# Sử dụng hàm
# process_empty_slots('lich_hoc.xlsx', 'lich_trong_cac_phong.xlsx')
if __name__ == "__main__":
    input_file = 'data/lich_hoc.xlsx'  # Đường dẫn đến file excel đầu vào
    output_file = 'data/lich_trong_cac_phong.xlsx'  # Đường dẫn đến file excel đầu ra
    process_empty_slots(input_file, output_file)