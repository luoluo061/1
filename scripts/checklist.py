"""Generate a textual checklist for reviewers.

The checklist is a convenience for manual QA to ensure各模块依赖关系、配置文件、示例数据
以及测试套件齐备。本脚本不会执行任何外部操作，仅打印结构化清单供参考。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

CHECKS = [
    "配置文件存在：trait_schema.yaml、vector_schema.yaml、weights_default.yaml、similarity.yaml、profile_rules.yaml",
    "示例数据完整：examples/demo_data.csv >= 30 行，demo_weights.yaml 包含多套方案",
    "docs 目录包含接口、配置、数据结构、流程与算法说明",
    "scripts 目录包含 gen_docs.py、validate_inputs.py、preview_profiles.py",
    "tests 目录包含 12+ 个测试模块覆盖关键环节",
    "src 分层完整：domain、ingestion、normalization、feature_engineering、weighting、similarity、profiling、storage、evaluation、utils",
]


@dataclass
class ChecklistItem:
    description: str
    done: bool = False

    def render(self) -> str:
        status = "[x]" if self.done else "[ ]"
        return f"- {status} {self.description}"


def build_checklist(descriptions: List[str]) -> List[ChecklistItem]:
    return [ChecklistItem(description=item) for item in descriptions]


def render_checklist(items: List[ChecklistItem]) -> str:
    lines = [item.render() for item in items]
    return "\n".join(lines)


def main() -> None:
    items = build_checklist(CHECKS)
    print("项目检查清单：")
    print(render_checklist(items))


if __name__ == "__main__":
    main()
