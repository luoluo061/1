"""打印系统概览，包括目录、配置文件与模块用途。

该脚本面向软著撰写阶段的快速自检，可在无外部依赖的情况下运行，输出描述性
信息而不是执行真实计算。
"""

from __future__ import annotations

from pathlib import Path
from typing import List

PROJECT_DIRS = [
    "configs",
    "docs",
    "examples",
    "scripts",
    "src/flower_trait_modeling",
    "tests",
]

MODULES = [
    "domain",
    "ingestion",
    "normalization",
    "feature_engineering",
    "weighting",
    "similarity",
    "profiling",
    "storage",
    "evaluation",
    "utils",
    "analysis",
    "policies",
    "reporting",
]

DOCUMENTATION_NOTES = [
    "- 接口文档位于 docs/interfaces.md，包含主要入口函数说明。",
    "- 配置说明位于 docs/configs.md，描述 YAML 字段与含义。",
    "- 数据结构列表见 docs/data_structures.md，帮助审阅属性范围。",
    "- 运行流程说明见 docs/workflow.md，概述 ingestion -> normalization -> vector -> similarity -> profiling 链路。",
    "- 算法说明见 docs/algorithms.md，列出关键处理器与度量方法。",
    "- 自动生成文档的脚本为 scripts/gen_docs.py，可在配置变更后更新 Markdown。",
    "- 示例预览脚本 scripts/preview_profiles.py 可用于生成少量画像供人工检查。",
    "- validate_inputs.py 会读取配置，确保 trait 与 vector schema 一致。",
    "- checklist.py 输出软著交付检查项，适合人工核对。",
    "- run_overview.py 本脚本即可快速确认目录与模块是否齐全。",
]

RESOURCE_NOTES = [
    "- examples/demo_data.csv 提供 30+ 行样例，涵盖形态、颜色、长度与瓶插期。",
    "- examples/demo_weights.yaml 包含多套权重方案供对比测试。",
    "- examples/demo_profiles/ 目录展示画像输出结构参考。",
    "- configs/profile_rules.yaml 控制画像版块与阈值，便于写作描述。",
]


def list_dir_status() -> List[str]:
    lines = []
    for directory in PROJECT_DIRS:
        path = Path(directory)
        status = "存在" if path.exists() else "缺失"
        lines.append(f"- {directory}: {status}")
    return lines


def list_module_summary() -> List[str]:
    return [f"- {module}: 负责 {module} 子域核心逻辑" for module in MODULES]


def main() -> None:
    print("项目目录状态：")
    for line in list_dir_status():
        print(line)
    print("\n模块说明：")
    for line in list_module_summary():
        print(line)
    print("\n文档提示：")
    for note in DOCUMENTATION_NOTES:
        print(note)
    print("\n资源提示：")
    for note in RESOURCE_NOTES:
        print(note)
    print("\n附加说明：所有代码均带类型注解和 docstring，便于软著材料引用。")
    print("若需更新示例或配置，请同步刷新 docs/generated_*.md 以保持一致性。")
    print("软著名称：鲜花品种性状参数建模系统。")
    print("业务覆盖：数据结构、标准化、向量构建、权重、相似度、画像、评估。")
    print("演示脚本可独立运行，不依赖外部数据库或网络。")
    print("\n配置提示：修改 configs/ 下的 YAML 可驱动字段、权重、相似度与画像规则变化。")


if __name__ == "__main__":
    main()
