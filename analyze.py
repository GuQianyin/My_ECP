# analyze.py
import json
import glob
from collections import defaultdict


def load_results(pattern="result/pickle_results_*.json"):
    """加载所有结果文件"""
    results = defaultdict(dict)
    for fname in glob.glob(pattern):
        with open(fname) as f:
            data = json.load(f)

            env_info = data['env_info']
            py_ver = env_info['python_version'].split()[0]  # 3.12.4
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
    """改进版报告生成"""
    print("🔍 Pickle序列化兼容性分析报告\n")

    for case, env_data in results.items():
        print(f"\n📌 测试用例: {case}")

        # 构建哈希到环境列表的反向映射
        hash_groups = defaultdict(list)
        for env, hash_val in env_data.items():
            hash_groups[hash_val].append(env)

        # 按哈希组数量排序（最多差异的排前面）
        sorted_groups = sorted(hash_groups.items(),
                               key=lambda x: len(x[1]),
                               reverse=True)

        if len(sorted_groups) == 1:
            print("   ✅ 全环境哈希一致")
            print(f"   🎯 统一哈希: {sorted_groups[0][0][:24]}...")
            print(f"       包含环境: {', '.join(sorted_groups[0][1])}")
        else:
            print(f"   ⚠️ 发现 {len(sorted_groups)} 个哈希组")
            for i, (hash_val, envs) in enumerate(sorted_groups, 1):
                print(f"\n   组 #{i} (哈希: {hash_val[:24]}...)")
                print(f"   └ 包含 {len(envs)} 个环境:")
                for env in envs:
                    print(f"      ▪ {env}")
if __name__ == "__main__":
    all_results = load_results()
    generate_report(all_results)