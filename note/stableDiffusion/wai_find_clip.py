import json
import re


def extract_keys_with_data_prefix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []

    def find_keys(obj, parent_key=''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_key = f"{parent_key}.{key}" if parent_key else key
                current_key = key

                if isinstance(value, str) and value.startswith('data:'):
                    results.append(current_key)
                else:
                    find_keys(value, current_key)

        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                find_keys(item, f"{parent_key}[{i}]")

    find_keys(data)
    return results


def group_by_first_word(text_lines):
    groups = {}

    for line in text_lines:
        line = line.strip()
        if not line or ',' not in line:
            continue

        # 分割第一个逗号
        parts = line.split(',', 1)
        first_word = parts[0].strip()
        rest_of_line = parts[1].strip()

        # 添加到对应的分组
        if first_word not in groups:
            groups[first_word] = []
        groups[first_word].append(f"{first_word}, {rest_of_line}")

    return groups


def process_and_display(text_lines):
    # 按第一个单词分组
    grouped = group_by_first_word(text_lines)

    # 输出结果
    result_lines = []
    for first_word, lines in grouped.items():
        result_lines.extend(lines)
        result_lines.append("")  # 添加空行分隔不同组

    return result_lines


keys = []
for i in range(1,12):
    keys += extract_keys_with_data_prefix(
        fr'C:\Users\Iko\Documents\ComfyUI\models\checkpoints\waiClap\WAI-NSFW-illustrious-character-select\output_{i}.json'
    )
result = process_and_display(keys)

for line in result:
    print(line)