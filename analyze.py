# analyze.py
import json
import glob
from collections import defaultdict
from pathlib import Path


def load_results(base_dir):
    """加载指定目录下的所有结果文件"""
    results = defaultdict(dict)
    pattern = str(Path(base_dir) / "pickle_results_*.json")

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


def generate_report(results, base_dir):
    """生成带场景标识的Markdown报告"""
    # 根据目录名称生成场景描述
    scenario_map = {
        "result_different_system": "不同操作系统间",
        "result_different_python_version": "不同Python版本间"
    }
    scenario = scenario_map.get(base_dir, "跨环境")

    report = [
        f"# 🔍 Pickle序列化兼容性分析报告（{scenario}）\n",
        f"**分析场景**: `{base_dir}` 目录结果\n"
    ]

    # 分类逻辑保持不变...
    diff_cases = []
    same_cases = []

    for case, env_data in results.items():
        hash_groups = defaultdict(list)
        for env, hash_val in env_data.items():
            hash_groups[hash_val].append(env)

        sorted_groups = sorted(hash_groups.items(),
                               key=lambda x: len(x[1]),
                               reverse=True)

        if len(sorted_groups) > 1:
            diff_cases.append((case, sorted_groups))
        else:
            same_cases.append((case, sorted_groups))

    if diff_cases:
        report.append("\n## 🚨 存在哈希值不一致的用例")
        for case, sorted_groups in diff_cases:
            report.append(f"\n### 📌 测试用例: {case}")
            report.append(f"⚠️ **发现 {len(sorted_groups)} 个哈希组**")

            for i, (hash_val, envs) in enumerate(sorted_groups, 1):
                report.append(f"\n#### 组 #{i}")
                report.append(f"- 哈希: `{hash_val[:24]}...`")
                report.append(f"- 包含 {len(envs)} 个环境:")
                report.append("\n".join([f"  - {env}" for env in envs]))

    if same_cases:
        report.append("\n## ✅ 哈希值一致的用例")
        for case, sorted_groups in same_cases:
            report.append(f"\n### 📌 测试用例: {case}")
            report.append(f"🎯 统一哈希: `{sorted_groups[0][0][:24]}...`\n")
            report.append("**包含环境:**\n- " + "\n- ".join(sorted_groups[0][1]))

    return "\n".join(report)


def save_report(content, base_dir):
    """保存到对应目录的报告文件"""
    filename = Path(base_dir) / "pickle_compatibility_report.md"
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.write_text(content, encoding='utf-8')
    return filename


if __name__ == "__main__":
    # 同时处理两个分析场景
    for analysis_scenario in [
        "result_different_system",
        "result_different_python_version"
    ]:
        print(f"\n正在处理场景: {analysis_scenario}...")
        results = load_results(analysis_scenario)
        report = generate_report(results, analysis_scenario)
        output_path = save_report(report, analysis_scenario)
        print(f"报告已生成至: {output_path.resolve()}")