import os
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# ========== 配置部分 ==========
topic = "红黑树"  # 每次只处理一个 topic
json_path = f"./slides/{topic}.json"
image_dir = "./images"
output_pptx = f"./ppt_output/{topic}.pptx"

# ========== 插图匹配 ==========
def find_image_for_description(desc, image_dir="./images"):
    """
    根据 image_suggestion 字符串模糊查找图片路径
    """
    if not desc:
        return None
    for img_file in os.listdir(image_dir):
        if any(keyword in img_file for keyword in desc.split()):
            return os.path.join(image_dir, img_file)
    return None

# ========== PPT 创建逻辑 ==========
prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
bullet_slide_layout = prs.slide_layouts[1]
blank_slide_layout = prs.slide_layouts[6]

# 读取 JSON
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Slide 1: 标题页
slide = prs.slides.add_slide(title_slide_layout)
slide.shapes.title.text = data.get("title", topic)
slide.placeholders[1].text = f"主题：{topic}"

# Slide 2: 提纲 + 讲解
slide = prs.slides.add_slide(bullet_slide_layout)
slide.shapes.title.text = "主要内容"
content_shape = slide.placeholders[1]
outline = data.get("outline", [])
if outline:
    for point in outline:
        content_shape.text += f"\n• {point}"
else:
    content_shape.text = "（无内容）"

# Slide 3: 讲解详细内容
slide = prs.slides.add_slide(blank_slide_layout)
text_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8.5), Inches(1))
text_box.text_frame.text = "简要讲解"
body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(9), Inches(5))
body_box.text_frame.text = data.get("explanation", "（无讲解内容）")

# Slide 4: 插图页（如果有）
img_path = find_image_for_description(data.get("image_suggestion", ""), image_dir)
slide = prs.slides.add_slide(blank_slide_layout)

# 标题
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(1))
title_box.text_frame.text = "示意图"

if img_path and os.path.exists(img_path):
    slide.shapes.add_picture(img_path, Inches(1), Inches(1.2), height=Inches(4.5))
else:
    desc_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(3))
    desc_frame = desc_box.text_frame
    desc_frame.text = data.get("image_suggestion", "（无插图建议）")

# Slide 5: 代码示例
slide = prs.slides.add_slide(blank_slide_layout)
text_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1))
text_box.text_frame.text = "代码示例"

code = data.get("code_example", "")
code_box = slide.shapes.add_textbox(Inches(0.5), Inches(1), Inches(9), Inches(5))
code_frame = code_box.text_frame
code_frame.word_wrap = True
p = code_frame.add_paragraph()
p.text = code
p.font.name = 'Courier New'
p.font.size = Pt(12)
p.font.color.rgb = RGBColor(50, 50, 50)

# ========== 保存 ==========
os.makedirs(os.path.dirname(output_pptx), exist_ok=True)
prs.save(output_pptx)
print(f"PPT 已保存至：{output_pptx}")
