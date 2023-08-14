import os
import ffmpeg


os.chdir("cuong gui\Vietnamese_hand_sign-main")
folder_path = "Raw data\\Raw video\\nguyen"
output_folder_path = "Raw data\\Raw video\\nguyen"
start_time = [15.8, 21.1, 20.8, 18.5, 20.3, 21.9, 23]
end_time = [1507, 1454, 1446, 1440, 1444, 1447, 1448]
i = 0

def cut_video(input_file, output_file, start_time, duration):
    ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file).run()

def trim(in_file, out_file, start, end):
    if os.path.exists(out_file):
        os.remove(out_file)

    in_file_probe_result = ffmpeg.probe(in_file)
    in_file_duration = in_file_probe_result.get(
        "format", {}).get("duration", None)
    print(in_file_duration)

    input_stream = ffmpeg.input(in_file)

    pts = "PTS-STARTPTS"
    video = input_stream.trim(start=start, end=end).setpts(pts)
    audio = (input_stream
             .filter_("atrim", start=start, end=end)
             .filter_("asetpts", pts))
    video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
    output = ffmpeg.output(video_and_audio, out_file, format="mp4")
    output.run()

    out_file_probe_result = ffmpeg.probe(out_file)
    out_file_duration = out_file_probe_result.get(
        "format", {}).get("duration", None)
    print(out_file_duration)

for filename in os.listdir(folder_path):
    # print(filename)
    if filename.endswith((".mp4")) and not filename.startswith(("check")):
        # Create the input and output file paths
        print(filename)
        input_file = os.path.join(folder_path, filename)
        output_file = os.path.join(output_folder_path, f"syncho_{filename}")

        # Call the cut_video function
        trim(input_file, output_file, start_time[i], end_time[i])
        i+=1
        
        