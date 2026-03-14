#!/usr/bin/env python3
"""
AIMC - MVP 演示程序
===================
功能：
1. 解析YAML主持稿
2. 生成像素风格主持人头像
3. 使用TTS播放台词
4. 模拟简单的主持流程

作者：AI Assistant
版本：MVP 0.1.0
"""

import os
import sys
import time
import random
from pathlib import Path
from typing import Optional, List

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from aimc.core.script_parser import ScriptParser, Script, Segment, Line, SpeakerType
from aimc.utils.avatar_generator import generate_host_avatar
from aimc.utils.tts_engine import create_tts_engine


class SimpleOrchestrator:
    """简化的流程协调器 - MVP版本"""

    def __init__(self, script: Script, avatar_path: Optional[str] = None):
        self.script = script
        self.current_segment_index = 0
        self.current_line_index = 0
        self.avatar_path = avatar_path
        self.tts = create_tts_engine("auto")
        self.is_running = False
        self.dialogue_history = []

    def display_avatar(self):
        """在终端显示头像"""
        if not self.avatar_path or not Path(self.avatar_path).exists():
            # 显示默认表情符号头像
            print("\n" + "="*50)
            print("            🤖 数字人主持")
            print("="*50)
            return

        try:
            from PIL import Image
            img = Image.open(self.avatar_path)
            # 在终端显示图片（使用ASCII艺术）
            print("\n" + "="*50)
            self._print_ascii_avatar(img)
            print("="*50)
        except Exception as e:
            print(f"[头像显示失败: {e}]")

    def _print_ascii_avatar(self, img, width=40):
        """将图片转换为ASCII艺术"""
        # 调整大小
        aspect = img.height / img.width
        height = int(width * aspect * 0.5)
        img = img.resize((width, height))

        # 转换为灰度
        if img.mode != 'L':
            img = img.convert('L')

        # ASCII字符集
        chars = "█▉▊▋▌▍▎▏  "
        pixels = img.load()

        for y in range(img.height):
            line = ""
            for x in range(img.width):
                gray = pixels[x, y]
                char_idx = min(int(gray / 255 * (len(chars) - 1)), len(chars) - 1)
                line += chars[char_idx]
            print(line)

    def play_line(self, line: Line):
        """播放台词"""
        speaker_name = "主持人" if line.speaker == SpeakerType.HUMAN else "🤖 AI"
        print(f"\n[{speaker_name}] {line.text}")

        # 只有AI的发言需要TTS播放
        if line.speaker == SpeakerType.AI:
            print("  [正在播放语音...]")
            success = self.tts.speak(line.text)
            if not success:
                print("  [语音播放失败，请检查TTS配置]")
            return success
        else:
            # 人类发言，模拟等待
            duration = line.duration if line.duration > 0 else len(line.text) * 0.3
            print(f"  [模拟人类发言，时长: {duration:.1f}秒]")
            time.sleep(min(duration, 2))  # 最多等待2秒
            return True

    def run_segment(self, segment: Segment) -> bool:
        """运行一个环节"""
        print(f"\n{'='*50}")
        print(f"【环节 {segment.index + 1}】{segment.name}")
        print(f"预计时长: {segment.expected_duration}秒")
        print('='*50)

        # 显示头像
        self.display_avatar()

        # 播放台词
        for i, line in enumerate(segment.lines):
            self.current_line_index = i
            success = self.play_line(line)

            if not success:
                print(f"[警告: 第{i+1}行播放失败]")

            # 记录历史
            self.dialogue_history.append({
                "segment": segment.name,
                "speaker": line.speaker.value,
                "text": line.text,
                "timestamp": time.time()
            })

        print(f"\n[环节 {segment.name} 完成]")
        return True

    def run(self) -> bool:
        """运行完整主持流程"""
        self.is_running = True

        print("\n" + "="*50)
        print("   AIMC 数字人主持系统 - MVP演示")
        print("="*50)
        print(f"主持稿: {self.script.title}")
        print(f"环节数: {len(self.script.segments)}")

        try:
            for i, segment in enumerate(self.script.segments):
                if not self.is_running:
                    print("\n[流程被中断]")
                    break

                self.current_segment_index = i
                self.run_segment(segment)

                # 环节间暂停
                if i < len(self.script.segments) - 1:
                    print("\n[准备进入下一环节...]")
                    time.sleep(1)

            print("\n" + "="*50)
            print("   主持流程结束，感谢参与！")
            print("="*50)

            # 打印对话历史统计
            print(f"\n对话统计:")
            print(f"  总行数: {len(self.dialogue_history)}")
            human_count = sum(1 for d in self.dialogue_history if d["speaker"] == "human")
            ai_count = sum(1 for d in self.dialogue_history if d["speaker"] == "ai")
            print(f"  人类发言: {human_count}")
            print(f"  AI发言: {ai_count}")

            return True

        except KeyboardInterrupt:
            print("\n\n[用户中断]")
            return False
        except Exception as e:
            print(f"\n[错误: {e}]")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.is_running = False

    def stop(self):
        """停止运行"""
        self.is_running = False


def quick_demo():
    """快速演示"""
    # 创建一个简单的测试主持稿
    test_yaml = """
环节信息:
  名称: 开场介绍
  序号: 1
  预期时长: 60
  预期发言顺序:
    - human
    - ai
    - human
    - ai

主持人台词:
  human_intro:
    文本: "大家好，欢迎来到AI创新大会！"
    预期时长: 3
    关键词:
      - 欢迎
      - AI
    语气: 热情
  ai_response:
    文本: "大家好，我是数字人主持小智，很高兴能和大家一起见证这场科技盛会！"
    预期时长: 6
    关键词:
      - 数字人
      - 科技盛会
    语气: 亲切
    表情: 微笑
  human_continue:
    文本: "是的，今天我们汇聚了很多优秀的AI专家和创业者！"
    预期时长: 4
    关键词:
      - 专家
      - 创业者
    语气: 激动
  ai_close:
    文本: "没错，今天的议程非常精彩。那我们就正式开始吧！"
    预期时长: 5
    关键词:
      - 议程
      - 精彩
    语气: 兴奋
    表情: 兴奋

衔接词库:
  正常衔接:
    - "好的，"
    - "接下来，"
    - "非常好，"
  打断衔接:
    - "抱歉，"
    - "请稍等，"

配置:
  允许即兴: true
  静默判断时长: 2.0
  语音检测阈值: 500
"""

    # 保存测试文件
    test_path = "/tmp/test_script.yaml"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(test_yaml)

    # 解析主持稿
    print("="*50)
    print("解析主持稿...")
    print("="*50)

    parser = ScriptParser()
    script = parser.parse(test_path)

    if not script:
        print("❌ 解析失败!")
        for error in parser.get_errors():
            print(f"  错误: {error}")
        return

    print(f"✅ 解析成功!")
    print(f"   标题: {script.title}")
    print(f"   环节数: {len(script.segments)}")

    # 生成头像
    print("\n" + "="*50)
    print("生成主持人头像...")
    print("="*50)

    avatar_path = "/tmp/host_avatar.png"
    try:
        from aimc.utils.avatar_generator import generate_host_avatar
        img = generate_host_avatar(name="小智", style="default", size=256)
        img.save(avatar_path)
        print(f"✅ 头像已保存: {avatar_path}")
    except Exception as e:
        print(f"⚠️ 头像生成失败: {e}")
        avatar_path = None

    # 运行Orchestrator
    print("\n" + "="*50)
    print("启动主持流程...")
    print("="*50)

    from aimc.mvp_demo import SimpleOrchestrator

    orchestrator = SimpleOrchestrator(script, avatar_path)

    try:
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n\n用户中断演示")
    except Exception as e:
        print(f"\n运行错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    quick_demo()
