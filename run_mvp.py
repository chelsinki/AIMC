#!/usr/bin/env python3
"""
AIMC MVP - 简化运行脚本
=======================
一键运行数字人主持演示

使用方法:
    python run_mvp.py
"""

import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """主函数"""
    print("="*60)
    print("  AIMC 数字人主持系统 - MVP")
    print("="*60)
    print()

    # 导入并运行测试
    try:
        import test_mvp
        return test_mvp.main()
    except Exception as e:
        print(f"运行错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
