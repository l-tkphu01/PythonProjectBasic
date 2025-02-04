import pandas as pd
import os
import datetime
import time  # Import module time

class NewData:
    print("\n" + " " * 47 + "========= Phát sinh dữ liệu =========\n")
    
    # Ghi nhận thời gian bắt đầu
    start_time = time.time()

    # Đọc file dữ liệu gốc
    input_file = 'Data/Cleaned_DataFile.csv'

    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        exit()

    # Xử lý dữ liệu và thêm các cột phân tích

    # 2. Hiệu suất doanh thu
    df['Hiệu suất doanh thu'] = df['Doanh thu'] / df['Ngân sách']
    df['Hiệu suất doanh thu'] = df['Hiệu suất doanh thu'].fillna(0)

    # 3. Thể loại chính
    df['Thể loại chính'] = df['Thể loại'].apply(lambda x: x.split('|')[0] if isinstance(x, str) else 'unknown')

    # 4. Mức độ phổ biến
    max_popularity = df['Độ phổ biến'].max()
    max_popularity = max(max_popularity, 101)  # Ensure the highest bin edge is strictly greater than 100
    df['Mức độ phổ biến'] = pd.cut(
        df['Độ phổ biến'],
        bins=[0, 10, 50, 100, max_popularity],
        labels=['Thấp', 'Trung bình', 'Cao', 'Rất cao'],
        right=False
    )

    # 5. Số lượng diễn viên
    df['Số lượng diễn viên'] = df['Dàn diễn viên'].apply(lambda x: len(x.split('|')) if isinstance(x, str) else 0)

    # 6. Mùa phát hành
    def classify_season(date):
        if pd.isna(date):
            return 'unknown'
        try:
            month = pd.to_datetime(date, format='%d/%m/%Y', errors='coerce').month
            if month in [12, 1, 2]:
                return 'Đông'
            elif month in [3, 4, 5]:
                return 'Xuân'
            elif month in [6, 7, 8]:
                return 'Hạ'
            else:
                return 'Thu'
        except Exception:
            return 'unknown'

    df['Mùa phát hành'] = df['Ngày phát hành'].apply(classify_season)

    # 7. Loại thời lượng
    max_runtime = df['Thời lượng'].max()
    max_runtime = max(max_runtime, 121)  # Ensure the highest bin edge is strictly greater than 120
    df['Loại thời lượng'] = pd.cut(
        df['Thời lượng'],
        bins=[0, 90, 120, max_runtime],
        labels=['Ngắn', 'Trung bình', 'Dài'],
        right=False
    )

    # 8. Phân loại bình chọn
    max_votes = df['Số phiếu bầu'].max()
    max_votes = max(max_votes, 1001)  # Ensure the highest bin edge is strictly greater than 1000
    df['Phân loại bình chọn'] = pd.cut(
        df['Số phiếu bầu'],
        bins=[0, 100, 1000, max_votes],
        labels=['Ít', 'Trung bình', 'Nhiều'],
        right=False
    )

    # 9. Chênh lệch điều chỉnh
    df['Chênh lệch điều chỉnh'] = df['Doanh thu điều chỉnh'] - df['Ngân sách điều chỉnh']

    # 10. Số phim của đạo diễn
    df['Số phim của đạo diễn'] = df.groupby('Đạo diễn')['Đạo diễn'].transform('count')

    # 11. Số lượng công ty sản xuất
    df['Số lượng công ty sản xuất'] = df['Công ty sản xuất'].apply(lambda x: len(x.split('|')) if isinstance(x, str) else 0)

    # 12. Số năm từ khi phát hành
    current_year = datetime.datetime.now().year
    df['Số năm từ khi phát hành'] = current_year - df['Năm phát hành']

    # 13. Đánh giá tổng quan phim
    df['Đánh giá'] = pd.cut(
        df['Điểm trung bình'],
        bins=[0, 5, 7, 10],
        labels=['Tệ', 'Khá', 'Xuất sắc']
    )

    # Lưu file kết quả
    output_dir = 'Data'
    output_file = os.path.join(output_dir, 'Enhanced_DataFile.csv')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"File dữ liệu được phân tích và lưu thành công tại: {output_file}")
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")

    # Ghi nhận thời gian kết thúc
    end_time = time.time()

    # Tính toán và in thời gian chạy
    execution_time = end_time - start_time
    print(f"\nThời gian chạy: {execution_time:.2f} giây.")
    print("\n" + " " * 42 + "========= Kết thúc phát sinh dữ liệu =========\n")
    print('-' * 120)
