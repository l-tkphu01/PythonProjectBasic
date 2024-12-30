import CleanData
import NewData
import GUI
import SourceCode.Mat_plotlib as Mat_plotlib
def main():
    # Lọc dữ liệu (Class CleanData)
    CleanData.CleanData

    # Phát sinh thêm dữ liệu sau khi lọc (NewData)
    NewData.NewData

    Mat_plotlib.main()
    
    GUI.main()

if __name__ == "__main__":
    main()


