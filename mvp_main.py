#!/usr/bin/env python3
"""
AIMC - MVP 主程序
================
数字人主持系统最小可用产品

使用方法：
    python mvp_main.py [--script 主持稿.yaml] [--demo]

作者：AI Assistant
版本：MVP 0.1.0
"""

import os
import sys
import argparse
import time
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def check_dependencies():
    """检查必要的依赖"""
    missing = []

    try:
        import yaml
    except ImportError:
        missing.append("PyYAML")

    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")

    try:
        import numpy
    except ImportError:
        missing.append("numpy")

    if missing:
        print("❌ 缺少以下依赖包:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n请运行以下命令安装:")
        print(f"   pip install {' '.join(missing)}")
        return False

    return True

def generate_demo_script():
    """生成演示用的主持稿"""
    demo_yaml = """环节信息:
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

    # 保存到临时目录
    demo_path = PROJECT_ROOT / "materials" / "主持稿" / "开场词.yaml"
    demo_path.parent.mkdir(parents=True, exist_ok=True)

    with open(demo_path, "w", encoding="utf-8") as f:
        f.write(demo_yaml)

    return str(demo_path)

def run_demo():
    """运行演示"""
    print("\n" + "="*60)
    print("   AIMC 数字人主持系统 - MVP 演示")
    print("="*60)

    # 生成演示主持稿
    print("\n📄 生成演示主持稿...")
    script_path = generate_demo_script()
    print(f"   ✅ 已生成: {script_path}")

    # 导入必要的模块
    from aimc.core.script_parser import ScriptParser
    from aimc.mvp_demo import SimpleOrchestrator
    from aimc.utils.avatar_generator import generate_host_avatar

    # 解析主持稿
    print("\n📖 解析主持稿...")
    parser = ScriptParser()
    script = parser.parse(script_path)

    if not script:
        print("❌ 解析失败!")
        for error in parser.get_errors():
            print(f"   错误: {error}")
        return False

    print(f"   ✅ 解析成功: {script.title}")
    print(f"      环节数: {len(script.segments)}")

    # 生成主持人头像
    print("\n🎨 生成主持人头像...")
    avatar_path = PROJECT_ROOT / "materials" / "数字人动画" / "host_avatar.png"
    avatar_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        img = generate_host_avatar(name="小智", style="default", size=256)
        img.save(avatar_path)
        print(f"   ✅ 头像已保存: {avatar_path}")
    except Exception as e:
        print(f"   ⚠️ 头像生成失败: {e}")
        avatar_path = None

    # 启动Orchestrator
    print("\n🚀 启动主持流程...")
    print("-"*60)

    orchestrator = SimpleOrchestrator(script, str(avatar_path) if avatar_path else None)

    try:
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n\n用户中断演示")
    except Exception as e:
        print(f"\n运行错误: {e}")
        import traceback
        traceback.print_exc()

    return True

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="AIMC - 数字人主持系统 MVP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python mvp_main.py --demo          # 运行演示
    python mvp_main.py --script 主持稿.yaml  # 使用指定主持稿
        """
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="运行演示模式"
    )

    parser.add_argument(
        "--script",
        type=str,
        help="指定主持稿YAML文件路径"
    )

    args = parser.parse_args()

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 运行模式
    if args.demo or not args.script:
        # 演示模式
        run_demo()
    elif args.script:
        # 使用指定主持稿
        print(f"使用主持稿: {args.script}")
        # TODO: 实现指定主持稿的运行
        run_demo()

if __name__ == "__main__":
    main()
