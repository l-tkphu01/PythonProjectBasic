import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
class Plot:
    def __init__(self, file_path):
        # Đọc dữ liệu từ file CSV
        self.df = pd.read_csv(file_path, encoding='utf-8')
        print(f"Đã tải dữ liệu từ: {file_path}\n")

    #1. Đếm số lượng phim theo năm phát hành
    def hinh1(self):
        film_count_per_year = self.df['Năm phát hành'].value_counts().sort_index()

        plt.figure(figsize=(12, 8))
        plt.plot(film_count_per_year.index, film_count_per_year.values, marker='o', color='purple')
        plt.title('Số lượng phim phát hành theo thời gian', fontsize=14, fontweight='bold', color='darkblue')
        plt.xlabel('Năm phát hành', fontsize=13, fontweight='bold', color='darkblue')
        plt.ylabel('Số lượng phim', fontsize=13, fontweight='bold', color='darkblue')
        plt.xticks(np.arange(1960,2030,10))
        plt.grid()
        plt.savefig('SoLuongPhimPhatHanhTheoTungNam.png')
        plt.close()

    #2. 5 công ty sản xuất phim nhiều nhất piechart
    def hinh2(self):
        self.df['Công ty sản xuất'] = self.df['Công ty sản xuất'].fillna('Các công ty khác')

        company_counts = self.df['Công ty sản xuất'].value_counts()

        top_companies = company_counts.head(5)

        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']

        plt.figure(figsize=(12,8))

        plt.pie(top_companies, 
            labels=top_companies.index, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors,   
            shadow=True, 
            wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'linestyle': 'solid'}) 

        plt.title('5 công ty sản xuất phim nhiều nhất thống kê từ 1960 đến 2024', fontsize=16, fontweight='bold', color='darkblue')

        plt.legend(top_companies.index, title='Công ty sản xuất', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

        plt.savefig('Top5CongTyDungDauTrongViecSanXuatPhim.png')
        plt.close()


    #4. Top 10 thể loại phim được yêu thích nhất
    def hinh4(self):
        plt.figure(figsize=(12, 8))
        self.df["Thể loại"].value_counts()[:10].plot(kind="barh", color="orange")
        plt.title("Top 10 thể loại phim được yêu thích ",fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Số lượng', fontsize=12, fontweight='bold', color='darkblue')
        plt.ylabel('Thể loại', fontsize=12, fontweight='bold', color='darkblue')
        plt.savefig('Top10PhimDuocYeuThichNhat.png')
        plt.close()


    #5. Top 6 đạo diễn hàng đầu trong top 6 thể loại được yêu thích
    def hinh5(self):
        top_6_the_loai = self.df['Thể loại'].value_counts().head(6).index

        # Tạo figure với 3 hàng và 2 cột
        fig, axes = plt.subplots(3, 2, figsize=(10, 6)) #10, 6

        # Vẽ biểu đồ cho từng thể loại
        for i in range(6):
            row = i // 2
            col = i % 2
    
            loai = top_6_the_loai[i]
            frame = self.df[self.df['Thể loại'] == loai]
    
            top_6_dao_dien = frame['Đạo diễn'].value_counts().head(6).index
    
            # Tạo biểu đồ đếm số lượng phim cho từng đạo diễn
            sns.countplot(x='Đạo diễn', data=frame[frame['Đạo diễn'].isin(top_6_dao_dien)], ax=axes[row, col], palette='Set2')
    
            axes[row, col].set_title('Top 6 Đạo diễn trong top 6 thể loại: ' + loai, fontsize=12, fontweight='bold')
            axes[row, col].set_ylabel('Số lượng phim', fontsize=8, fontweight='bold')
            axes[row, col].set_xlabel('Đạo diễn', fontsize=8, fontweight='bold')

            axes[row, col].set_xticklabels(top_6_dao_dien, rotation=45, ha='right', fontsize=8)

        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=1.0)
        plt.tight_layout()
        plt.savefig('Top6DaoDienDungDauTrongViecSanXuatPhim.png')
        plt.close()
    
    #6. Ngân sách theo từng năm
    def hinh6(self):
        # self.df['Ngân sách'] = self.df['Ngân sách'] / 1e6
        yearly_budget = self.df.groupby('Năm phát hành')['Ngân sách'].sum() 

        plt.figure(figsize=(8, 6))
        plt.bar(yearly_budget.index, yearly_budget.values, color='skyblue', edgecolor='black')

        plt.title('Ngân sách qua từng năm (triệu USD)', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Năm', fontsize=14, fontweight='bold')
        plt.ylabel('Ngân sách (triệu USD)', fontsize=14, fontweight='bold')

        plt.xticks(np.arange(yearly_budget.index.min(), yearly_budget.index.max() + 1, step=5), rotation=45, fontsize=10)
        plt.yticks(fontsize=12)

        plt.tight_layout()
        plt.savefig('NganSachTheoTungNam.png')
        plt.close()
    
    def hinh7(self):
        plt.figure(figsize=(8, 6))
        # Tính toán ma trận tương quan
        numeric_columns = ['Độ phổ biến', 'Ngân sách', 'Doanh thu', 'Thời lượng', 
                           'Số phiếu bầu', 'Điểm trung bình', 'Ngân sách điều chỉnh', 'Doanh thu điều chỉnh']
        correlation_matrix = self.df[numeric_columns].corr()
        
        # Vẽ biểu đồ heatmap để hiển thị mối tương quan
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Ma trận tương quan giữa các cột số')
        plt.xticks(rotation=45, fontsize=8)
        plt.savefig('TuongQuanGiuaCacCotSo.png')
        plt.close()
    
    def hinh8(self):
        # Chuẩn bị dữ liệu
        self.df['Ngày phát hành'] = pd.to_datetime(self.df['Ngày phát hành'], errors='coerce')
        self.df['Năm phát hành'] = self.df['Ngày phát hành'].dt.year
        self.df['Doanh thu'] = pd.to_numeric(self.df['Doanh thu'], errors='coerce')
        self.df['Thể loại'] = self.df['Thể loại'].str.split('|').str[0]

        self.df = self.df.dropna(subset=['Doanh thu', 'Năm phát hành', 'Thể loại'])

        # Lấy danh sách tất cả các năm trong khoảng từ năm nhỏ nhất đến năm lớn nhất
        all_years = pd.Series(range(int(self.df['Năm phát hành'].min()), int(self.df['Năm phát hành'].max() + 1)))

        # Tổng hợp dữ liệu doanh thu theo năm và thể loại
        area_data = self.df.groupby(['Năm phát hành', 'Thể loại'])['Doanh thu'].sum().unstack(fill_value=0)

        # Đảm bảo tất cả các năm đều có mặt
        area_data = area_data.reindex(all_years, fill_value=0)
        # Vẽ biểu đồ miền
        plt.figure(figsize=(12, 8))
        area_data.plot.area(alpha=0.7, colormap='Spectral', figsize=(12, 8))
        # Thêm tiêu đề và nhãn
        plt.title('Doanh thu của từng thể loại phim theo năm', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Năm phát hành', fontsize=12, fontweight='bold', color='darkblue')
        plt.ylabel('Doanh thu (triệu USD)', fontsize=12, fontweight='bold', color='darkblue')
        # plt.xticks(np.arange(1960,2030,10), rotation=45)
        # Hiển thị biểu đồ
        plt.legend(title='Thể loại phim', fontsize=10)
        plt.grid(axis='y', linestyle='--', linewidth=0.7)
        plt.savefig('DoanhThuTungTheLoaiTheoTungNam.png')
        plt.close()
    
    def hinh9(self):
        #6 Từ khóa
        keywords = ' '.join(self.df['Từ khóa'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(keywords)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('CacTuKhoaPhoBien.png')
        plt.close()
    
    def hinh10(self):
        # Đảm bảo xử lý đúng định dạng tháng/ngày/năm
        self.df['Ngày phát hành'] = pd.to_datetime(self.df['Ngày phát hành'], format='%m/%d/%Y', errors='coerce')

        # Lọc những hàng có giá trị hợp lệ
        self.df = self.df.dropna(subset=['Ngày phát hành'])

        # Trích xuất năm và tháng từ ngày phát hành
        self.df['Nam'] = self.df['Ngày phát hành'].dt.year
        self.df['Thang'] = self.df['Ngày phát hành'].dt.month

        # Đếm số lượng phim theo năm và tháng
        heatmap_data = self.df.groupby(['Nam', 'Thang']).size().unstack(fill_value=0)

        # Vẽ heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            heatmap_data, 
            cmap='YlGnBu',
            annot=True,
            fmt='d',
            linewidths=0.5,
            cbar_kws={'label': 'Số lượng phim'},
            annot_kws={"size": 8}
        )
        # Thêm tiêu đề và nhãn
        plt.title('Số lượng phim phát hành theo tháng', fontsize=16, fontweight='bold')
        plt.xlabel('Tháng', fontsize=12)
        plt.ylabel('Năm phát hàng', fontsize=12)
        plt.savefig('SoLuongPhimPhatHanhTheoTungThang.png')
        plt.close()
    
    def hinh11(self):
        self.df['Doanh thu'] = pd.to_numeric(self.df['Doanh thu'].astype(str).str.replace(',', ''), errors='coerce')
        self.df['Thể loại'] = self.df['Thể loại'].str.split('|').str[0]

        # Lọc bỏ giá trị NaN
        self.df = self.df.dropna(subset=['Doanh thu', 'Thể loại', 'Ngày phát hành'])

        # Thêm cột 'Tháng' từ cột 'Ngày phát hành'
        self.df['Thang'] = self.df['Ngày phát hành'].dt.month

        # Nhóm dữ liệu theo Thể loại và Tháng, tính tổng doanh thu
        revenue_by_genre_month = self.df.groupby(['Thể loại', 'Thang'])['Doanh thu'].sum().unstack(fill_value=0)

        # Vẽ biểu đồ
        plt.figure(figsize=(14, 8))
        revenue_by_genre_month.T.plot(kind='bar', stacked=True, figsize=(14, 8), cmap='tab20')
        # Thêm tiêu đề và nhãn
        plt.title('Tổng doanh thu thể loại phim theo tháng ra mắt', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Tháng', fontsize=12, fontweight='bold', color='darkblue')
        plt.ylabel('Tổng doanh thu (triệu USD)', fontsize=12, fontweight='bold', color='darkblue')
        plt.legend(title='Thể loại phim', fontsize=10, bbox_to_anchor=(1, 1), loc='upper left')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', linewidth=0.7)
        plt.savefig('TongDoanhThuTungTheLoaiPhimTheoTungThang.png')
        plt.close()
    
    def hinh12(self):
        #12.Doan thu trung bình của thể loại
        self.df['Doanh thu'] = pd.to_numeric(self.df['Doanh thu'].astype(str).str.replace(',', ''), errors='coerce')
        self.df['Thể loại'] = self.df['Thể loại'].str.split('|').str[0]

        # Lọc bỏ giá trị NaN
        self.df = self.df.dropna(subset=['Doanh thu', 'Thể loại'])

        # Tính tổng doanh thu và số lượng phim cho mỗi thể loại
        revenue_by_genre = self.df.groupby('Thể loại')['Doanh thu'].sum()
        count_by_genre = self.df.groupby('Thể loại')['Doanh thu'].count()

        # Tính doanh thu trung bình
        average_revenue_by_genre = revenue_by_genre / count_by_genre

        # Vẽ biểu đồ doanh thu trung bình theo thể loại
        plt.figure(figsize=(12, 8))
        sns.barplot(
            x=average_revenue_by_genre.index,
            y=average_revenue_by_genre.values,
            palette='coolwarm'
        )

        # Thêm tiêu đề và nhãn
        plt.title('Doanh thu trung bình của từng thể loại phim', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Thể loại phim', fontsize=12, fontweight='bold', color='darkblue')
        plt.ylabel('Doanh thu trung bình (triệu USD)', fontsize=12, fontweight='bold', color='darkblue')
        plt.xticks(rotation=45, ha='right')  # Đặt góc xoay cho các nhãn trục x
        plt.grid(axis='y', linestyle='--', linewidth=0.7)
        plt.savefig('DoanhThuTrungBinhTungTheLoaiPhim.png')
        plt.close()
    
    def hinh13(self):
        # Chuẩn bị dữ liệu
        self.df['Ngày phát hành'] = pd.to_datetime(self.df['Ngày phát hành'], errors='coerce')
        self.df['Năm phát hành'] = self.df['Ngày phát hành'].dt.year
        self.df['Ngân sách'] = pd.to_numeric(self.df['Ngân sách'], errors='coerce')
        self.df['Thể loại'] = self.df['Thể loại'].str.split('|').str[0]

        self.df = self.df.dropna(subset=['Ngân sách', 'Năm phát hành', 'Thể loại'])

        # Lấy danh sách tất cả các năm trong khoảng từ năm nhỏ nhất đến năm lớn nhất
        all_years = pd.Series(range(int(self.df['Năm phát hành'].min()), int(self.df['Năm phát hành'].max() + 1)))

        # Tổng hợp dữ liệu doanh thu theo năm và thể loại
        area_data = self.df.groupby(['Năm phát hành', 'Thể loại'])['Ngân sách'].sum().unstack(fill_value=0)

        # Đảm bảo tất cả các năm đều có mặt
        area_data = area_data.reindex(all_years, fill_value=0)
        # Vẽ biểu đồ miền
        plt.figure(figsize=(12, 8))
        area_data.plot.area(alpha=0.7, colormap='Spectral', figsize=(12, 8))
        # Thêm tiêu đề và nhãn
        plt.title('Ngân sách của từng thể loại phim theo năm', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Năm phát hành', fontsize=12, fontweight='bold', color='darkblue')
        plt.ylabel('Ngân sách (triệu USD)', fontsize=12, fontweight='bold', color='darkblue')
        # plt.xticks(np.arange(1960,2030,10), rotation=45)
        # Hiển thị biểu đồ
        plt.legend(title='Thể loại phim', fontsize=10)
        plt.grid(axis='y', linestyle='--', linewidth=0.7)
        plt.savefig('NganSachTungTheLoaiPhimTheoTungNam.png')
        plt.close()
                
def main():

    # Đảm bảo rằng bạn thay đổi đường dẫn đúng tới file dữ liệu của mình
    file_path = 'Data/Cleaned_DataFile.csv'  # Đường dẫn tới file CSV của bạn
    plot = Plot(file_path)

    plot.hinh1()
    plot.hinh2()
    plot.hinh4()
    plot.hinh5()
    plot.hinh6()
    plot.hinh7()
    plot.hinh8()
    plot.hinh9()
    plot.hinh10()
    plot.hinh11()
    plot.hinh12()
    plot.hinh13()

if __name__ == "__main__":
    main()

