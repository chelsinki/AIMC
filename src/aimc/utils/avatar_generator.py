"""
像素风格主持人头像生成器
"""
from PIL import Image, ImageDraw, ImageFont
import random


class AvatarGenerator:
    """生成像素风格的主持人头像"""

    # 预设的主持人形象配置
    HOST_STYLES = {
        "default": {
            "name": "小智",
            "skin_color": (255, 224, 196),
            "hair_color": (80, 60, 40),
            "eye_color": (40, 80, 120),
            "shirt_color": (60, 100, 160),
            "tie_color": (180, 60, 60),
        },
        "female": {
            "name": "小慧",
            "skin_color": (255, 224, 196),
            "hair_color": (60, 40, 30),
            "eye_color": (80, 120, 80),
            "shirt_color": (180, 100, 120),
            "tie_color": None,
        },
        "tech": {
            "name": "小科",
            "skin_color": (220, 200, 180),
            "hair_color": (40, 40, 60),
            "eye_color": (0, 200, 255),
            "shirt_color": (40, 60, 80),
            "tie_color": (0, 150, 200),
        }
    }

    def __init__(self, style: str = "default", size: int = 128):
        """
        初始化头像生成器

        Args:
            style: 风格名称 (default/female/tech)
            size: 头像尺寸（像素）
        """
        self.style = self.HOST_STYLES.get(style, self.HOST_STYLES["default"])
        self.size = size
        self.pixel_size = max(4, size // 32)  # 像素块大小

    def generate(self, expression: str = "smile") -> Image.Image:
        """
        生成头像

        Args:
            expression: 表情 (smile/neutral/surprise)

        Returns:
            PIL Image对象
        """
        # 创建画布
        img = Image.new('RGB', (self.size, self.size), (240, 240, 240))
        draw = ImageDraw.Draw(img)

        # 计算中心点
        center_x = self.size // 2
        center_y = self.size // 2

        # 绘制各个部分
        self._draw_face(draw, center_x, center_y)
        self._draw_eyes(draw, center_x, center_y, expression)
        self._draw_mouth(draw, center_x, center_y, expression)
        self._draw_hair(draw, center_x, center_y)
        self._draw_body(draw, center_x, center_y)

        return img

    def _draw_face(self, draw: ImageDraw, cx: int, cy: int):
        """绘制脸部"""
        face_width = self.size * 0.35
        face_height = self.size * 0.45
        x1 = cx - face_width // 2
        y1 = cy - face_height // 3
        x2 = x1 + face_width
        y2 = y1 + face_height
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=self.style["skin_color"])

    def _draw_eyes(self, draw: ImageDraw, cx: int, cy: int, expression: str):
        """绘制眼睛"""
        eye_width = self.size * 0.08
        eye_height = self.size * 0.06
        eye_y = cy - self.size * 0.08

        # 左眼
        left_x = cx - self.size * 0.1
        draw.ellipse([left_x, eye_y, left_x + eye_width, eye_y + eye_height],
                     fill=self.style["eye_color"])

        # 右眼
        right_x = cx + self.size * 0.02
        draw.ellipse([right_x, eye_y, right_x + eye_width, eye_y + eye_height],
                     fill=self.style["eye_color"])

        # 根据表情调整
        if expression == "surprise":
            # 眼睛睁大效果（白色高光）
            pass

    def _draw_mouth(self, draw: ImageDraw, cx: int, cy: int, expression: str):
        """绘制嘴巴"""
        mouth_y = cy + self.size * 0.12
        mouth_width = self.size * 0.15

        if expression == "smile":
            # 微笑 - 弧线
            draw.arc([cx - mouth_width//2, mouth_y - 10,
                     cx + mouth_width//2, mouth_y + 10],
                    start=0, end=180, fill=(200, 80, 80), width=2)
        elif expression == "surprise":
            # 惊讶 - 圆形
            draw.ellipse([cx - 8, mouth_y - 8, cx + 8, mouth_y + 8],
                        fill=(200, 80, 80))
        else:
            # 中性 - 直线
            draw.line([cx - mouth_width//2, mouth_y,
                      cx + mouth_width//2, mouth_y],
                     fill=(200, 80, 80), width=2)

    def _draw_hair(self, draw: ImageDraw, cx: int, cy: int):
        """绘制头发"""
        hair_y = cy - self.size * 0.25
        hair_width = self.size * 0.4
        hair_height = self.size * 0.2

        # 简单的发型 - 头顶部分
        draw.ellipse([cx - hair_width//2, hair_y,
                     cx + hair_width//2, hair_y + hair_height],
                    fill=self.style["hair_color"])

    def _draw_body(self, draw: ImageDraw, cx: int, cy: int):
        """绘制身体/衣服"""
        body_y = cy + self.size * 0.35
        body_width = self.size * 0.5
        body_height = self.size * 0.4

        # 衣服
        draw.rectangle([cx - body_width//2, body_y,
                       cx + body_width//2, body_y + body_height],
                      fill=self.style["shirt_color"])

        # 如果有领带
        if self.style.get("tie_color"):
            tie_width = self.size * 0.08
            tie_height = self.size * 0.15
            draw.polygon([
                (cx, body_y),
                (cx - tie_width//2, body_y + tie_height),
                (cx + tie_width//2, body_y + tie_height)
            ], fill=self.style["tie_color"])

    def save(self, path: str, expression: str = "smile"):
        """保存头像到文件"""
        img = self.generate(expression)
        img.save(path)
        return path


def generate_host_avatar(name: str = "小智", style: str = "default", size: int = 256):
    """快速生成主持人头像的便捷函数"""
    generator = AvatarGenerator(style=style, size=size)
    img = generator.generate(expression="smile")

    # 添加名字标签
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)

    # 尝试使用字体，如果没有就用默认
    try:
        font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", size=size//10)
    except:
        font = ImageFont.load_default()

    # 在底部添加名字
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    x = (size - text_width) // 2
    y = size - size//8

    draw.text((x, y), name, fill=(40, 40, 40), font=font)

    return img


if __name__ == "__main__":
    # 测试生成不同风格的头像
    for style in ["default", "female", "tech"]:
        gen = AvatarGenerator(style=style, size=256)
        img = gen.generate(expression="smile")
        img.save(f"host_avatar_{style}.png")
        print(f"Generated: host_avatar_{style}.png")
