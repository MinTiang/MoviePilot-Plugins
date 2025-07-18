import json
import subprocess

from app.utils.system import SystemUtils


class FfmpegHelper:

    @staticmethod
    def get_thumb(video_path: str, image_path: str, frames: str = None):
        """
        使用ffmpeg从视频文件中截取缩略图
        """
        if not frames:
            frames = "00:03:01"
        if not video_path or not image_path:
            return False
        cmd = 'ffmpeg -ss {frames} -i "{video_path}" -vframes 1 -f image2 "{image_path}"'.format(video_path=video_path,
                                                                                                 frames=frames,
                                                                                                 image_path=image_path)
        result = SystemUtils.execute(cmd)
        if result:
            return True
        return False

    @staticmethod
    def extract_wav(video_path: str, audio_path: str, audio_index: str = None):
        """
        使用ffmpeg从视频文件中提取16000hz, 16-bit的wav格式音频
        """
        if not video_path or not audio_path:
            return False

        # 提取指定音频流
        if audio_index:
            command = ['ffmpeg', "-hide_banner", "-loglevel", "warning", '-y', '-i', video_path,
                       '-map', f'0:a:{audio_index}',
                       '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', audio_path]
        else:
            command = ['ffmpeg', "-hide_banner", "-loglevel", "warning", '-y', '-i', video_path,
                       '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', audio_path]

        ret = subprocess.run(command).returncode
        if ret == 0:
            return True
        return False

    @staticmethod
    def get_metadata(video_path: str):
        """
        获取视频元数据
        """
        if not video_path:
            return False

        try:
            command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return json.loads(result.stdout.decode("utf-8"))
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def extract_subtitle(video_path: str, subtitle_path: str, subtitle_index: str = None):
        """
        从视频中提取字幕
        """
        if not video_path or not subtitle_path:
            return False

        if subtitle_index:
            command = ['ffmpeg', "-hide_banner", "-loglevel", "warning", '-y', '-i', video_path,
                       '-map', f'0:s:{subtitle_index}',
                       subtitle_path]
        else:
            command = ['ffmpeg', "-hide_banner", "-loglevel", "warning", '-y', '-i', video_path, subtitle_path]
        ret = subprocess.run(command).returncode
        if ret == 0:
            return True
        return False
