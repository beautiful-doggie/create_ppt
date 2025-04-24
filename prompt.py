import os

# topic = "二叉树"

prompt_templates = {
    "concept": "请简要介绍『{topic}』的概念，适合初学者理解，并尽量配合类比或可视化描述，适用于教学PPT。",
    "code": "请用 Python 实现一个基本的『{topic}』结构，并附上插入和遍历等基础操作的示例代码，要求注释清晰，适合教学演示。",
    "application": "请说明『{topic}』在实际中的应用场景，结合至少一个具体例子，适合用于教学介绍。",
    "traversal": "请说明『{topic}』中可能的遍历方式或操作流程（如果适用），并附伪代码或流程图描述。",
    "comparison": "将『{topic}』与其他类似的数据结构（如链表、数组等）进行对比分析，说明各自的特点和适用场景。"
}
def generate_prompts(topic: str):
    """
    为给定 topic 生成多个教学 prompt，保存在 prompts/{topic}/ 中
    """
    topic_dir = os.path.join("prompts", topic)
    os.makedirs(topic_dir, exist_ok=True)
    paths=[]
    for key, template in prompt_templates.items():
        prompt_text = template.format(topic=topic)
        filename = os.path.join(topic_dir, f"prompt_{topic}_{key}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(prompt_text)
        paths.append(filename)
    print(f"已生成关于「{topic}」的 prompts，共 {len(prompt_templates)} 条，保存在 {topic_dir}/")



# output_dir = "prompts"
# os.makedirs(output_dir, exist_ok=True)

# # 遍历维度模板生成 prompt
# for key, template in prompt_templates.items():
#     prompt_text = template.format(topic=topic)
#     filename = os.path.join(output_dir, f"prompt_{topic}_{key}.txt")
#     with open(filename, "w", encoding="utf-8") as f:
#         f.write(prompt_text)

# print(f"已生成关于{topic}的教学 prompt，共 {len(prompt_templates)} 条，保存在 prompts/ 目录下")
