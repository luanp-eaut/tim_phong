import pandas as pd
import re

def parse_capacity(room_string):
    """Trích xuất sức chứa từ chuỗi định dạng 'Tên_Phòng(Sức_Chứa)'"""
    match = re.search(r'\((\d+)\)', str(room_string))
    if match:
        return int(match.group(1))
    return 0

def get_user_input(day_name):
    """Hàm xử lý nhập liệu ca học cho từng ngày"""
    while True:
        prompt = f"{day_name} [*: tất cả ca, 0: không chọn, hoặc liệt kê ca 1 2...]: "
        choice = input(prompt).strip()
        
        if choice == '*':
            return [1, 2, 3, 4, 5]
        if choice == '0':
            return []
        
        try:
            selected_slots = [int(s) for s in choice.split() if s in ['1', '2', '3', '4', '5']]
            return selected_slots
        except ValueError:
            print("Vui lòng nhập đúng định dạng số cách nhau bằng khoảng trắng.")

def main():
    input_file = 'data/lich_hoc.xlsx'
    output_file = 'data/result.xlsx'

    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Lỗi: Không tìm thấy file '{input_file}'.")
        return

    # 1. Nhập sức chứa tối thiểu
    try:
        min_capacity = int(input("1. Sức chứa tối thiểu: "))
    except ValueError:
        print("Sức chứa phải là số nguyên.")
        return

    # 2. Xử lý tiêu đề cột ngày tháng
    days_list = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
    actual_columns = {}
    for d in days_list:
        col_name = [c for c in df.columns if str(c).startswith(d)]
        if col_name:
            actual_columns[d] = col_name[0]

    # 3. Thu thập yêu cầu
    user_requests = {}
    print("\nNhập các ca cần kiểm tra:")
    for d in days_list:
        user_requests[d] = get_user_input(d)

    slots_time = {
        1: "07:00-09:30", 2: "09:40-12:10", 3: "13:00-15:30",
        4: "15:40-18:10", 5: "18:30-21:00"
    }

    results = []

    # 4. Kiểm tra logic OR
    for _, row in df.iterrows():
        room_name = row['Phòng học']
        capacity = parse_capacity(room_name)

        if capacity >= min_capacity:
            matching_details = [] # Lưu thông tin ca nào trống để ghi vào file
            
            for d, requested_slots in user_requests.items():
                if not requested_slots: continue
                
                col_name = actual_columns.get(d)
                content = str(row[col_name]) if col_name and pd.notna(row[col_name]) else ""
                
                for slot in requested_slots:
                    if slots_time[slot] not in content:
                        matching_details.append(f"{d}-Ca{slot}")
            
            # Nếu có ít nhất một ca trống khớp yêu cầu
            if matching_details:
                results.append({
                    'Phòng học': room_name,
                    'Sức chứa': capacity,
                    'Các ca trống khớp yêu cầu': ", ".join(matching_details)
                })

    # 5. Xuất kết quả
    if results:
        result_df = pd.DataFrame(results)
        result_df.to_excel(output_file, index=False)
        print(f"\n--- THÀNH CÔNG ---")
        print(f"Đã tìm thấy {len(results)} phòng phù hợp.")
        print(f"Kết quả đã được lưu vào file: {output_file}")
    else:
        print("\nKhông tìm thấy phòng nào khớp với yêu cầu của bạn.")

if __name__ == "__main__":
    main()