import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def get_font(size):
    """跨平台获取字体"""
    # 常见字体路径列表
    font_paths = [
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Times.ttc",
        # Windows
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    
    # Pillow 10.1.0+ 支持 load_default 带 size 参数
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        # 旧版本 Pillow，返回固定大小默认字体（不推荐）
        print("警告：无法找到合适字体，文字可能显示异常")
        return ImageFont.load_default()


def create_mihomo_logo_v2():
    # 1. 获取原始 Logo
    url = "https://raw.githubusercontent.com/MetaCubeX/mihomo/Meta/Meta.png"
    print("正在下载图标...")
    response = requests.get(url)
    logo = Image.open(BytesIO(response.content)).convert("RGBA")

    # --- 调整参数区域 ---
    target_icon_h = 350  # 图标高度
    font_size = target_icon_h // 2  # 文字大小为图标高度的一半 (175)
    padding = 40  # 图标和文字的间距
    # -------------------

    # 2. 处理 Logo 尺寸
    ratio = target_icon_h / logo.height
    target_icon_w = int(logo.width * ratio)
    logo = logo.resize((target_icon_w, target_icon_h), Image.Resampling.LANCZOS)

    # 3. 处理文字
    text = "mihomo"
    font = get_font(font_size)

    # 计算文字宽高
    temp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 字体基线修正 (让视觉更居中)
    offset_y = bbox[1]

    # 4. 创建画布
    canvas_w = target_icon_w + padding + text_w
    # 画布高度取图标高度 (因为图标现在比文字大很多)
    canvas_h = target_icon_h

    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 5. 绘制
    # 绘制 Logo (垂直居中，其实就是贴在 (0,0) 因为画布高度就是图标高度)
    logo_y = (canvas_h - target_icon_h) // 2
    img.paste(logo, (0, logo_y), logo)

    # 绘制文字 (计算垂直居中)
    text_x = target_icon_w + padding
    # 核心算法: 画布高度的一半 - 文字高度的一半 - 文字自身的偏移
    text_y = (canvas_h - text_h) // 2 - offset_y

    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0, 255))

    # 6. 保存
    output_filename = "mihomo_logo_large_icon.png"
    img.save(output_filename)
    print(f"成功生成: {output_filename}")


if __name__ == "__main__":
    create_mihomo_logo_v2()
