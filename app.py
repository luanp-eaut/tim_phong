import pandas as pd
import re

SLOTS_TIME = {
    1: "07:00-09:30", 2: "09:40-12:10", 3: "13:00-15:30",
    4: "15:40-18:10", 5: "18:30-21:00"
}
DAYS_LIST = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']

def parse_capacity(room_string):
    """Trích xuất sức chứa từ chuỗi định dạng 'Tên_Phòng(Sức_Chứa)'"""
    match = re.search(r'\((\d+)\)', str(room_string))
    return int(match.group(1)) if match else 0

def load_data(file_path):
    """Đọc dữ liệu từ file Excel"""
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Lỗi: Không thể đọc file '{file_path}'. Chi tiết: {e}")
        return None

def get_actual_columns(df):
    """Ánh xạ các cột thực tế trong file dựa trên danh sách ngày"""
    actual_columns = {}
    for d in DAYS_LIST:
        col_name = [c for c in df.columns if str(c).startswith(d)]
        if col_name:
            actual_columns[d] = col_name[0]
    return actual_columns

def get_user_requirements():
    """Thu thập yêu cầu về sức chứa và ca học từ người dùng"""
    try:
        min_cap = int(input("Sức chứa tối thiểu: "))
    except ValueError:
        print("Sức chứa phải là số nguyên.")
        return None, None

    user_requests = {}
    print("\nNhập các ca cần kiểm tra (*: tất cả, 0: bỏ qua, hoặc liệt kê ca 1 2...):")
    for d in DAYS_LIST:
        user_requests[d] = get_slots(d)
    
    return min_cap, user_requests

def get_slots(day_name):
    """Hàm nội bộ để xử lý nhập liệu cho từng ngày"""
    while True:
        choice = input(f"{day_name}: ").strip()
        if choice == '*': return list(SLOTS_TIME.keys())
        if choice == '0': return []
        try:
            return [int(s) for s in choice.split() if int(s) in SLOTS_TIME]
        except ValueError:
            print("Vui lòng nhập số cách nhau bằng khoảng trắng.")

def find_available_rooms(df, min_capacity, user_requests, actual_columns):
    """Lọc các phòng thỏa mãn điều kiện"""
    results = []

    for _, row in df.iterrows():
        room_name = row['Phòng học']
        capacity = parse_capacity(room_name)

        if capacity < min_capacity:
            continue

        matching_details = []
        for d, requested_slots in user_requests.items():
            if not requested_slots: 
                continue
                
            col_name = actual_columns.get(d)
            content = str(row[col_name]) if col_name and pd.notna(row[col_name]) else ""
            
            for slot in requested_slots:
                # Nếu thời gian của ca KHÔNG xuất hiện trong nội dung cột -> Ca đó trống
                if SLOTS_TIME[slot] not in content:
                    matching_details.append(f"{d}-Ca{slot}")

        if matching_details:
            results.append({
                'Phòng học': room_name,
                'Sức chứa': capacity,
                'Các ca trống khớp yêu cầu': ", ".join(matching_details)
            })
    
    return results

def main():
    input_file = 'data/lich_hoc.xlsx'
    output_file = 'data/result.xlsx'

    df = load_data(input_file)
    if df is None: return

    min_capacity, user_requests = get_user_requirements()
    if min_capacity is None: return

    actual_columns = get_actual_columns(df)
    results = find_available_rooms(df, min_capacity, user_requests, actual_columns)

    if results:
        pd.DataFrame(results).to_excel(output_file, index=False)
        print(f"\n--- Tìm thấy {len(results)} phòng. Đã lưu vào {output_file} ---")
    else:
        print("\nKhông tìm thấy phòng nào phù hợp.")

if __name__ == "__main__":
    main()