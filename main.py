import os
import sys
from prompt import generate_prompts
from load import generate_outputs
from txt_to_json import convert_txt_to_json
from json_to_ppt import json_to_ppt

def process_topic(topic: str):
    ppt_path = f"ppt/{topic}.pptx"
    if os.path.exists(ppt_path):
        print(f"{ppt_path} 已存在，跳过生成。")
        return

    print(f"\n>>> 开始处理主题：{topic}")
    generate_prompts(topic)
    generate_outputs(topic)
    convert_txt_to_json(topic)
    json_to_ppt(topic)
    print(f">>> 全流程完成：{ppt_path}\n")

if __name__ == "__main__":
    process_topic('深度优先搜索')