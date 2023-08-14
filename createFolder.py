import os

os.chdir("cuong gui\Vietnamese_hand_sign-main")
folder_path = 'vietnamese_hand_sign\classes_point_2'  # Đường dẫn tới thư mục xác định
alphabet = "alphabet.txt"

with open(alphabet, 'r') as file:
    lines = file.readlines()  # Đọc từng dòng trong file
    
    for line in lines:
        char = line.strip()  # Loại bỏ khoảng trắng và ký tự xuống dòng
        if char:  # Kiểm tra xem chuỗi không rỗng
            folder_name = "Class " + char
            folder_name = ''.join(c for c in folder_name if c not in r'\/:*?"<>|')  # Loại bỏ ký tự không hợp lệ từ tên thư mục
            folder_path_with_name = os.path.join(folder_path, folder_name)
            os.makedirs(folder_path_with_name, exist_ok=True)
