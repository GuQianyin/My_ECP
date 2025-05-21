import json
import glob
from collections import defaultdict
from pathlib import Path


def load_results(pattern="result/pickle_results_*.json"):
    """加载所有结果文件"""
    results = defaultdict(dict)
    for fname in glob.glob(pattern):
        with open(fname) as f:
            data = json.load(f)

            env_info = data['env_info']
            py_ver = env_info['python_version'].split()[0]
            proto = env_info['pickle_protocol']
            platform = env_info['platform']

            env_key = (
                f"Python {py_ver} "
                f"Protocol {proto} "
                f"{platform}"
            )

            for case, value in data['valid_cases'].items():
                results[case][env_key] = value
    return results


def generate_report(results):
    """生成Markdown格式报告内容（按差异优先分组）"""
    report = ["# 🔍 Pickle序列化兼容性分析报告\n"]

    # 分类存储用例
    diff_cases = []  # 存在差异的用例（多个哈希组）
    same_cases = []  # 全环境一致的用例（单个哈希组）

    for case, env_data in results.items():
        # 构建哈希到环境列表的反向映射
        hash_groups = defaultdict(list)
        for env, hash_val in env_data.items():
            hash_groups[hash_val].append(env)

        # 按哈希组数量排序（最多差异的排前面）
        sorted_groups = sorted(hash_groups.items(),
                               key=lambda x: len(x[1]),
                               reverse=True)

        # 分类存储用例信息（包含排序后的哈希组）
        if len(sorted_groups) > 1:
            diff_cases.append((case, sorted_groups))
        else:
            same_cases.append((case, sorted_groups))

    # 优先展示存在差异的用例
    if diff_cases:
        report.append("\n## 🚨 哈希值不一致的用例")
        for case, sorted_groups in diff_cases:
            report.append(f"\n### 📌 测试用例: {case}")
            report.append(f"⚠️ **发现 {len(sorted_groups)} 个哈希组**")

            for i, (hash_val, envs) in enumerate(sorted_groups, 1):
                report.append(f"\n#### 组 #{i}")
                report.append(f"- 哈希: `{hash_val[:24]}...`")
                report.append(f"- 包含 {len(envs)} 个环境:")
                report.append("\n".join([f"  - {env}" for env in envs]))

    # 展示全环境一致的用例
    if same_cases:
        report.append("\n## ✅ 哈希值一致的用例")
        for case, sorted_groups in same_cases:
            report.append(f"\n### 📌 测试用例: {case}")
            report.append(f"🎯 统一哈希: `{sorted_groups[0][0][:24]}...`\n")
            report.append("**包含环境:**\n- " + "\n- ".join(sorted_groups[0][1]))

    return "\n".join(report)


def save_report(content, filename="result/pickle_compatibility_report.md"):
    """保存报告到文件"""
    path = Path(filename)
    path.parent.mkdir(exist_ok=True)  # 确保目录存在
    path.write_text(content, encoding='utf-8')
    return path


if __name__ == "__main__":
    all_results = load_results()
    report_content = generate_report(all_results)
    output_path = save_report(report_content)
    print(f"报告已生成至: {output_path.resolve()}")