# get_json.py 修改后
import os
import sys
import json
from pathlib import Path


def pytest_sessionfinish(session, exitstatus):
    try:
        # 获取 test_case.py 所在目录
        test_case_dir = Path(__file__).parent

        # 创建 result 目录
        result_dir = test_case_dir / "result"
        result_dir.mkdir(exist_ok=True)

        # 从测试模块导入 TEST_RESULTS
        from test_case import TEST_RESULTS

        # 动态获取协议版本
        proto_version = TEST_RESULTS["env_info"]["pickle_protocol"]

        # 构建动态文件名
        output_file = result_dir / (
            f"pickle_results_py{sys.version_info.major}{sys.version_info.minor}"
            f"_proto{proto_version}"
            f"_{sys.platform}.json"
        )

        with open(output_file, 'w') as f:
            json.dump(TEST_RESULTS, f, indent=2, default=str)
        print(f"\n测试结果已保存至: {output_file.resolve()}")
    except Exception as e:
        print(f"\n保存文件失败: {str(e)}")