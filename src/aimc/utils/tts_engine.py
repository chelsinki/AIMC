"""
TTS (Text-to-Speech) 引擎
支持多种TTS后端：pyttsx3(离线)、edge-tts(在线)
"""
import os
import tempfile
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TTSEngine:
    """TTS引擎基类"""

    def __init__(self, cache_dir: str = "materials/预生成音频"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.stats = {"cache_hits": 0, "cache_misses": 0, "errors": 0}

    def _get_cache_path(self, text: str, voice: str = "default") -> Path:
        """获取缓存文件路径"""
        import hashlib
        text_hash = hashlib.md5(f"{text}_{voice}".encode()).hexdigest()[:12]
        return self.cache_dir / f"{text_hash}.wav"

    def speak(self, text: str, voice: str = "default", use_cache: bool = True) -> bool:
        """
        播放文本（同步接口）

        Args:
            text: 要播放的文本
            voice: 音色名称
            use_cache: 是否使用缓存

        Returns:
            是否成功
        """
        raise NotImplementedError

    def save(self, text: str, output_path: str, voice: str = "default") -> bool:
        """
        保存到文件

        Args:
            text: 要转换的文本
            output_path: 输出文件路径
            voice: 音色名称

        Returns:
            是否成功
        """
        raise NotImplementedError

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.stats.copy()


class Pyttsx3Engine(TTSEngine):
    """基于pyttsx3的离线TTS引擎"""

    def __init__(self, cache_dir: str = "materials/预生成音频"):
        super().__init__(cache_dir)
        self.engine = None
        self._init_engine()

    def _init_engine(self):
        """初始化pyttsx3引擎"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            # 设置默认参数
            self.engine.setProperty('rate', 180)  # 语速
            self.engine.setProperty('volume', 0.9)  # 音量

            # 尝试设置中文语音
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                    self.engine.setProperty('voice', voice.id)
                    logger.info(f"设置中文语音: {voice.name}")
                    break

            logger.info("pyttsx3引擎初始化成功")
        except Exception as e:
            logger.error(f"pyttsx3引擎初始化失败: {e}")
            self.engine = None

    def speak(self, text: str, voice: str = "default", use_cache: bool = True) -> bool:
        """播放文本"""
        if not self.engine:
            logger.error("TTS引擎未初始化")
            return False

        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"TTS播放失败: {e}")
            self.stats["errors"] += 1
            return False

    def save(self, text: str, output_path: str, voice: str = "default") -> bool:
        """保存到文件"""
        if not self.engine:
            logger.error("TTS引擎未初始化")
            return False

        try:
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"TTS保存失败: {e}")
            self.stats["errors"] += 1
            return False


class EdgeTTSEngine(TTSEngine):
    """基于edge-tts的在线TTS引擎（免费）"""

    # 中文音色列表
    VOICES = {
        "default": "zh-CN-XiaoxiaoNeural",      # 晓晓 - 年轻女声
        "female1": "zh-CN-XiaoyiNeural",        # 晓伊 - 女声
        "male1": "zh-CN-YunjianNeural",        # 云健 - 男声
        "male2": "zh-CN-YunxiNeural",          # 云希 - 男声
        "child": "zh-CN-XiaoxiaoNeural",       # 童声
    }

    def __init__(self, cache_dir: str = "materials/预生成音频"):
        super().__init__(cache_dir)
        self._check_edge_tts()

    def _check_edge_tts(self):
        """检查edge-tts是否可用"""
        try:
            import edge_tts
            logger.info("edge-tts已安装")
        except ImportError:
            logger.warning("edge-tts未安装，正在尝试安装...")
            import subprocess
            subprocess.run(["pip", "install", "edge-tts", "-q"])

    def _get_voice(self, voice_key: str) -> str:
        """获取音色ID"""
        return self.VOICES.get(voice_key, self.VOICES["default"])

    async def _speak_async(self, text: str, voice: str = "default") -> bool:
        """异步播放（使用文件缓存）"""
        try:
            import edge_tts

            voice_id = self._get_voice(voice)
            communicate = edge_tts.Communicate(text, voice_id)

            # 保存到临时文件并播放
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp_path = tmp.name
                await communicate.save(tmp_path)

            # 播放音频
            self._play_audio(tmp_path)

            # 清理临时文件
            os.unlink(tmp_path)
            return True

        except Exception as e:
            logger.error(f"edge-tts播放失败: {e}")
            self.stats["errors"] += 1
            return False

    def _play_audio(self, audio_path: str):
        """播放音频文件"""
        import platform
        import subprocess

        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.run(["afplay", audio_path], check=True)
            elif system == "Linux":
                subprocess.run(["aplay", audio_path], check=True)
            elif system == "Windows":
                import winsound
                winsound.PlaySound(audio_path, winsound.SND_FILENAME)
        except Exception as e:
            logger.error(f"音频播放失败: {e}")

    def speak(self, text: str, voice: str = "default", use_cache: bool = True) -> bool:
        """同步播放接口"""
        # 检查缓存
        if use_cache:
            cache_path = self._get_cache_path(text, voice)
            if cache_path.exists():
                logger.info(f"使用缓存: {cache_path}")
                self.stats["cache_hits"] += 1
                self._play_audio(str(cache_path))
                return True
            self.stats["cache_misses"] += 1

        # 运行异步播放
        try:
            result = asyncio.run(self._speak_async(text, voice))
            return result
        except Exception as e:
            logger.error(f"播放失败: {e}")
            return False

    async def _save_async(self, text: str, output_path: str, voice: str = "default") -> bool:
        """异步保存"""
        try:
            import edge_tts
            voice_id = self._get_voice(voice)
            communicate = edge_tts.Communicate(text, voice_id)
            await communicate.save(output_path)
            return True
        except Exception as e:
            logger.error(f"保存失败: {e}")
            return False

    def save(self, text: str, output_path: str, voice: str = "default") -> bool:
        """保存到文件"""
        try:
            return asyncio.run(self._save_async(text, output_path, voice))
        except Exception as e:
            logger.error(f"保存失败: {e}")
            return False


def create_tts_engine(engine_type: str = "auto", cache_dir: str = "materials/预生成音频") -> TTSEngine:
    """
    工厂函数：创建TTS引擎

    Args:
        engine_type: 引擎类型 ("auto" | "pyttsx3" | "edge-tts")
        cache_dir: 缓存目录

    Returns:
        TTSEngine实例
    """
    if engine_type == "auto":
        # 自动选择：优先尝试edge-tts（质量更好），失败则用pyttsx3
        try:
            import edge_tts
            logger.info("使用 edge-tts 引擎")
            return EdgeTTSEngine(cache_dir)
        except ImportError:
            logger.info("edge-tts 不可用，使用 pyttsx3 引擎")
            return Pyttsx3Engine(cache_dir)
    elif engine_type == "pyttsx3":
        return Pyttsx3Engine(cache_dir)
    elif engine_type == "edge-tts":
        return EdgeTTSEngine(cache_dir)
    else:
        raise ValueError(f"未知的引擎类型: {engine_type}")


# 便捷函数
def quick_say(text: str, voice: str = "default"):
    """快速播放文本"""
    engine = create_tts_engine("auto")
    return engine.speak(text, voice)


def quick_save(text: str, output_path: str, voice: str = "default"):
    """快速保存到文件"""
    engine = create_tts_engine("auto")
    return engine.save(text, output_path, voice)


if __name__ == "__main__":
    # 测试TTS引擎
    print("测试TTS引擎...")

    # 创建引擎
    tts = create_tts_engine("auto")

    # 测试播放
    test_texts = [
        "大家好，我是今天的数字人主持小智，很高兴见到大家！",
        "今天的会议非常精彩，让我们开始吧。",
        "感谢各位嘉宾的精彩分享！"
    ]

    for i, text in enumerate(test_texts):
        print(f"\n测试 {i+1}: {text[:30]}...")
        success = tts.speak(text)
        print(f"播放结果: {'成功' if success else '失败'}")

    # 测试保存
    print("\n测试保存到文件...")
    save_path = "test_output.mp3"
    success = tts.save(test_texts[0], save_path)
    print(f"保存到 {save_path}: {'成功' if success else '失败'}")

    # 打印统计信息
    print(f"\n统计信息: {tts.get_stats()}")
