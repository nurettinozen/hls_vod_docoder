import argparse
import os

def encode_video(video_path, output_path, subtitles_path=None):
    resolutions = [240, 360, 480, 720, 1080]
    bitrates = [400, 800, 1200, 2500, 5000]
    keyframe_intervals = [90, 90, 90, 90, 90]
    crf = 23
    preset = 'fast'
    tune = 'film'

    commands = []
    for i in range(len(resolutions)):
        resolution = resolutions[i]
        bitrate = bitrates[i]
        keyframe_interval = keyframe_intervals[i]

        # Generate segment filename
        segment_filename = f'{output_path}/{resolution}p_%03d.ts'

        # Generate command for video encoding
        command = (
            f'ffmpeg -i {video_path} -vf "scale=-2:{resolution}" '
            f'-c:v libx264 -preset {preset} -tune {tune} -profile:v main '
            f'-keyint_min {keyframe_interval} -g {keyframe_interval} '
            f'-sc_threshold 0 -b:v {bitrate}k -maxrate {bitrate}k -bufsize {bitrate * 2}k '
            f'-hls_time 6 -hls_list_size 0 -hls_segment_filename {segment_filename} '
        )

        if subtitles_path:
            command += f'-vf subtitles={subtitles_path} '

        commands.append(command)

    master_playlist = '#EXTM3U\n'
    for i in range(len(resolutions)):
        resolution = resolutions[i]
        command = commands[i]
        segment_filename = f'{output_path}/{resolution}p_%03d.ts'

        os.system(f'{command} {output_path}/{resolution}p.m3u8')

        master_playlist += (
            f'#EXT-X-STREAM-INF:BANDWIDTH={bitrates[i] * 1000},RESOLUTION={output_path}/{resolution}x{int(resolution * 9 / 16)}\n'
            f'{output_path}/{resolution}p.m3u8\n'
        )
    with open('master.m3u8', 'w') as f:
        f.write(master_playlist)

def main():
    parser = argparse.ArgumentParser(description='Encode video into multiple resolutions and bitrates and create an HLS playlist.')
    parser.add_argument('video_path', help='Path to the input video file.')
    parser.add_argument('output_path', help='Path to the directory where the encoded video files and playlist will be written.')
    parser.add_argument('--subtitles_path', help='Path to a subtitle file that will be embedded into the encoded video.')
    args = parser.parse_args()

    video_path = args.video_path
    output_path = args.output_path
    subtitles_path = args.subtitles_path

    encode_video(video_path, output_path, subtitles_path)

if __name__ == '__main__':
    main()
