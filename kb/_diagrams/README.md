---
title: 商业图(_diagrams)说明
type: meta
updated: 2026-06-27
summary: ABI 智能化独立站的海报级商业图(PNG + PDF):总架构、全景、横/纵蓝图、节点能力矩阵。
---

# _diagrams — 海报级商业图(ABI 智能化独立站)

| 图 | 文件 | 看什么 |
|----|------|--------|
| **总架构(新)** | `00_ABI总架构_architecture.(png/pdf)` | 商业价值 + 5 层(信息源→内容→机器→产品→消费)+ 人审闸,**产品与知识库全展示** |
| 全景图 | `01_全景图_panorama.(png/pdf)` | 编排层→11 节点→能力层→数据底座→8 源/产出→横切层 |
| 横向流程蓝图 | `02_横向流程蓝图_horizontal.(png/pdf)` | 00→10 每节点目标/能力/人审 + 复购闭环 |
| 纵向架构蓝图 | `03_纵向架构蓝图_vertical.(png/pdf)` | 大脑(Agent)→手脚(能力)→地基(数据)+ 人审闸 |
| 节点能力矩阵 | `04_节点能力矩阵_matrix.(png/pdf)` | 节点 × Shopify 能力 |
| 全集 | `商业图全集_5页.pdf` | 5 图合订,便于汇报 |

- 格式:PNG(高清)+ PDF(矢量级)。重建:`cd kb/_build && PYTHONPATH=/tmp/shopify-diagram-deps python diag_*.py`(matplotlib + Noto Sans CJK SC;也可使用已安装 matplotlib 的 Python 环境)。
