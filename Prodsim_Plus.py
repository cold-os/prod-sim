import re
import os
import json
from typing import List, Dict, Optional, Any, Tuple
from dashscope import Generation
import dashscope
from datetime import datetime
from enum import Enum

# 设置API基础URL
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'


# ===================== 生产知识框架 =====================
class ProductionKnowledgeFramework:
    """生产知识框架 - 存储生产流程、失效模式、专家规则等知识"""

    def __init__(self):
        # 基础框架库
        self.frameworks = {
            "process_flow_analysis": self._get_process_flow_framework(),
            "fmea_framework": self._get_fmea_framework(),
            "quality_gate_criteria": self._get_quality_gate_framework(),
            "historical_issue_database": self._get_historical_issues(),
            "expert_experience_rules": self._get_expert_rules()
        }

        # 智能体与框架映射
        self.agent_framework_map = {
            "ai_simulation": "fmea_framework",
            "expert_review": "expert_experience_rules",
            "worker_validation": "quality_gate_criteria"
        }

        self.loaded_framework = None
        self.current_mode = None

    def _get_process_flow_framework(self) -> Dict[str, Any]:
        """工艺流程分析框架"""
        return {
            "name": "工艺流程分析",
            "description": "用于分析生产流程的各个环节及其依赖关系",
            "dimensions": {
                "input_requirements": {
                    "name": "输入要求",
                    "description": "环节所需的原材料、零部件、信息等输入",
                    "analysis_questions": [
                        "输入规格是否符合标准？",
                        "供应商质量是否稳定？",
                        "库存管理是否存在风险？"
                    ]
                },
                "process_parameters": {
                    "name": "工艺参数",
                    "description": "设备参数、环境条件、操作标准等",
                    "analysis_questions": [
                        "参数设置是否在安全范围内？",
                        "设备状态是否正常？",
                        "环境温湿度是否达标？"
                    ]
                },
                "output_quality": {
                    "name": "输出质量",
                    "description": "产品质量特征、合格率、缺陷类型等",
                    "analysis_questions": [
                        "关键质量特性是否达标？",
                        "缺陷模式有哪些？",
                        "过程能力指数如何？"
                    ]
                }
            },
            "application_guidance": "分析生产环节时，按输入-过程-输出三个维度系统检查"
        }

    def _get_fmea_framework(self) -> Dict[str, Any]:
        """失效模式与影响分析框架"""
        return {
            "name": "FMEA框架",
            "description": "识别潜在失效模式及其影响和严重度",
            "failure_categories": {
                "equipment_failure": {
                    "name": "设备失效",
                    "examples": ["机械故障", "电气故障", "传感器漂移", "软件错误"],
                    "severity_scale": "1-10，10为最严重"
                },
                "material_issue": {
                    "name": "材料问题",
                    "examples": ["尺寸超差", "材质不良", "批次差异", "污染"],
                    "severity_scale": "1-10，10为最严重"
                },
                "human_error": {
                    "name": "人为失误",
                    "examples": ["操作错误", "装配漏项", "检验疏忽", "参数设置错误"],
                    "severity_scale": "1-10，10为最严重"
                },
                "environmental_factor": {
                    "name": "环境因素",
                    "examples": ["温湿度异常", "振动干扰", "电源波动", "粉尘污染"],
                    "severity_scale": "1-10，10为最严重"
                }
            },
            "analysis_process": [
                "识别潜在失效模式",
                "评估失效影响和严重度",
                "分析失效原因和发生频率",
                "评估当前检测手段的有效性",
                "计算风险优先数(RPN)"
            ]
        }

    def _get_quality_gate_framework(self) -> Dict[str, Any]:
        """质量门控标准框架"""
        return {
            "name": "质量门控标准",
            "description": "定义各环节的质量验收标准和检查方法",
            "gates": {
                "incoming_inspection": {
                    "name": "来料检验",
                    "criteria": ["尺寸检查", "材质证明", "外观检查", "功能测试"],
                    "acceptance_level": "AQL 0.65"
                },
                "in_process_check": {
                    "name": "过程检验",
                    "criteria": ["首件检验", "巡检频率", "关键特性监控", "设备点检"],
                    "acceptance_level": "CpK ≥ 1.33"
                },
                "final_inspection": {
                    "name": "最终检验",
                    "criteria": ["全尺寸检查", "性能测试", "外观终检", "包装检查"],
                    "acceptance_level": "零缺陷"
                }
            },
            "escalation_rules": {
                "minor_defect": "记录并继续生产，下批次前解决",
                "major_defect": "暂停生产，立即分析原因",
                "critical_defect": "全线停产，追溯所有受影响产品"
            }
        }

    def _get_historical_issues(self) -> Dict[str, Any]:
        """历史问题数据库"""
        return {
            "name": "历史问题库",
            "description": "记录过往发生的生产问题及解决方案",
            "issue_categories": {
                "recurrent_issues": {
                    "name": "重复发生问题",
                    "examples": ["某型号螺栓松动", "传感器误报", "软件死机"],
                    "root_causes": ["设计缺陷", "维护不足", "培训不到位"]
                },
                "seasonal_issues": {
                    "name": "季节性/周期性问题",
                    "examples": ["夏季高温导致设备过热", "梅雨季电路板受潮"],
                    "patterns": ["温度相关", "湿度相关", "人员变动期"]
                },
                "supplier_issues": {
                    "name": "供应商相关问题",
                    "examples": ["批次质量波动", "交货延迟", "规格不符"],
                    "mitigations": ["增加检验频次", "开发第二供应商", "加强供应商审核"]
                }
            },
            "lessons_learned": [
                "关键设备必须有备用方案",
                "重要参数必须双重校验",
                "变更必须经过评审和验证"
            ]
        }

    def _get_expert_rules(self) -> Dict[str, Any]:
        """专家经验规则库"""
        return {
            "name": "专家经验规则",
            "description": "资深工程师和老师的经验法则",
            "heuristics": {
                "equipment_maintenance": [
                    "听声音：异常响声往往是故障前兆",
                    "看振动：异常振动表明部件磨损",
                    "闻气味：烧焦味立即停机检查"
                ],
                "quality_judgment": [
                    "尺寸问题看工装，装配问题看手法",
                    "外观问题看光源，性能问题看参数",
                    "偶发问题查环境，频发问题查系统"
                ],
                "troubleshooting": [
                    "从最简单、最可能的原因开始排查",
                    "一次只改变一个变量进行测试",
                    "记录完整的过程和数据供后续分析"
                ]
            },
            "decision_rules": {
                "when_to_stop": "连续3件不合格或关键特性超差立即停机",
                "when_to_escalate": "问题30分钟内未解决必须上报",
                "when_to_accept": "让步接收必须获得技术和质量双签批"
            }
        }

    def load_framework_for_mode(self, mode: str) -> bool:
        """根据模式加载对应的框架"""
        self.current_mode = mode
        framework_key = self.agent_framework_map.get(mode)

        if framework_key and framework_key in self.frameworks:
            self.loaded_framework = self.frameworks[framework_key]
            return True
        return False

    def get_guidance_for_mode(self, mode: str, question: str) -> str:
        """获取特定模式的认知框架指导"""
        if not self.loaded_framework or self.current_mode != mode:
            self.load_framework_for_mode(mode)

        if not self.loaded_framework:
            return "【生产知识框架指导】\n未加载认知框架\n\n"

        mode_descriptions = {
            "ai_simulation": "AI模拟推演",
            "expert_review": "专家审核修正",
            "worker_validation": "工人实证检验"
        }

        mode_desc = mode_descriptions.get(mode, "生产分析")

        guidance = f"【{self.loaded_framework['name']}指导】\n"
        guidance += f"模式：{mode_desc}\n"
        guidance += f"描述：{self.loaded_framework['description']}\n\n"

        # 添加模式特定的指导
        if mode == "ai_simulation":
            guidance += "● 模拟推演要点:\n"
            guidance += "  1. 基于FMEA框架识别潜在失效模式\n"
            guidance += "  2. 分析失效原因、影响和严重度\n"
            guidance += "  3. 参考历史问题库识别类似模式\n"
            guidance += "  4. 生成带置信度分级的问题假设\n"

            if 'failure_categories' in self.loaded_framework:
                guidance += "\n● 失效类别参考:\n"
                for cat_key, cat_info in self.loaded_framework['failure_categories'].items():
                    guidance += f"  - {cat_info['name']}: {', '.join(cat_info['examples'][:2])}\n"

        elif mode == "expert_review":
            guidance += "● 专家审核要点:\n"
            guidance += "  1. 基于实际经验检验模拟的合理性\n"
            guidance += "  2. 补充被忽略的关键风险点\n"
            guidance += "  3. 提供具体可行的解决方案\n"
            guidance += "  4. 评估问题发生的实际概率\n"

            if 'heuristics' in self.loaded_framework:
                guidance += "\n● 专家经验参考:\n"
                for rule_type, rules in self.loaded_framework['heuristics'].items():
                    guidance += f"  - {rule_type}: {rules[0]}\n"

        elif mode == "worker_validation":
            guidance += "● 实证检验要点:\n"
            guidance += "  1. 评估问题假设的可观测性\n"
            guidance += "  2. 设计简单有效的验证方案\n"
            guidance += "  3. 考虑验证过程的安全性和成本\n"
            guidance += "  4. 提供数据记录和反馈方法\n"

            if 'gates' in self.loaded_framework:
                guidance += "\n● 质量门控参考:\n"
                for gate_key, gate_info in self.loaded_framework['gates'].items():
                    guidance += f"  - {gate_info['name']}: {gate_info['criteria'][0]}\n"

        guidance += f"\n【问题分析】\n{question}\n"
        return guidance


# 全局生产知识框架实例
production_framework = ProductionKnowledgeFramework()


# ===================== 置信度三元组解析器（优化版） =====================
class ConfidenceTripletExtractor:
    """解析置信度三元组（我确信的/我推测的/我不知道的）"""

    @staticmethod
    def extract_triplets(text: str) -> Dict[str, List[str]]:
        """从文本中提取三个置信度类别的内容 - 优化版本"""
        triplets = {
            "confident": [],  # 我确信的
            "speculative": [],  # 我推测的
            "unknown": []  # 我不知道的
        }

        if not text:
            return triplets

        # 定义匹配模式 - 优化模式，更好地处理多种格式
        patterns = {
            "confident": [
                r'【我确信的】[^】]*?(?=【|$)',
                r'我确信的[：:\s]*([^】]*?)(?=【|$)',
                r'【我确信的】\s*(.*?)(?=【我推测的】|【我不知道的】|$)',
                r'我确信的\s*(.*?)(?=我推测的|我不知道的|$)',
                r'【确信】[^】]*?(?=【|$)',
                r'确信[：:\s]*([^】]*?)(?=【|$)'
            ],
            "speculative": [
                r'【我推测的】[^】]*?(?=【|$)',
                r'我推测的[：:\s]*([^】]*?)(?=【|$)',
                r'【我推测的】\s*(.*?)(?=【我确信的】|【我不知道的】|$)',
                r'我推测的\s*(.*?)(?=我确信的|我不知道的|$)',
                r'【推测】[^】]*?(?=【|$)',
                r'推测[：:\s]*([^】]*?)(?=【|$)'
            ],
            "unknown": [
                r'【我不知道的】[^】]*?(?=【|$)',
                r'我不知道的[：:\s]*([^】]*?)(?=【|$)',
                r'【我不知道的】\s*(.*?)(?=【我确信的】|【我推测的】|$)',
                r'我不知道的\s*(.*?)(?=我确信的|我推测的|$)',
                r'【未知】[^】]*?(?=【|$)',
                r'未知[：:\s]*([^】]*?)(?=【|$)'
            ]
        }

        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    content = match if isinstance(match, str) else match[0] if match else ""
                    if content.strip():
                        # 使用多种方式分割内容
                        items = []

                        # 尝试按数字编号分割（1. 2. 3.）
                        numbered_items = re.split(r'\d+[\.、]', content)
                        if len(numbered_items) > 1:
                            items.extend([item.strip() for item in numbered_items if item.strip()])

                        # 尝试按项目符号分割
                        bullet_items = re.split(r'[•\-\*•·▶▪▸]', content)
                        if len(bullet_items) > 1:
                            items.extend([item.strip() for item in bullet_items if item.strip()])

                        # 尝试按换行分割
                        line_items = re.split(r'[\n\r]+', content)
                        if len(line_items) > 1:
                            items.extend([item.strip() for item in line_items if item.strip()])

                        # 如果以上都没有分割成功，使用整个内容
                        if not items:
                            items = [content.strip()]

                        # 清理和过滤项目
                        for item in items:
                            if item and len(item) > 3:  # 过滤掉过短的内容
                                # 移除多余的空格和标点
                                item_clean = re.sub(r'^[:\-\s]*', '', item)
                                item_clean = re.sub(r'[\s。\.]+$', '', item_clean)

                                # 确保以完整句子结束
                                if not item_clean.endswith(('.', '。', '?', '？', '!', '！')):
                                    item_clean += '.'

                                triplets[category].append(item_clean)

        # 去重
        for category in triplets:
            triplets[category] = list(dict.fromkeys(triplets[category]))

        return triplets

    @staticmethod
    def format_triplets(triplets: Dict[str, List[str]]) -> str:
        """格式化三元组为可读文本"""
        output = []

        if triplets.get("confident"):
            output.append("【我确信的】")
            for idx, item in enumerate(triplets["confident"], 1):
                output.append(f"{idx}. {item}")

        if triplets.get("speculative"):
            output.append("\n【我推测的】")
            for idx, item in enumerate(triplets["speculative"], 1):
                output.append(f"{idx}. {item}")

        if triplets.get("unknown"):
            output.append("\n【我不知道的】")
            for idx, item in enumerate(triplets["unknown"], 1):
                output.append(f"{idx}. {item}")

        return "\n".join(output)

    @staticmethod
    def calculate_similarity(triplets1: Dict[str, List[str]], triplets2: Dict[str, List[str]]) -> float:
        """计算两个三元组之间的相似度 - 优化版本"""
        if not triplets1 or not triplets2:
            return 0.0

        total_similarity = 0
        category_count = 0

        for category in ["confident", "speculative", "unknown"]:
            list1 = triplets1.get(category, [])
            list2 = triplets2.get(category, [])

            if not list1 and not list2:
                continue

            # 使用文本相似度计算
            similarity = 0
            if list1 and list2:
                # 将列表转换为文本
                text1 = " ".join([item[:30] for item in list1])  # 取前30字符进行比较
                text2 = " ".join([item[:30] for item in list2])

                # 简单的Jaccard相似度
                words1 = set(text1.split())
                words2 = set(text2.split())

                if words1 or words2:
                    intersection = len(words1.intersection(words2))
                    union = len(words1.union(words2))
                    similarity = intersection / union if union > 0 else 0
            elif not list1 and not list2:
                similarity = 1.0

            total_similarity += similarity
            category_count += 1

        return total_similarity / category_count if category_count > 0 else 0


# ===================== 生产认知提示词模板 =====================
def create_production_prompt(question: str, is_first_layer: bool = True,
                             previous_response: str = "", previous_critique: str = "",
                             layer_num: int = 1, mode: str = "ai_simulation") -> str:
    """创建生产认知领域提示词 - 支持三种模式"""

    # 获取当前认知框架指导
    framework_guidance = production_framework.get_guidance_for_mode(mode, question)

    # 基础约束
    base_constraints = """重要要求：
1. 所有分析必须基于生产知识和实际情况
2. 必须清晰区分已知事实和推测假设
3. 必须按照以下三个类别组织分析内容
4. 每个类别必须包含3-8个具体的要点
5. 语言精炼，避免重复和过度论证
6. 每个要点必须以完整句子的形式呈现
7. 参考生产知识框架进行分析，但必须结合具体生产场景"""

    mode_descriptions = {
        "ai_simulation": "AI模拟推演",
        "expert_review": "专家审核修正",
        "worker_validation": "工人实证检验"
    }

    current_mode_desc = mode_descriptions.get(mode, "生产分析")

    if is_first_layer:
        if mode == "ai_simulation":
            prompt = f"""你是一个生产模拟AI，专门推演生产过程中可能的问题。请基于生产知识框架进行问题推演，并严格按格式输出。

{framework_guidance}

{base_constraints}

【AI模拟推演任务】
请系统性地推演以下生产环节可能出现的问题：

1. **设备/工具相关风险**：考虑设备故障、工具磨损、参数设置等问题
2. **材料/零部件相关风险**：考虑尺寸偏差、材质不良、批次差异等问题  
3. **人员操作相关风险**：考虑操作失误、检验漏项、技能不足等问题
4. **环境/参数相关风险**：考虑温湿度异常、振动干扰、电源波动等问题
5. **系统/流程相关风险**：考虑流程设计缺陷、信息传递错误、接口不匹配等问题

【输出格式要求】
必须严格按照以下格式组织输出，使用中文标点：

【我确信的】
1. [具体的风险描述，包括原因和影响]
2. [具体的风险描述，包括原因和影响]
3. [具体的风险描述，包括原因和影响]

【我推测的】
1. [基于逻辑推断的可能风险]
2. [基于逻辑推断的可能风险]
3. [基于逻辑推断的可能风险]

【我不知道的】
1. [需要实际数据验证的假设]
2. [需要专家经验确认的疑问]
3. [需要现场观察验证的现象]

注意：每个要点都必须是完整的句子，以句号结束。

生产环节: {question}

请开始问题推演:"""

        elif mode == "expert_review":
            prompt = f"""你是一个经验丰富的生产专家，请审核AI的模拟推演并补充修正。

{framework_guidance}

{base_constraints}

【专家审核任务】
请从专家视角审核以下AI模拟推演：

1. **经验准确性检查**：基于实际经验检验模拟的合理性
2. **风险完整性检查**：补充AI忽略的关键风险点
3. **解决方案提供**：提供具体可行的改进建议
4. **优先级评估**：评估各问题的实际发生概率和紧急程度
5. **数据补充**：补充实际生产数据、PPM值、维修成本等信息

【输出格式要求】
必须严格按照以下格式组织输出，使用中文标点：

【我确信的】
1. [经过专家确认的关键问题，包括实际数据和案例]
2. [经过专家确认的关键问题，包括实际数据和案例]
3. [经过专家确认的关键问题，包括实际数据和案例]

【我推测的】
1. [需要进一步观察的潜在风险]
2. [需要进一步观察的潜在风险]
3. [需要进一步观察的潜在风险]

【我不知道的】
1. [需要实际数据验证的假设]
2. [需要跨部门协调解决的问题]
3. [需要专业技术支持的疑问]

注意：每个要点都必须是完整的句子，以句号结束。

AI模拟推演: {question}

请开始专家审核:"""

        else:  # worker_validation
            prompt = f"""你是一个一线生产工人，请检验问题假设的实际可观测性并设计验证方案。

{framework_guidance}

{base_constraints}

【实证检验任务】
请从工人视角评估以下问题假设：

1. **可观测性评估**：哪些问题在实际生产中容易被观察到？
2. **验证方案设计**：需要什么工具或方法进行验证？
3. **操作便利性**：验证过程是否便于一线工人操作？
4. **成本效益分析**：验证成本是否合理？效果如何？
5. **安全风险考虑**：验证过程是否存在安全隐患？
6. **数据记录方法**：如何记录和反馈验证结果？

【输出格式要求】
必须严格按照以下格式组织输出，使用中文标点：

【我确信的】
1. [可立即验证的问题指标和具体验证方法]
2. [可立即验证的问题指标和具体验证方法]
3. [可立即验证的问题指标和具体验证方法]

【我推测的】
1. [需要创造条件验证的假设和验证思路]
2. [需要创造条件验证的假设和验证思路]
3. [需要创造条件验证的假设和验证思路]

【我不知道的】
1. [难以验证或需要专业设备的项目]
2. [需要技术部门支持解决的难题]
3. [需要投入大量资源才能验证的内容]

注意：每个要点都必须是完整的句子，以句号结束。

待验证问题: {question}

请开始实证检验规划:"""

    else:
        # 后续层增加更严格的约束
        layer_constraints = ""
        if layer_num == 2:
            layer_constraints = """【第二轮思考特别要求】
1. 精准针对质疑点进行修正，不要全面重写
2. 每个类别保持3-5个最核心的要点
3. 总分析长度控制在600字以内
4. 重点修正被质疑的具体推断"""
        else:  # 第三层
            layer_constraints = """【最终轮思考特别要求】
1. 只保留经过验证的最核心要点
2. 每个类别3-4个最关键认知洞察
3. 总分析长度控制在500字以内
4. 聚焦于达成共识的内容"""

        prompt = f"""基于前一轮的批判，进行精准修正：

原始问题: {question}

前一轮{current_mode_desc}:
{previous_response}

前一轮批判要点:
{previous_critique}

{base_constraints}
{layer_constraints}

请基于批判进行精准改进：
1. 必须正面回应质疑者的具体质疑点
2. 对于质疑者指出的问题，要么用证据捍卫，要么降级置信度类别
3. 保持认知分析的严谨性，避免过度推断
4. 必须严格按照三个类别重新组织分析
5. 重点：修正而非扩充，保持内容精炼

改进后的{current_mode_desc}:"""

    return prompt


# ===================== 生产思考层核心组件 =====================
class ProductionThinkingLayer:
    """生产思考层：单轮建构-质疑-观察的完整流程"""

    def __init__(self, layer_num: int, question: str, mode: str,
                 previous_response: str = "", previous_critique: str = ""):
        self.layer_num = layer_num
        self.question = question
        self.mode = mode
        self.previous_response = previous_response
        self.previous_critique = previous_critique
        self.response = ""
        self.critique = ""
        self.confidence_triplets = {"confident": [], "speculative": [], "unknown": []}
        self.final_triplets = {"confident": [], "speculative": [], "unknown": []}
        self.confidence_score = 0.0
        self.critique_validity = 0.0
        self.should_terminate_early = False
        self.stability_similarity = 0.0

    def execute(self) -> Dict[str, Any]:
        """执行单层思考流程"""
        mode_descriptions = {
            "ai_simulation": "AI模拟推演",
            "expert_review": "专家审核",
            "worker_validation": "实证检验"
        }
        mode_desc = mode_descriptions.get(self.mode, "生产分析")

        print(f"\n--- 第{self.layer_num}层{mode_desc}思考 ---")

        # 建构者生成分析
        self.response = self._constructor_generate()
        print(f"建构者生成完成 (长度: {len(self.response)}字符)")

        # 提取置信度三元组
        self.confidence_triplets = ConfidenceTripletExtractor.extract_triplets(self.response)
        print(f"初始三元组 - 确信: {len(self.confidence_triplets['confident'])}, "
              f"推测: {len(self.confidence_triplets['speculative'])}, "
              f"未知: {len(self.confidence_triplets['unknown'])}")

        # 检查内容稳定性（第二层及以上）
        if self.layer_num > 1:
            self.stability_similarity = self._check_content_stability()
            if self.stability_similarity > 0.65:  # 降低阈值到0.65
                print(f"🔍 内容已稳定，相似度 {self.stability_similarity:.2f}，建议提前终止")
                self.should_terminate_early = True
                return self._create_early_termination_result()

        # 质疑者批判
        self.critique = self._critic_critique()
        print(f"质疑者批判完成")

        # 观察者评估并生成最终三元组
        observer_result = self._observer_evaluate()
        self.final_triplets = observer_result["final_triplets"]
        self.confidence_score = observer_result["confidence_score"]
        self.critique_validity = observer_result["critique_validity"]

        print(f"观察者评估: 置信度{self.confidence_score:.2f}, "
              f"批判有效性{self.critique_validity:.2f}")
        print(f"最终三元组 - 确信: {len(self.final_triplets['confident'])}, "
              f"推测: {len(self.final_triplets['speculative'])}, "
              f"未知: {len(self.final_triplets['unknown'])}")

        return {
            "layer": self.layer_num,
            "mode": self.mode,
            "response": self.response,
            "critique": self.critique,
            "initial_triplets": self.confidence_triplets,
            "final_triplets": self.final_triplets,
            "confidence_score": self.confidence_score,
            "critique_validity": self.critique_validity,
            "should_terminate_early": self.should_terminate_early,
            "stability_similarity": self.stability_similarity
        }

    def _constructor_generate(self) -> str:
        """建构者生成分析"""
        is_first_layer = not self.previous_response

        prompt = create_production_prompt(
            question=self.question,
            is_first_layer=is_first_layer,
            previous_response=self.previous_response,
            previous_critique=self.previous_critique,
            layer_num=self.layer_num,
            mode=self.mode
        )

        role_mapping = {
            "ai_simulation": "production_simulator",
            "expert_review": "production_expert",
            "worker_validation": "production_worker"
        }
        role = role_mapping.get(self.mode, "production_default")

        return call_qwen(prompt, role, temperature=0.1)

    def _critic_critique(self) -> str:
        """质疑者提出认知批判"""

        mode_descriptions = {
            "ai_simulation": "AI模拟推演",
            "expert_review": "专家审核",
            "worker_validation": "实证检验"
        }
        mode_desc = mode_descriptions.get(self.mode, "生产分析")

        if self.mode == "ai_simulation":
            prompt = f"""你是一个严格的生产问题审查者，请针对以下AI模拟推演进行批判：

生产环节: {self.question}

建构者AI模拟推演:
{self.response}

【AI模拟推演质疑要求】
请从以下方面提出具体质疑：

1. **逻辑合理性**：推演的问题是否符合生产实际逻辑？是否存在过于理论化的假设？
2. **风险覆盖度**：是否遗漏了重要的风险类别或关键控制点？
3. **假设依据**：推测的问题是否有合理的依据和证据支撑？
4. **可验证性**：提出的问题是否具备可观测性和可验证性？
5. **严重度评估**：风险严重度评估是否准确合理？

请输出聚焦的批判内容，指出具体问题并提供改进建议（限制在400字以内）："""

        elif self.mode == "expert_review":
            prompt = f"""你是一个严格的生产专家审查者，请针对以下专家审核进行批判：

原始问题: {self.question}

建构者专家审核:
{self.response}

【专家审核质疑要求】
请从以下方面提出具体质疑：

1. **经验准确性**：专家经验是否准确可靠？是否有实际数据支撑？
2. **方案可行性**：提出的解决方案是否实际可行？实施成本如何？
3. **优先级合理性**：问题优先级排序是否合理？紧急程度评估是否准确？
4. **风险评估**：风险概率评估是否有依据？是否考虑了实际情况？
5. **数据完整性**：补充的数据是否完整可信？来源是否可靠？

请输出聚焦的批判内容，指出具体问题并提供改进建议（限制在400字以内）："""

        else:  # worker_validation
            prompt = f"""你是一个严格的实证检验审查者，请针对以下实证检验规划进行批判：

待验证问题: {self.question}

建构者实证检验规划:
{self.response}

【实证检验质疑要求】
请从以下方面提出具体质疑：

1. **可操作性**：验证方案是否便于一线工人操作？是否需要特殊技能？
2. **成本效益**：验证成本是否合理？投入产出比如何？
3. **安全性**：验证过程是否存在安全隐患？是否有安全措施？
4. **数据质量**：验证结果是否易于记录和反馈？数据可靠性如何？
5. **时效性**：验证过程是否影响生产节拍？耗时是否合理？

请输出聚焦的批判内容，指出具体问题并提供改进建议（限制在400字以内）："""

        role_mapping = {
            "ai_simulation": "production_critic_simulation",
            "expert_review": "production_critic_expert",
            "worker_validation": "production_critic_worker"
        }
        role = role_mapping.get(self.mode, "production_critic_default")

        return call_qwen(prompt, role, temperature=0.3)

    def _check_content_stability(self) -> float:
        """检查内容是否已经稳定，返回相似度"""
        if not self.previous_response:
            return 0.0

        # 提取当前和前一轮的三元组
        current_triplets = self.confidence_triplets
        previous_triplets = ConfidenceTripletExtractor.extract_triplets(self.previous_response)

        # 计算相似度
        similarity = ConfidenceTripletExtractor.calculate_similarity(current_triplets, previous_triplets)
        print(f"内容稳定性检查: 相似度 {similarity:.2f}")

        return similarity

    def _create_early_termination_result(self) -> Dict[str, Any]:
        """创建提前终止的结果"""
        mode_descriptions = {
            "ai_simulation": "AI模拟推演",
            "expert_review": "专家审核",
            "worker_validation": "实证检验"
        }
        mode_desc = mode_descriptions.get(self.mode, "生产分析")

        # 直接使用当前结果作为最终结果
        self.final_triplets = self.confidence_triplets
        self.confidence_score = min(0.9, 0.7 + len(self.confidence_triplets["confident"]) * 0.05)
        self.critique_validity = 0.5

        return {
            "layer": self.layer_num,
            "mode": self.mode,
            "response": f"【思考提前终止】{mode_desc}内容已稳定，无需进一步迭代",
            "critique": f"【思考提前终止】{mode_desc}内容稳定性已达到阈值",
            "initial_triplets": self.confidence_triplets,
            "final_triplets": self.final_triplets,
            "confidence_score": self.confidence_score,
            "critique_validity": self.critique_validity,
            "should_terminate_early": True,
            "stability_similarity": self.stability_similarity
        }

    def _observer_evaluate(self) -> Dict[str, Any]:
        """观察者评估并生成最终置信度三元组"""

        mode_descriptions = {
            "ai_simulation": "AI模拟推演",
            "expert_review": "专家审核",
            "worker_validation": "实证检验"
        }
        mode_desc = mode_descriptions.get(self.mode, "生产分析")

        if self.mode == "ai_simulation":
            prompt = f"""你是一个生产模拟质量评估专家，请基于建构者推演和质疑者批判，生成最终的置信度分类。

生产环节: {self.question}

建构者AI模拟推演:
{self.response}

质疑者聚焦批判:
{self.critique}

【AI模拟推演评估要求】
请完成以下评估任务：

1. **逻辑合理性评估**：评估推演的逻辑严密性和生产实际符合度
2. **风险覆盖度评估**：评估风险识别的全面性和关键性
3. **假设质量评估**：评估推测假设的质量和依据充分性
4. **实用价值评估**：评估推演结果对生产实践的实际指导价值

请根据批判内容调整三元组分类：
- 对于质疑者指出但建构者未能有效捍卫的内容，应降级或移到未知
- 对于建构者成功捍卫且批判合理的内容，应保持或升级
- 确保最终三元组包含3-8个具体要点

【输出格式】
请严格按照JSON格式输出：
{{
    "final_triplets": {{
        "confident": ["确信内容1", "确信内容2", ...],
        "speculative": ["推测内容1", "推测内容2", ...], 
        "unknown": ["未知内容1", "未知内容2", ...]
    }},
    "confidence_score": 0.0-1.0之间的数值,
    "critique_validity": 0.0-1.0之间的数值
}}"""

        elif self.mode == "expert_review":
            prompt = f"""你是一个专家审核质量评估专家，请基于建构者审核和质疑者批判，生成最终的置信度分类。

原始问题: {self.question}

建构者专家审核:
{self.response}

质疑者聚焦批判:
{self.critique}

【专家审核评估要求】
请完成以下评估任务：

1. **经验准确性评估**：评估专家经验的准确性和数据支撑度
2. **方案可行性评估**：评估解决方案的实际可行性和成本效益
3. **风险评估质量**：评估风险分析和优先级排序的质量
4. **实用价值评估**：评估审核结果对生产改进的实际价值

请根据批判内容调整三元组分类：
- 对于质疑者指出但建构者未能有效捍卫的内容，应降级或移到未知
- 对于建构者成功捍卫且批判合理的内容，应保持或升级
- 确保最终三元组包含3-8个具体要点

【输出格式】
请严格按照JSON格式输出：
{{
    "final_triplets": {{
        "confident": ["确信内容1", "确信内容2", ...],
        "speculative": ["推测内容1", "推测内容2", ...], 
        "unknown": ["未知内容1", "未知内容2", ...]
    }},
    "confidence_score": 0.0-1.0之间的数值,
    "critique_validity": 0.0-1.0之间的数值
}}"""

        else:  # worker_validation
            prompt = f"""你是一个实证检验质量评估专家，请基于建构者规划和质疑者批判，生成最终的置信度分类。

待验证问题: {self.question}

建构者实证检验规划:
{self.response}

质疑者聚焦批判:
{self.critique}

【实证检验评估要求】
请完成以下评估任务：

1. **可操作性评估**：评估验证方案的操作便利性和实施难度
2. **成本效益评估**：评估验证方案的成本效益比和实际价值
3. **安全性评估**：评估验证过程的安全性和风险控制
4. **数据质量评估**：评估验证结果的数据质量和可靠性

请根据批判内容调整三元组分类：
- 对于质疑者指出但建构者未能有效捍卫的内容，应降级或移到未知
- 对于建构者成功捍卫且批判合理的内容，应保持或升级
- 确保最终三元组包含3-8个具体要点

【输出格式】
请严格按照JSON格式输出：
{{
    "final_triplets": {{
        "confident": ["确信内容1", "确信内容2", ...],
        "speculative": ["推测内容1", "推测内容2", ...], 
        "unknown": ["未知内容1", "未知内容2", ...]
    }},
    "confidence_score": 0.0-1.0之间的数值,
    "critique_validity": 0.0-1.0之间的数值
}}"""

        role_mapping = {
            "ai_simulation": "production_observer_simulation",
            "expert_review": "production_observer_expert",
            "worker_validation": "production_observer_worker"
        }
        role = role_mapping.get(self.mode, "production_observer_default")

        try:
            evaluation_text = call_qwen(prompt, role, temperature=0.1)

            # 尝试解析JSON
            json_match = re.search(r'\{.*\}', evaluation_text, re.DOTALL)
            if json_match:
                evaluation_json = json_match.group()
                evaluation = json.loads(evaluation_json)

                # 验证和清理三元组数据
                final_triplets = evaluation.get("final_triplets", {})
                for category in ["confident", "speculative", "unknown"]:
                    if category not in final_triplets:
                        final_triplets[category] = []
                    elif not isinstance(final_triplets[category], list):
                        final_triplets[category] = []

                    # 清理每个项目
                    cleaned_items = []
                    for item in final_triplets[category]:
                        if isinstance(item, str) and item.strip():
                            cleaned_items.append(item.strip())
                    final_triplets[category] = cleaned_items[:8]  # 限制每个类别最多8个

                # 验证分数范围
                confidence_score = float(evaluation.get("confidence_score", 0.5))
                confidence_score = max(0.0, min(1.0, confidence_score))

                critique_validity = float(evaluation.get("critique_validity", 0.3))
                critique_validity = max(0.0, min(1.0, critique_validity))

                return {
                    "final_triplets": final_triplets,
                    "confidence_score": confidence_score,
                    "critique_validity": critique_validity
                }
            else:
                print(f"观察者评估未返回有效JSON: {evaluation_text[:200]}")
        except Exception as e:
            print(f"观察者评估解析失败: {e}")
            print(f"原始响应: {evaluation_text[:500]}")

        # 如果解析失败，使用启发式评估
        return self._heuristic_evaluation()

    def _heuristic_evaluation(self) -> Dict[str, Any]:
        """启发式评估"""
        # 基于初始三元组和批判质量进行启发式评估
        confident_count = len(self.confidence_triplets["confident"])
        speculative_count = len(self.confidence_triplets["speculative"])
        unknown_count = len(self.confidence_triplets["unknown"])

        total_items = confident_count + speculative_count + unknown_count
        if total_items == 0:
            confidence_score = 0.1
        else:
            # 确信内容越多，置信度越高；未知内容越多，置信度越低
            confidence_score = (confident_count * 1.0 + speculative_count * 0.5 + unknown_count * 0.1) / total_items

        # 基于批判内容的质量调整
        critique_indicators = []
        if self.mode == "ai_simulation":
            critique_indicators = ["逻辑", "风险", "假设", "验证", "遗漏", "合理", "实际", "理论"]
        elif self.mode == "expert_review":
            critique_indicators = ["经验", "方案", "优先", "风险", "可行", "依据", "数据", "成本"]
        else:  # worker_validation
            critique_indicators = ["操作", "成本", "安全", "数据", "便利", "质量", "时效", "节拍"]

        critique_strength = sum(1 for indicator in critique_indicators if indicator in self.critique)
        critique_validity = min(0.9, critique_strength * 0.12 + 0.3)  # 基础值0.3，每个关键词加0.12

        # 根据三元组质量微调置信度
        if confident_count >= 3:
            confidence_score = min(0.9, confidence_score + 0.1)
        if unknown_count > 5:
            confidence_score = max(0.3, confidence_score - 0.1)

        return {
            "final_triplets": self.confidence_triplets,
            "confidence_score": min(0.95, max(0.1, confidence_score)),
            "critique_validity": critique_validity
        }


# ===================== 生产思考单元核心组件 =====================
class ProductionThinkingUnit:
    """生产思考单元：包含3层完整思考的饱和对抗单元"""

    def __init__(self, unit_num: int, question: str, mode: str,
                 previous_final_response: str = "", previous_final_critique: str = ""):
        self.unit_num = unit_num
        self.question = question
        self.mode = mode
        self.previous_final_response = previous_final_response
        self.previous_final_critique = previous_final_critique
        self.layers: List[ProductionThinkingLayer] = []
        self.final_response = ""
        self.final_critique = ""
        self.final_triplets = {"confident": [], "speculative": [], "unknown": []}
        self.final_confidence = 0.0
        self.layer_history: List[Dict] = []
        self.early_terminated = False
        self.stability_threshold = 0.65  # 内容稳定性阈值

    def execute(self) -> Dict[str, Any]:
        """执行单元思考流程（最多3层饱和对抗）"""
        mode_descriptions = {
            "ai_simulation": "AI模拟推演",
            "expert_review": "专家审核修正",
            "worker_validation": "工人实证检验"
        }
        mode_desc = mode_descriptions.get(self.mode, "生产分析")

        print(f"\n{'=' * 60}")
        print(f"启动{mode_desc}思考单元 {self.unit_num}")
        print(f"{'=' * 60}")

        current_response = self.previous_final_response
        current_critique = self.previous_final_critique

        # 执行最多3层思考，支持提前终止
        for layer_num in range(1, 4):
            layer = ProductionThinkingLayer(layer_num, self.question, self.mode,
                                            current_response, current_critique)
            layer_result = layer.execute()

            self.layers.append(layer)
            self.layer_history.append(layer_result)

            # 检查是否应该提前终止
            if layer_result.get("should_terminate_early", False):
                print(f"🛑 在第{layer_num}层提前终止思考 (相似度: {layer_result.get('stability_similarity', 0):.2f})")
                self.early_terminated = True
                break

            # 更新当前层的结果，传递给下一层
            current_response = layer.response
            current_critique = layer.critique

            # 记录层间进展
            print(f"单元{self.unit_num}-层{layer_num}: 置信度{layer.confidence_score:.2f} -> ", end="")
            if layer_num < 3 and not self.early_terminated:
                print("进入下一层")
            else:
                print("单元完成")
                break

        # 单元最终结果（使用最后一层的结果）
        if self.layers:
            last_layer = self.layers[-1]
            self.final_response = last_layer.response
            self.final_critique = last_layer.critique
            self.final_triplets = last_layer.final_triplets
            self.final_confidence = last_layer.confidence_score

        return {
            "unit": self.unit_num,
            "mode": self.mode,
            "final_response": self.final_response,
            "final_critique": self.final_critique,
            "final_triplets": self.final_triplets,
            "final_confidence": self.final_confidence,
            "layer_history": self.layer_history,
            "early_terminated": self.early_terminated,
            "actual_layers": len(self.layers)
        }


# ===================== 领域智能体 =====================
class DomainAgent:
    """领域智能体基类"""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.results = None

    def process(self, question: str, max_units: int = 2) -> Dict[str, Any]:
        """处理问题 - 子类需要实现"""
        raise NotImplementedError


class AISimulationAgent(DomainAgent):
    """AI模拟智能体 - 负责问题推演"""

    def __init__(self):
        super().__init__("AI模拟智能体", "ai_simulation")

    def process(self, question: str, max_units: int = 2) -> Dict[str, Any]:
        """执行AI模拟推演"""
        print(f"\n{'=' * 80}")
        print(f"启动AI模拟智能体")
        print(f"分析环节: {question}")
        print(f"{'=' * 80}")

        # 加载FMEA框架
        production_framework.load_framework_for_mode("ai_simulation")

        current_response = ""
        current_critique = ""
        unit_results = []

        for unit_num in range(1, max_units + 1):
            print(f"\n>>> 启动AI模拟单元 {unit_num}/{max_units}")

            unit = ProductionThinkingUnit(unit_num, question, "ai_simulation",
                                          current_response, current_critique)
            unit_result = unit.execute()
            unit_results.append(unit_result)

            current_response = unit_result["final_response"]
            current_critique = unit_result["final_critique"]

            print(f"\nAI模拟单元{unit_num}完成: 置信度{unit_result['final_confidence']:.2f}")

            # 终止条件：置信度足够高或达到最大单元数
            if unit_result["final_confidence"] >= 0.75 or unit_num >= max_units:
                print(f"\n>>> AI模拟终止于单元 {unit_num}")
                break

        # 选择最佳结果
        best_unit_index = max(range(len(unit_results)),
                              key=lambda i: unit_results[i]["final_confidence"])
        best_result = unit_results[best_unit_index]

        # 格式化输出
        formatted_triplets = ConfidenceTripletExtractor.format_triplets(best_result["final_triplets"])

        self.results = {
            "agent": self.name,
            "role": self.role,
            "question": question,
            "best_result": best_result,
            "all_results": unit_results,
            "framework_used": "FMEA框架",
            "formatted_output": formatted_triplets
        }

        print(f"\n✅ AI模拟智能体完成")
        print(f"最终置信度: {best_result['final_confidence']:.2f}")

        return self.results


class ExpertAgent(DomainAgent):
    """专家智能体 - 负责审核修正"""

    def __init__(self):
        super().__init__("专家智能体", "expert_review")

    def process(self, simulation_results: Dict[str, Any], max_units: int = 2) -> Dict[str, Any]:
        """基于AI模拟结果进行专家审核"""
        if not simulation_results:
            print("❌ 请先运行AI模拟智能体")
            return {"error": "需要AI模拟结果作为输入"}

        # 提取AI模拟的总结
        ai_summary = self._extract_ai_summary(simulation_results)

        print(f"\n{'=' * 80}")
        print(f"启动专家智能体")
        print(f"审核AI模拟结果")
        print(f"{'=' * 80}")

        # 加载专家经验规则框架
        production_framework.load_framework_for_mode("expert_review")

        current_response = ""
        current_critique = ""
        unit_results = []

        for unit_num in range(1, max_units + 1):
            print(f"\n>>> 启动专家审核单元 {unit_num}/{max_units}")

            unit = ProductionThinkingUnit(unit_num, ai_summary, "expert_review",
                                          current_response, current_critique)
            unit_result = unit.execute()
            unit_results.append(unit_result)

            current_response = unit_result["final_response"]
            current_critique = unit_result["final_critique"]

            print(f"\n专家审核单元{unit_num}完成: 置信度{unit_result['final_confidence']:.2f}")

            # 终止条件
            if unit_result["final_confidence"] >= 0.75 or unit_num >= max_units:
                print(f"\n>>> 专家审核终止于单元 {unit_num}")
                break

        # 选择最佳结果
        best_unit_index = max(range(len(unit_results)),
                              key=lambda i: unit_results[i]["final_confidence"])
        best_result = unit_results[best_unit_index]

        # 生成对比分析
        comparison = self._compare_with_ai(simulation_results["best_result"], best_result)

        # 格式化输出
        formatted_triplets = ConfidenceTripletExtractor.format_triplets(best_result["final_triplets"])

        self.results = {
            "agent": self.name,
            "role": self.role,
            "ai_input": ai_summary,
            "best_result": best_result,
            "all_results": unit_results,
            "framework_used": "专家经验规则",
            "comparison_with_ai": comparison,
            "formatted_output": formatted_triplets
        }

        print(f"\n✅ 专家智能体完成")
        print(f"最终置信度: {best_result['final_confidence']:.2f}")

        return self.results

    def _extract_ai_summary(self, simulation_results: Dict[str, Any]) -> str:
        """从AI模拟结果中提取总结"""
        best_result = simulation_results.get("best_result", {})
        triplets = best_result.get("final_triplets", {})

        summary = "AI模拟推演结果总结：\n"
        summary += f"置信度: {best_result.get('final_confidence', 0):.2f}\n\n"

        # 添加三元组内容
        if triplets.get("confident"):
            summary += "确信的问题：\n"
            for idx, item in enumerate(triplets["confident"][:5], 1):
                summary += f"{idx}. {item}\n"

        if triplets.get("speculative"):
            summary += "\n推测的问题：\n"
            for idx, item in enumerate(triplets["speculative"][:3], 1):
                summary += f"{idx}. {item}\n"

        if triplets.get("unknown"):
            summary += "\n未知/待验证的问题：\n"
            for idx, item in enumerate(triplets["unknown"][:2], 1):
                summary += f"{idx}. {item}\n"

        return summary

    def _compare_with_ai(self, ai_result: Dict, expert_result: Dict) -> Dict[str, Any]:
        """比较AI和专家结果的差异"""
        ai_triplets = ai_result.get("final_triplets", {})
        expert_triplets = expert_result.get("final_triplets", {})

        comparison = {
            "confidence_change": expert_result.get("final_confidence", 0) - ai_result.get("final_confidence", 0),
            "confident_items_added": [],
            "confident_items_removed": [],
            "speculative_items_changed": []
        }

        # 对比确信内容
        ai_confident_set = set(ai_triplets.get("confident", []))
        expert_confident_set = set(expert_triplets.get("confident", []))

        comparison["confident_items_added"] = list(expert_confident_set - ai_confident_set)[:3]
        comparison["confident_items_removed"] = list(ai_confident_set - expert_confident_set)[:3]

        # 对比推测内容
        ai_speculative_set = set(ai_triplets.get("speculative", []))
        expert_speculative_set = set(expert_triplets.get("speculative", []))

        # 找出从推测变为确信的内容
        speculative_to_confident = expert_confident_set.intersection(ai_speculative_set)
        if speculative_to_confident:
            comparison["speculative_items_changed"] = list(speculative_to_confident)[:2]

        return comparison


class WorkerAgent(DomainAgent):
    """工人智能体 - 负责实证检验"""

    def __init__(self):
        super().__init__("工人智能体", "worker_validation")

    def process(self, expert_results: Dict[str, Any], max_units: int = 2) -> Dict[str, Any]:
        """基于专家审核结果进行实证检验规划"""
        if not expert_results:
            print("❌ 请先运行专家智能体")
            return {"error": "需要专家审核结果作为输入"}

        # 提取专家审核的关键问题
        expert_summary = self._extract_expert_summary(expert_results)

        print(f"\n{'=' * 80}")
        print(f"启动工人智能体")
        print(f"规划实证检验方案")
        print(f"{'=' * 80}")

        # 加载质量门控框架
        production_framework.load_framework_for_mode("worker_validation")

        current_response = ""
        current_critique = ""
        unit_results = []

        for unit_num in range(1, max_units + 1):
            print(f"\n>>> 启动实证检验单元 {unit_num}/{max_units}")

            unit = ProductionThinkingUnit(unit_num, expert_summary, "worker_validation",
                                          current_response, current_critique)
            unit_result = unit.execute()
            unit_results.append(unit_result)

            current_response = unit_result["final_response"]
            current_critique = unit_result["final_critique"]

            print(f"\n实证检验单元{unit_num}完成: 置信度{unit_result['final_confidence']:.2f}")

            # 终止条件
            if unit_result["final_confidence"] >= 0.75 or unit_num >= max_units:
                print(f"\n>>> 实证检验终止于单元 {unit_num}")
                break

        # 选择最佳结果
        best_unit_index = max(range(len(unit_results)),
                              key=lambda i: unit_results[i]["final_confidence"])
        best_result = unit_results[best_unit_index]

        # 生成可执行的验证计划
        validation_plan = self._generate_validation_plan(best_result)

        # 格式化输出
        formatted_triplets = ConfidenceTripletExtractor.format_triplets(best_result["final_triplets"])

        self.results = {
            "agent": self.name,
            "role": self.role,
            "expert_input": expert_summary,
            "best_result": best_result,
            "all_results": unit_results,
            "framework_used": "质量门控标准",
            "validation_plan": validation_plan,
            "formatted_output": formatted_triplets
        }

        print(f"\n✅ 工人智能体完成")
        print(f"最终置信度: {best_result['final_confidence']:.2f}")

        return self.results

    def _extract_expert_summary(self, expert_results: Dict[str, Any]) -> str:
        """从专家结果中提取关键问题"""
        best_result = expert_results.get("best_result", {})
        triplets = best_result.get("final_triplets", {})

        summary = "专家审核的关键问题：\n"
        summary += f"置信度: {best_result.get('final_confidence', 0):.2f}\n\n"

        # 重点关注确信的问题
        if triplets.get("confident"):
            summary += "需要实证检验的关键问题：\n"
            for idx, item in enumerate(triplets["confident"][:5], 1):
                summary += f"{idx}. {item}\n"

        summary += "\n请规划针对这些问题的实证检验方案："
        return summary

    def _generate_validation_plan(self, worker_result: Dict) -> List[Dict[str, Any]]:
        """生成结构化的验证计划 - 优化版本"""
        triplets = worker_result.get("final_triplets", {})
        plan = []

        # 从确信内容中提取可验证的项目
        for idx, item in enumerate(triplets.get("confident", []), 1):
            if idx > 8:  # 最多生成8个验证计划
                break

            validation_method = self._suggest_method(item)
            required_tools = self._suggest_tools(item)

            # 根据问题内容确定优先级
            if any(keyword in item for keyword in ["关键", "严重", "紧急", "危险", "安全"]):
                priority = "高"
            elif any(keyword in item for keyword in ["重要", "主要", "核心"]):
                priority = "中"
            else:
                priority = "低"

            # 估计验证时间
            if any(keyword in item.lower() for keyword in ["简单", "快速", "目视", "检查"]):
                estimated_time = "15-30分钟"
            elif any(keyword in item.lower() for keyword in ["复杂", "测试", "测量", "分析"]):
                estimated_time = "1-2小时"
            else:
                estimated_time = "30-60分钟"

            plan.append({
                "id": f"V{idx:03d}",
                "description": item,
                "validation_method": validation_method,
                "required_tools": required_tools,
                "estimated_time": estimated_time,
                "priority": priority,
                "confidence": "高"  # 确信内容
            })

        # 从推测内容中提取需要验证的项目（优先级较低）
        spec_start_idx = len(plan) + 1
        for idx, item in enumerate(triplets.get("speculative", []), spec_start_idx):
            if idx > 12:  # 总共最多12个验证计划
                break

            plan.append({
                "id": f"V{idx:03d}",
                "description": item,
                "validation_method": self._suggest_method(item),
                "required_tools": self._suggest_tools(item),
                "estimated_time": "1-3小时",
                "priority": "中",
                "confidence": "中"
            })

        return plan

    def _suggest_method(self, item: str) -> str:
        """根据问题描述建议验证方法 - 优化版本"""
        item_lower = item.lower()

        if any(keyword in item_lower for keyword in ["扭矩", "力矩", "拧紧"]):
            return "使用数显扭力扳手或扭力测试仪进行抽样检测，对比标准值"
        elif any(keyword in item_lower for keyword in ["尺寸", "公差", "间隙", "距离"]):
            return "使用卡尺、千分尺、塞尺或三坐标测量仪进行实际测量"
        elif any(keyword in item_lower for keyword in ["振动", "噪声", "声音", "异响"]):
            return "使用振动仪、分贝计或声学相机现场检测，对比基准值"
        elif any(keyword in item_lower for keyword in ["温度", "发热", "冷却", "温升"]):
            return "使用红外测温仪或热电偶监测温度变化，记录温升曲线"
        elif any(keyword in item_lower for keyword in ["压力", "流量", "泄漏", "漏气", "漏水"]):
            return "使用压力表、流量计进行测试，或进行气密性/水密性试验"
        elif any(keyword in item_lower for keyword in ["电压", "电流", "电阻", "电路"]):
            return "使用万用表、示波器或电路测试仪进行电气参数检测"
        elif any(keyword in item_lower for keyword in ["外观", "划伤", "锈蚀", "污渍"]):
            return "目视检查配合放大镜或显微镜，按标准样件对比"
        elif any(keyword in item_lower for keyword in ["装配", "配合", "安装", "连接"]):
            return "功能测试配合检具检查，验证装配完整性和功能正常性"
        elif any(keyword in item_lower for keyword in ["材料", "硬度", "强度", "材质"]):
            return "取样送实验室进行材料性能测试，或使用便携式硬度计"
        elif any(keyword in item_lower for keyword in ["软件", "程序", "代码", "逻辑"]):
            return "进行功能测试、边界测试和异常测试，验证软件逻辑"
        else:
            return "目视检查与功能测试相结合，按检验标准进行验证"

    def _suggest_tools(self, item: str) -> List[str]:
        """根据问题描述建议所需工具 - 优化版本"""
        item_lower = item.lower()
        tools = ["检查表", "记录表", "签字笔"]

        if any(keyword in item_lower for keyword in ["扭矩", "力矩"]):
            tools.extend(["数显扭力扳手", "扭力测试仪", "校准证书"])
        elif any(keyword in item_lower for keyword in ["尺寸", "公差"]):
            tools.extend(["卡尺", "千分尺", "塞尺", "高度规", "三坐标测量仪"])
        elif any(keyword in item_lower for keyword in ["振动", "噪声"]):
            tools.extend(["振动仪", "分贝计", "声学相机", "数据分析软件"])
        elif any(keyword in item_lower for keyword in ["温度", "发热"]):
            tools.extend(["红外测温仪", "热电偶", "温度记录仪"])
        elif any(keyword in item_lower for keyword in ["压力", "泄漏"]):
            tools.extend(["压力表", "流量计", "检漏液", "气密性测试仪"])
        elif any(keyword in item_lower for keyword in ["电气", "电路"]):
            tools.extend(["万用表", "示波器", "绝缘测试仪", "电路测试仪"])
        elif any(keyword in item_lower for keyword in ["外观", "表面"]):
            tools.extend(["放大镜", "显微镜", "标准样件", "光源箱"])
        elif any(keyword in item_lower for keyword in ["材料", "硬度"]):
            tools.extend(["便携式硬度计", "取样工具", "实验室测试设备"])
        elif any(keyword in item_lower for keyword in ["软件", "程序"]):
            tools.extend(["测试软件", "调试工具", "日志分析工具"])

        # 添加通用工具
        tools.extend(["安全防护用品", "照明设备", "通讯工具"])

        return list(dict.fromkeys(tools))  # 去重


# ===================== 生产模拟协调引擎 =====================
class ProductionSimulationEngine:
    """生产模拟协调引擎 - 协调三个领域智能体的工作流程"""

    def __init__(self):
        self.ai_agent = AISimulationAgent()
        self.expert_agent = ExpertAgent()
        self.worker_agent = WorkerAgent()
        self.results_history = []

    def run_full_workflow(self, production_step: str, max_units_per_agent: int = 2) -> Dict[str, Any]:
        """执行完整的工作流程：AI模拟 → 专家审核 → 工人检验"""
        print(f"\n{'=' * 100}")
        print(f"开始生产模拟增强完整工作流程")
        print(f"分析环节: {production_step}")
        print(f"{'=' * 100}")

        # 阶段1: AI模拟推演
        print(f"\n📊 阶段1: AI模拟推演")
        ai_results = self.ai_agent.process(production_step, max_units_per_agent)
        self.results_history.append({"stage": "ai_simulation", "results": ai_results})

        # 阶段2: 专家审核修正
        print(f"\n🔍 阶段2: 专家审核修正")
        expert_results = self.expert_agent.process(ai_results, max_units_per_agent)
        self.results_history.append({"stage": "expert_review", "results": expert_results})

        # 阶段3: 工人实证检验规划
        print(f"\n🔧 阶段3: 实证检验规划")
        worker_results = self.worker_agent.process(expert_results, max_units_per_agent)
        self.results_history.append({"stage": "worker_validation", "results": worker_results})

        # 生成最终报告
        final_report = self._generate_final_report(ai_results, expert_results, worker_results)

        print(f"\n{'=' * 100}")
        print(f"🎉 生产模拟增强工作流程完成!")
        print(f"{'=' * 100}")

        return {
            "production_step": production_step,
            "ai_results": ai_results,
            "expert_results": expert_results,
            "worker_results": worker_results,
            "final_report": final_report,
            "results_history": self.results_history
        }

    def _generate_final_report(self, ai_results: Dict, expert_results: Dict, worker_results: Dict) -> str:
        """生成最终的综合报告"""
        report = f"""
# 生产模拟增强分析报告

## 分析对象
**生产环节**: {ai_results.get('question', '未知环节')}
**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 阶段一: AI模拟推演
**执行智能体**: {ai_results.get('agent', 'AI模拟智能体')}
**使用框架**: {ai_results.get('framework_used', 'FMEA框架')}
**最终置信度**: {ai_results['best_result']['final_confidence']:.2f}
**思考层数**: {ai_results['best_result'].get('actual_layers', '未知')}

**关键推演结果**:
{ai_results.get('formatted_output', '无输出')}

## 阶段二: 专家审核修正  
**执行智能体**: {expert_results.get('agent', '专家智能体')}
**使用框架**: {expert_results.get('framework_used', '专家经验规则')}
**最终置信度**: {expert_results['best_result']['final_confidence']:.2f}
**思考层数**: {expert_results['best_result'].get('actual_layers', '未知')}

**专家修正结果**:
{expert_results.get('formatted_output', '无输出')}

**与AI模拟的主要差异**:
"""

        # 添加对比信息
        comparison = expert_results.get('comparison_with_ai', {})
        if comparison.get('confident_items_added'):
            report += "\n专家新增确信问题:\n"
            for idx, item in enumerate(comparison['confident_items_added'][:3], 1):
                report += f"{idx}. {item}\n"

        if comparison.get('confident_items_removed'):
            report += "\n专家排除的AI问题:\n"
            for idx, item in enumerate(comparison['confident_items_removed'][:3], 1):
                report += f"{idx}. {item}\n"

        if comparison.get('speculative_items_changed'):
            report += "\n从推测变为确信的问题:\n"
            for idx, item in enumerate(comparison['speculative_items_changed'][:2], 1):
                report += f"{idx}. {item}\n"

        report += f"""

## 阶段三: 实证检验规划
**执行智能体**: {worker_results.get('agent', '工人智能体')}
**使用框架**: {worker_results.get('framework_used', '质量门控标准')}
**最终置信度**: {worker_results['best_result']['final_confidence']:.2f}
**思考层数**: {worker_results['best_result'].get('actual_layers', '未知')}

**实证检验规划**:
{worker_results.get('formatted_output', '无输出')}

## 可执行的验证计划
"""

        # 添加验证计划
        validation_plan = worker_results.get('validation_plan', [])
        if validation_plan:
            # 按优先级排序
            high_priority = [item for item in validation_plan if item.get('priority') == '高']
            medium_priority = [item for item in validation_plan if item.get('priority') == '中']
            low_priority = [item for item in validation_plan if item.get('priority') == '低']

            sorted_plan = high_priority + medium_priority + low_priority

            for item in sorted_plan[:10]:  # 最多显示10个
                report += f"\n**{item['id']}** (优先级: {item['priority']}, 置信度: {item.get('confidence', '未知')})\n"
                report += f"**问题描述**: {item['description']}\n"
                report += f"**验证方法**: {item['validation_method']}\n"
                report += f"**所需工具**: {', '.join(item['required_tools'][:5])}\n"
                report += f"**预计时间**: {item['estimated_time']}\n"
        else:
            report += "\n暂无验证计划\n"

        report += f"""

## 整体评估
- **AI模拟置信度**: {ai_results['best_result']['final_confidence']:.2f}
- **专家审核置信度**: {expert_results['best_result']['final_confidence']:.2f} 
- **实证规划置信度**: {worker_results['best_result']['final_confidence']:.2f}
- **平均置信度**: {(ai_results['best_result']['final_confidence'] + expert_results['best_result']['final_confidence'] + worker_results['best_result']['final_confidence']) / 3:.2f}

## 知识积累建议
1. **验证执行**: 按照验证计划进行实际生产观察和测试
2. **数据记录**: 详细记录实际发现的问题与假设的差异
3. **知识更新**: 将验证结果反馈到生产知识库，优化认知框架
4. **流程优化**: 基于验证结果更新生产流程和检验标准
5. **持续改进**: 建立定期回顾和更新机制，形成PDCA循环

## 下一步行动
1. 立即执行高优先级的验证计划（V001-V003）
2. 1周内完成中等优先级验证
3. 1月内建立知识反馈机制
4. 季度性回顾和优化生产流程

---
**报告生成系统**: 生产模拟增强引擎 v1.1
**系统特点**: 基于RAMTN架构的三智能体协作系统
**技术架构**: 一个核心引擎 + 多个领域智能体按序引导
"""

        return report


# ===================== 大模型调用 =====================
def call_qwen(prompt: str, role: str = "default", temperature: float = 0.3) -> str:
    """调用qwen API - 支持生产领域角色"""
    system_messages = {
        # AI模拟相关角色
        "production_simulator": """你是一个生产模拟AI，专门推演生产过程中可能的问题。你的核心能力是：
1. 基于FMEA框架识别潜在失效模式
2. 结合工艺流程分析推演问题发生逻辑
3. 参考历史问题库识别类似模式
4. 生成带置信度分级的问题假设，避免过度推断
5. 输出格式规范，严格按照"确信/推测/未知"三类组织内容""",

        "production_critic_simulation": """你是一个严格的生产模拟审查者，专注于发现AI模拟推演中的问题。你的批判：
1. 检查推演逻辑的合理性和严密性
2. 评估风险识别的全面性和准确性
3. 验证问题假设的可观测性和可验证性
4. 确保推演结果对生产实践具有实际价值
5. 提出具体可操作的改进建议""",

        "production_observer_simulation": """你是一个生产模拟质量评估专家，擅长：
1. 评估AI模拟推演的逻辑严密性
2. 判断风险识别的全面性和准确性
3. 验证问题假设的质量和依据
4. 衡量推演结果对生产实践的价值
5. 输出规范的JSON评估结果""",

        # 专家审核相关角色
        "production_expert": """你是一个经验丰富的生产专家，拥有多年的现场经验和专业知识。你的核心能力是：
1. 基于实际经验审核AI模拟的合理性
2. 补充AI忽略的关键风险点和解决方案
3. 提供问题优先级排序和实际发生概率评估
4. 给出具体可行的改进建议和预防措施
5. 输出格式规范，包含实际数据和案例""",

        "production_critic_expert": """你是一个严格的专家审核审查者，专注于发现专家审核中的问题。你的批判：
1. 检查专家经验的准确性和可靠性
2. 评估解决方案的实际可行性
3. 验证风险概率评估的依据是否充分
4. 确保审核结果具有实际的指导价值
5. 提出具体可操作的改进建议""",

        "production_observer_expert": """你是一个专家审核质量评估专家，擅长：
1. 评估专家经验的准确性和可靠性
2. 判断解决方案的实际可行性
3. 验证风险分析和优先级排序的质量
4. 衡量审核结果对生产改进的实际价值
5. 输出规范的JSON评估结果""",

        # 工人检验相关角色
        "production_worker": """你是一个一线生产工人，熟悉现场操作和设备使用。你的核心能力是：
1. 评估问题假设在实际生产中的可观测性
2. 设计简单有效的验证方案和检查表
3. 考虑验证过程的安全性、成本和便利性
4. 提供实际可行的数据记录和反馈方法
5. 输出格式规范，包含具体验证步骤""",

        "production_critic_worker": """你是一个严格的实证检验审查者，专注于发现验证方案中的问题。你的批判：
1. 检查验证方案的操作便利性和安全性
2. 评估验证成本和时间是否合理
3. 验证数据记录方法的有效性
4. 确保验证方案能够获得可靠的结论
5. 提出具体可操作的改进建议""",

        "production_observer_worker": """你是一个实证检验质量评估专家，擅长：
1. 评估验证方案的操作便利性和安全性
2. 判断验证成本和时间是否合理
3. 验证数据记录和反馈方法的质量
4. 衡量验证方案对问题解决的贡献度
5. 输出规范的JSON评估结果""",

        "default": "你是一个有帮助的AI助手。"
    }

    system_content = system_messages.get(role, system_messages["default"])

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": prompt},
    ]

    try:
        print(f"调用API - {role}: {prompt[:80]}...")

        response = Generation.call(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            model="qwen-plus",
            messages=messages,
            result_format="message",
            temperature=temperature,
        )

        if response.status_code == 200:
            content = response.output.choices[0].message.content
            print(f"API响应 - {role}: {content[:80]}...")
            return content
        else:
            raise Exception(f"API调用失败: {response.message}")

    except Exception as e:
        print(f"API调用异常 - {role}: {str(e)}")
        # 返回模拟响应用于测试
        if "simulator" in role:
            return """【我确信的】
1. 铰链安装扭矩不达标将直接导致车门装配松动或异响，FMEA严重度S≥8，属关键控制点。
2. 密封条未完全卡入槽位必然导致漏水与风噪问题，终检必须覆盖此项检查。
3. 电子线路连接器虚接会引起功能失效，必须进行导通测试验证。

【我推测的】
1. 冬季低温可能使密封条材料变脆，增加装配断裂风险，建议控制环境温度。
2. 扭矩工具长期使用可能出现轴承磨损，导致输出力矩衰减，建议定期校准。
3. 门板预装工装磨损可能导致定位精度下降，建议增加工装点检频次。

【我不知道的】
1. 视觉检测系统对微小缺陷的检出率受光照条件影响程度未知，需要实测验证。
2. 不同操作人员对装配质量的个体差异量化数据缺失，需要统计分析。
3. 产线节拍变化对装配质量的具体影响机制需要进一步研究。"""
        elif "expert" in role and "critic" not in role:
            return """【我确信的】
1. 铰链扭矩问题在多款车型中均有发生，A/B工厂PPM达480-520，必须作为关键特性管控。
2. 密封条装配漏检率达12%，单台维修成本超800元，需实施操作者自检+检验员专检双机制。
3. 扭矩工具未校准已引发3起批量返修，故障溯源报告证实因果链，必须纳入预防性维护。

【我推测的】
1. 轴承间隙＞0.2mm可能与角度偏差相关，但对力矩衰减的影响需台架测试验证。
2. 低温环境下密封条断裂率可能上升，但加热方案的成本效益需进一步评估。
3. 批次硬度差异在自动化线上更敏感，但系统性风险证据不足，建议协同评估。

【我不知道的】
1. 轴承间隙与力矩衰减的非线性关系需要建立量化模型，缺乏实验数据。
2. 密封条硬度与装配力的具体函数关系未知，需要DOE实验确定。
3. 人员培训效果对质量改善的长期影响需要跟踪研究。"""
        else:
            return "API调用失败，返回模拟响应"


# ===================== 测试示例 =====================
if __name__ == "__main__":
    try:
        if not os.getenv("DASHSCOPE_API_KEY"):
            print("⚠️  警告：未设置DASHSCOPE_API_KEY环境变量，将使用模拟响应")
            print("如需使用真实API，请设置环境变量: export DASHSCOPE_API_KEY=your_key")

        print("开始生产模拟增强系统测试...")

        # 创建生产模拟引擎
        simulator = ProductionSimulationEngine()

        # 定义汽车生产线的三个关键环节
        production_steps = [
            "汽车车门装配环节：包括门板预装、铰链安装、密封条装配、电子线路连接、最终调试等步骤",
            "汽车发动机缸体机加工环节：包括粗加工、精加工、孔加工、清洗、检测等步骤",
            "汽车总装线内饰安装环节：包括仪表盘安装、座椅安装、线束布置、多媒体系统安装等步骤"
        ]

        # 测试第一个环节
        test_step = production_steps[0]

        print(f"\n选择测试环节: {test_step}")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 运行完整工作流程
        results = simulator.run_full_workflow(test_step, max_units_per_agent=2)

        # 输出最终报告
        print("\n" + "=" * 100)
        print("最终报告摘要:")
        print("=" * 100)
        print(results["final_report"])

        # 保存结果到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"production_simulation_report_{timestamp}.txt"

        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(results["final_report"])

        print(f"\n✅ 报告已保存到文件: {report_filename}")

        # 保存详细结果到JSON文件
        json_filename = f"production_simulation_results_{timestamp}.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump({
                "production_step": test_step,
                "timestamp": timestamp,
                "ai_confidence": results["ai_results"]["best_result"]["final_confidence"],
                "expert_confidence": results["expert_results"]["best_result"]["final_confidence"],
                "worker_confidence": results["worker_results"]["best_result"]["final_confidence"],
                "summary": "生产模拟增强分析完成"
            }, f, ensure_ascii=False, indent=2)

        print(f"✅ 结果摘要已保存到文件: {json_filename}")

    except Exception as e:
        print(f"程序执行失败: {e}")
        import traceback

        traceback.print_exc()