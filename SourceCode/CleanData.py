import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os
import time

class CleanData:
    print('\n' + '-' * 120 + '\n')
    print(" " * 50 + "========= Lọc dữ liệu =========\n")
    
    start_time = time.time()  # Ghi nhận thời gian bắt đầu
    
    try:
        # Đọc file CSV với các tùy chọn phù hợp
        df = pd.read_csv(
            'Data/DataFile.csv',
            encoding='utf-8',
            sep=',',
            quotechar='"',
            skip_blank_lines=True,
            on_bad_lines='skip'
        )
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        exit()

    # 1. Xử lý giá trị trống (NaN hoặc Null)
    default_values = {
        'runtime': 0,                # Thay giá trị trống trong cột số
        'keywords': 'unknown'        # Thay giá trị trống trong cột chuỗi
    }
    df.fillna(default_values, inplace=True)

    # 2. Xử lý lỗi định dạng ngày tháng
    date_columns = ['release_date']  # Danh sách cột ngày tháng
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')  # Chuyển đổi sang kiểu datetime
            df[col] = df[col].dt.strftime('%d/%m/%Y')  # Chuẩn hóa định dạng ngày

    # 4. Loại bỏ các dòng trùng lặp
    df.drop_duplicates(inplace=True)

    # 5. Chuẩn hóa cột chuỗi (loại bỏ khoảng trắng, chuyển chữ thường)
    string_columns = ['genres', 'keywords']  # Danh sách các cột chuỗi
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower().fillna('unknown')  # Chuẩn hóa chữ thường và loại bỏ khoảng trắng

    # 8. Loại bỏ các cột không cần thiết
    columns_to_drop = ['homepage']  # Cột không cần thiết
    df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

    # 9. Chuẩn hóa tên cột (tiếng Việt)
    column_translation = {
        'id': 'Mã',
        'imdb_id': 'Mã imdb',
        'popularity': 'Độ phổ biến',
        'budget': 'Ngân sách',
        'revenue': 'Doanh thu',
        'original_title': 'Tựa gốc',
        'cast': 'Dàn diễn viên',
        'homepage': 'Trang chủ',
        'director': 'Đạo diễn',
        'tagline': 'Khẩu hiệu',
        'keywords': 'Từ khóa',
        'overview': 'Tóm tắt',
        'runtime': 'Thời lượng',
        'genres': 'Thể loại',
        'production_companies': 'Công ty sản xuất',
        'release_date': 'Ngày phát hành',
        'vote_count': 'Số phiếu bầu',
        'vote_average': 'Điểm trung bình',
        'release_year': 'Năm phát hành',
        'budget_adj': 'Ngân sách điều chỉnh',
        'revenue_adj': 'Doanh thu điều chỉnh'
    }
    df.rename(columns=column_translation, inplace=True)

    # 10. Loại bỏ dòng không hợp lệ (ví dụ: doanh_thu < ngân_sách)
    if 'doanh_thu' in df.columns and 'ngân_sách' in df.columns:
        df = df[df['doanh_thu'] >= df['ngân_sách']]

    # 11. Chuẩn hóa đơn vị đo lường
    if 'thời_lượng' in df.columns:
        df['thời_lượng'] = df['thời_lượng'].apply(lambda x: x * 60 if x < 5 else x)  # Giả định: thời_lượng < 5 là giờ, chuyển sang phút

    # 12. Loại bỏ cột hoặc dòng trống hoàn toàn
    df.dropna(axis=1, how='all', inplace=True)  # Loại bỏ cột trống
    df.dropna(axis=0, how='any', inplace=True)  # Loại bỏ dòng có bất kỳ giá trị NaN nào

    # 14. Thêm cột số thứ tự (STT)
    df.insert(0, 'STT', range(1, len(df) + 1))  # Thêm cột STT vào đầu DataFrame, bắt đầu từ 1

    # 15. Kiểm tra và thay thế năm phát hành nếu ngày không hợp lệ
    if 'Ngày phát hành' in df.columns and 'Năm phát hành' in df.columns:
    # Lấy ngày phát hành và chuyển đổi sang kiểu datetime
        df['Ngày phát hành'] = pd.to_datetime(df['Ngày phát hành'], format='%d/%m/%Y', errors='coerce')

        # Thay đổi năm của ngày phát hành thành năm từ 'Năm phát hành' và giữ nguyên ngày/tháng
        df['Ngày phát hành'] = df.apply(
            lambda row: row['Ngày phát hành'].replace(year=row['Năm phát hành']).strftime('%d/%m/%Y') 
            if pd.notnull(row['Ngày phát hành']) else row['Ngày phát hành'],
            axis=1
        )

    end_time = time.time()  # Ghi nhận thời gian kết thúc

    # Hàm dự đoán giá trị thiếu bằng mô hình học máy
    def predict_missing_values(df, target_column, feature_columns):
        # Tách dữ liệu thành 2 phần: có giá trị và không có giá trị
        known_data = df[df[target_column] > 0]  # Những hàng có giá trị target_column
        unknown_data = df[df[target_column] == 0]  # Những hàng có giá trị bằng 0
        
        # Nếu không có giá trị target_column, không thể huấn luyện mô hình
        if known_data.empty:
            print(f"No known data to train the model for {target_column}.")
            return df

        # Chia dữ liệu thành X (features) và y (target)
        X = known_data[feature_columns]
        y = known_data[target_column]

        # Huấn luyện mô hình Random Forest
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        # Dự đoán giá trị cho các dòng có target_column = 0
        X_unknown = unknown_data[feature_columns]
        predictions = model.predict(X_unknown)

        # Gán giá trị dự đoán vào cột target_column
        df.loc[df[target_column] == 0, target_column] = predictions

        return df
    
    # Các cột feature để huấn luyện mô hình
    feature_columns = ['Độ phổ biến', 'Số phiếu bầu', 'Điểm trung bình', 'Thời lượng', 'Năm phát hành']

    # Dự đoán giá trị cho 'Ngân sách' và 'Doanh thu'
    df = predict_missing_values(df, 'Ngân sách', feature_columns)
    df = predict_missing_values(df, 'Doanh thu', feature_columns)
    

    # 15. Lưu file kết quả vào thư mục 'Data' sau khi dự đoán giá trị thiếu
    output_dir = 'Data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_with_predictions = os.path.join(output_dir, 'Cleaned_DataFile.csv')
    df.to_csv(output_file_with_predictions, index=False, encoding='utf-8')
    print(f"File kết quả sau khi dự đoán đã được lưu tại: '{output_file_with_predictions}'")

    execution_time = end_time - start_time  # Tính thời gian thực hiện
    print(f"\nThời gian thực hiện: {execution_time:.2f} giây")

    print('\n' + '-' * 120)
