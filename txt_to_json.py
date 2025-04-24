import os
import json
from collections import defaultdict

def convert_txt_to_json(topic: str):
    """
    从 outputs/{topic}/ 中读取所有 .txt 文件，整合成 jsons/{topic}.json
    """
    prompt_dir = os.path.join("outputs", topic)
    json_dir = "jsons"
    os.makedirs(json_dir, exist_ok=True)

    topic_data = {}  # direction -> content

    for filename in os.listdir(prompt_dir):
        if filename.endswith(".txt"):
            parts = filename[len("output_"):-len(".txt")].split("_")
            # 输出格式为 output_二叉树_code.txt，处理出 key
            direction = "_".join(parts[1:]) if len(parts) >= 2 else parts[0]

            file_path = os.path.join(prompt_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            topic_data[direction] = content

    json_path = os.path.join(json_dir, f"{topic}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "topic": topic,
            "content": topic_data
        }, f, ensure_ascii=False, indent=2)

    print(f"已保存 JSON：{json_path}")



# prompt_dir = "outputs"     # txt 所在目录
# json_dir = "jsons"         # 输出 json 的目录
# os.makedirs(json_dir, exist_ok=True)

# # 结构：topic -> { direction: content }
# topic_data = defaultdict(dict)

# # 遍历所有提示词 txt 文件
# for filename in os.listdir(prompt_dir):
#     if filename.startswith("output_") and filename.endswith(".txt"):
#         parts = filename[len("output_"):-len(".txt")].split("_")
#         if len(parts) < 2:
#             continue
#         topic = parts[0]
#         direction = "_".join(parts[1:])
        
#         with open(os.path.join(prompt_dir, filename), "r", encoding="utf-8") as f:
#             content = f.read().strip()
        
#         topic_data[topic][direction] = content

# # 保存为 json 文件
# for topic, content_dict in topic_data.items():
#     json_path = os.path.join(json_dir, f"{topic}.json")
#     with open(json_path, "w", encoding="utf-8") as f:
#         json.dump({
#             "topic": topic,
#             "content": content_dict
#         }, f, ensure_ascii=False, indent=2)

#     print(f"已保存: {json_path}")
