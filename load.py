from transformers import AutoTokenizer, AutoModelForCausalLM
import os 
import torch
# model_path =r"C:\Users\Team NLP\Desktop\create_ppt\model\deepseek-coder-6.7b-base"
# device='cuda'
# tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
# model = AutoModelForCausalLM.from_pretrained(model_path,torch_dtype=torch.float16,
#     device_map="auto" )
def generate_outputs(topic: str):
    model_path =r"C:\Users\Team NLP\Desktop\create_ppt\model\deepseek-coder-6.7b-base"
    device='cuda'
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_path,torch_dtype=torch.float16,
    device_map="auto" )
    """
    读取 prompts/{topic}/ 下所有 prompt 文件，生成 outputs/{topic}/ 下的结果
    """
    prompt_dir = os.path.join("prompts", topic)
    output_dir = os.path.join("outputs", topic)
    os.makedirs(output_dir, exist_ok=True)
    output_paths=[]
    for filename in os.listdir(prompt_dir):
        if not filename.endswith(".txt"):
            continue

        prompt_path = os.path.join(prompt_dir, filename)

        # 读取 prompt 内容
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()

        print(f"正在处理: {filename}")

        # 模型生成
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs_tensor = model.generate(
            **inputs,
            max_new_tokens=2048,
            do_sample=True,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        result = tokenizer.decode(outputs_tensor[0], skip_special_tokens=True)

        # 去掉 prompt 前缀部分
        if result.startswith(prompt):
            result = result[len(prompt):].strip()

        # 保存结果
        output_path = os.path.join(output_dir, filename.replace("prompt_", "output_"))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"已保存: {output_path}")
        output_paths.append(output_path)
    print(f"所有 prompts/{topic}/ 下的 prompt 处理完毕！")


# prompt_dir = "prompts"
# output_dir = "outputs"
# os.makedirs(output_dir, exist_ok=True)

# for filename in os.listdir(prompt_dir):
#     if filename.endswith(".txt"):
#         prompt_path = os.path.join(prompt_dir, filename)

#         # 读取 prompt 内容
#         with open(prompt_path, "r", encoding="utf-8") as f:
#             prompt = f.read()

#         print(f"正在处理: {filename}")

#         # 模型生成
#         inputs = tokenizer(prompt, return_tensors="pt").to(device)
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=2048,
#             do_sample=True,
#             top_p=0.95,
#             temperature=0.7,
#             pad_token_id=tokenizer.eos_token_id
#         )
#         result = tokenizer.decode(outputs[0], skip_special_tokens=True)

#         # 只截取模型的输出部分（去掉 prompt）
#         if result.startswith(prompt):
#             result = result[len(prompt):].strip()

#         # 保存生成结果
#         output_path = os.path.join(output_dir, filename.replace("prompt_", "output_"))
#         with open(output_path, "w", encoding="utf-8") as f:
#             f.write(result)

#         print(f"已保存: {output_path}")

# print("所有 prompt 已处理完毕！")