import os
import shutil

os.chdir("cuong gui\Vietnamese_hand_sign-main")
# Đường dẫn tới thư mục chứa 10 folder con
parent_folder_path = 'vietnamese_hand_sign_quan\classes temp'

# Đường dẫn tới thư mục chứa 10 vid
video_folder_path = 'Cut data\Cut video'

# Lấy danh sách tất cả các folder con trong thư mục cha
subfolders = [f.path for f in os.scandir(parent_folder_path) if f.is_dir()]
subfolders.sort()
print(len(subfolders))
# Lấy danh sách tất cả các vid trong thư mục vid
videos = [f for f in os.listdir(video_folder_path) if os.path.isfile(os.path.join(video_folder_path, f))]
print(len(videos))
# print(videos[10:18])
temp_videos = videos[10:18].copy()
temp_videos[0] = videos[17]
temp_videos[1:8] = videos[10:17]
videos[10:18] = temp_videos
videos[20], videos[21] = videos[21], videos[20]
videos[30], videos[31] = videos[31], videos[30]
# print(temp_videos)
# Đảm bảo số lượng folder con và video là như nhau
if len(subfolders) != len(videos):
    print("Số lượng folder con và video không khớp!")
    exit()

# Di chuyển các video vào từng folder con theo thứ tự
for i in range(len(subfolders)):
    video_path = os.path.join(video_folder_path, videos[i])
    destination_path = os.path.join(subfolders[i], videos[i])        
    print(video_path + "|" + destination_path)
    shutil.move(video_path, destination_path)

print("Hoàn thành việc di chuyển video vào các thư mục con!")
