"""
主持稿解析器
支持YAML格式的主持稿解析和验证
"""
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class SpeakerType(Enum):
    """发言者类型"""
    HUMAN = "human"
    AI = "ai"


@dataclass
class Line:
    """台词"""
    speaker: SpeakerType
    text: str
    duration: int = 0
    keywords: List[str] = field(default_factory=list)
    tone: str = "neutral"
    expression: str = "neutral"


@dataclass
class Segment:
    """环节"""
    id: str
    name: str
    index: int
    expected_duration: int
    speaker_order: List[SpeakerType]
    lines: List[Line] = field(default_factory=list)
    transitions: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class Script:
    """主持稿"""
    title: str
    segments: List[Segment]
    config: Dict[str, Any] = field(default_factory=dict)


class ScriptParser:
    """主持稿解析器"""

    # 默认配置
    DEFAULT_CONFIG = {
        "allow_improvisation": True,
        "max_improvisation_duration": 30,
        "timeout_threshold": 1.3,
        "silence_duration": 2.0,
        "voice_threshold": 500,
    }

    def __init__(self):
        self.errors = []
        self.warnings = []

    def parse(self, yaml_path: Union[str, Path]) -> Optional[Script]:
        """
        解析YAML主持稿

        Args:
            yaml_path: YAML文件路径

        Returns:
            Script对象，解析失败返回None
        """
        yaml_path = Path(yaml_path)

        if not yaml_path.exists():
            self.errors.append(f"文件不存在: {yaml_path}")
            return None

        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML解析错误: {e}")
            return None

        return self._parse_script(data)

    def _parse_script(self, data: Dict) -> Optional[Script]:
        """解析主持稿数据"""
        # 解析环节信息
        segment_info = data.get("环节信息", {})
        segment_id = segment_info.get("名称", "unnamed").lower().replace(" ", "_")
        segment_name = segment_info.get("名称", "未命名环节")
        segment_index = segment_info.get("序号", 0)
        expected_duration = segment_info.get("预期时长", 0)

        # 解析发言顺序
        speaker_order_raw = segment_info.get("预期发言顺序", ["human", "ai"])
        speaker_order = []
        for s in speaker_order_raw:
            if s.lower() in ["human", "ai"]:
                speaker_order.append(SpeakerType.HUMAN if s.lower() == "human" else SpeakerType.AI)

        # 解析台词
        lines_data = data.get("主持人台词", {})
        lines = []

        for key, line_data in lines_data.items():
            speaker = SpeakerType.HUMAN if "human" in key.lower() else SpeakerType.AI
            text = line_data.get("文本", "") if isinstance(line_data, dict) else str(line_data)
            duration = line_data.get("预期时长", 0) if isinstance(line_data, dict) else 0
            keywords = line_data.get("关键词", []) if isinstance(line_data, dict) else []
            tone = line_data.get("语气", "neutral") if isinstance(line_data, dict) else "neutral"
            expression = line_data.get("表情", "neutral") if isinstance(line_data, dict) else "neutral"

            lines.append(Line(
                speaker=speaker,
                text=text,
                duration=duration,
                keywords=keywords,
                tone=tone,
                expression=expression
            ))

        # 解析衔接词库
        transitions_data = data.get("衔接词库", {})
        transitions = {}
        for key, values in transitions_data.items():
            transitions[key] = values if isinstance(values, list) else [str(values)]

        # 解析配置
        config = data.get("配置", {})
        # 合并默认配置
        merged_config = self.DEFAULT_CONFIG.copy()
        merged_config.update(config)

        # 创建环节
        segment = Segment(
            id=segment_id,
            name=segment_name,
            index=segment_index,
            expected_duration=expected_duration,
            speaker_order=speaker_order,
            lines=lines,
            transitions=transitions
        )

        # 创建主持稿
        script = Script(
            title=segment_name,
            segments=[segment],
            config=merged_config
        )

        return script

    def validate(self, script: Script) -> bool:
        """
        验证主持稿是否有效

        Args:
            script: Script对象

        Returns:
            是否有效
        """
        self.errors = []
        self.warnings = []

        if not script.segments:
            self.errors.append("主持稿没有环节")
            return False

        for segment in script.segments:
            # 检查必要字段
            if not segment.name:
                self.errors.append(f"环节 {segment.id} 没有名称")

            if not segment.lines:
                self.warnings.append(f"环节 {segment.name} 没有台词")

            # 检查台词
            for i, line in enumerate(segment.lines):
                if not line.text:
                    self.errors.append(f"环节 {segment.name} 第{i+1}行台词为空")

        return len(self.errors) == 0

    def get_errors(self) -> list:
        """获取错误列表"""
        return self.errors.copy()

    def get_warnings(self) -> list:
        """获取警告列表"""
        return self.warnings.copy()


def parse_script(yaml_path: str) -> Optional[Script]:
    """
    便捷函数：解析主持稿

    Args:
        yaml_path: YAML文件路径

    Returns:
        Script对象或None
    """
    parser = ScriptParser()
    script = parser.parse(yaml_path)

    if script and parser.validate(script):
        return script
    else:
        print("解析错误:")
        for error in parser.get_errors():
            print(f"  ❌ {error}")
        for warning in parser.get_warnings():
            print(f"  ⚠️  {warning}")
        return None


if __name__ == "__main__":
    # 测试解析器
    print("测试主持稿解析器...")

    # 创建一个测试用的YAML文件
    test_yaml = """
环节信息:
  名称: 开场词
  序号: 1
  预期时长: 120
  预期发言顺序:
    - human
    - ai

主持人台词:
  human:
    文本: "大家好，欢迎来到今天的活动！"
    预期时长: 30
    关键词:
      - 欢迎
      - 活动
    语气: 热情
  ai:
    文本: "感谢主持人的精彩开场，我是今天的数字人主持小智！"
    预期时长: 40
    关键词:
      - 感谢
      - 数字人
    语气: 亲切
    表情: 微笑

衔接词库:
  正常衔接:
    - "好的，接下来..."
    - "非常好，现在..."
  打断衔接:
    - "抱歉打断一下，"

配置:
  允许即兴: true
  静默判断时长: 2.0
  语音检测阈值: 500
"""

    # 写入测试文件
    test_path = "/tmp/test_script.yaml"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(test_yaml)

    # 解析
    script = parse_script(test_path)

    if script:
        print(f"\n✅ 解析成功！")
        print(f"主持稿标题: {script.title}")
        print(f"环节数量: {len(script.segments)}")
        for seg in script.segments:
            print(f"\n环节: {seg.name}")
            print(f"  台词数: {len(seg.lines)}")
            for i, line in enumerate(seg.lines):
                print(f"    {i+1}. [{line.speaker.value}] {line.text[:30]}...")
        print(f"\n配置: {script.config}")
