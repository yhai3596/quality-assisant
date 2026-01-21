#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5W1H问题追问引导器
系统性引导用户进行深度问题挖掘，找到根本原因
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class QuestionContext:
    """问题上下文"""
    question_id: str
    question_text: str
    category: str
    purpose: str
    follow_up_questions: List[str]
    expected_answer_type: str
    validation_criteria: List[str]

@dataclass
class UserResponse:
    """用户回答"""
    question_id: str
    answer_text: str
    answer_details: List[str]
    confidence_level: str
    supporting_evidence: List[str]
    timestamp: str

class FiveWInterviewer:
    """5W1H问题追问引导器"""

    def __init__(self):
        self.conversation_history = []
        self.question_templates = self._load_question_templates()
        self.current_phase = "initial"
        self.questions_asked = []
        self.responses = {}

    def _load_question_templates(self) -> Dict:
        """加载问题模板"""
        return {
            "initial": {
                "description": "初始问题定义阶段",
                "questions": [
                    {
                        "id": "what_problem",
                        "question": "请详细描述您遇到的具体问题是什么？",
                        "category": "问题定义",
                        "purpose": "明确问题的具体表现",
                        "follow_up": [
                            "这个问题是什么时候第一次出现的？",
                            "问题的具体表现有哪些？",
                            "受影响的产品或系统有哪些？"
                        ],
                        "answer_type": "详细描述",
                        "validation": ["是否具体", "是否可测量", "是否可验证"]
                    },
                    {
                        "id": "when_problem",
                        "question": "这个问题是什么时候发生的？",
                        "category": "时间维度",
                        "purpose": "确定问题发生的时间范围",
                        "follow_up": [
                            "是突然发生的还是逐渐出现的？",
                            "在什么情况下最容易发生？",
                            "有周期性或规律性吗？"
                        ],
                        "answer_type": "时间描述",
                        "validation": ["时间是否准确", "是否有具体时间点"]
                    },
                    {
                        "id": "where_problem",
                        "question": "这个问题在哪些地方或哪些环节出现？",
                        "category": "位置维度",
                        "purpose": "确定问题的发生位置",
                        "follow_up": [
                            "是所有地点都有还是特定地点？",
                            "在生产流程的哪个环节？",
                            "涉及哪些人员或设备？"
                        ],
                        "answer_type": "位置描述",
                        "validation": ["位置是否具体", "是否可定位"]
                    },
                    {
                        "id": "who_involved",
                        "question": "涉及哪些人员、供应商或合作伙伴？",
                        "category": "人员维度",
                        "purpose": "确定问题的相关人员",
                        "follow_up": [
                            "哪些人员直接参与了相关活动？",
                            "是否有外部供应商参与？",
                            "责任分工是怎样的？"
                        ],
                        "answer_type": "人员列表",
                        "validation": ["是否完整", "是否准确"]
                    },
                    {
                        "id": "how_severe",
                        "question": "问题的严重程度如何？影响范围有多大？",
                        "category": "影响评估",
                        "purpose": "评估问题的严重性和影响",
                        "follow_up": [
                            "对产品质量的影响程度？",
                            "对客户满意度的影响？",
                            "对成本和时间的影响？"
                        ],
                        "answer_type": "影响评估",
                        "validation": ["评估是否客观", "是否有数据支持"]
                    }
                ]
            },
            "root_cause": {
                "description": "根本原因挖掘阶段",
                "questions": [
                    {
                        "id": "why_immediate",
                        "question": "为什么会出现这个问题？请分析直接原因。",
                        "category": "直接原因",
                        "purpose": "识别问题的直接原因",
                        "follow_up": [
                            "这个直接原因是由什么导致的？",
                            "是否有关键的触发条件？",
                            "涉及哪些具体的环节或部件？"
                        ],
                        "answer_type": "原因分析",
                        "validation": ["原因是否具体", "是否可验证"]
                    },
                    {
                        "id": "why_systematic",
                        "question": "从系统角度看，为什么预防措施没有发挥作用？",
                        "category": "系统原因",
                        "purpose": "分析系统层面的问题",
                        "follow_up": [
                            "现有的控制措施为什么失效？",
                            "系统设计是否存在缺陷？",
                            "监控机制是否有效？"
                        ],
                        "answer_type": "系统分析",
                        "validation": ["分析是否深入", "是否触及根本"]
                    },
                    {
                        "id": "why_process",
                        "question": "在流程和程序方面，哪些环节可能存在问题？",
                        "category": "流程原因",
                        "purpose": "分析流程和程序问题",
                        "follow_up": [
                            "作业标准是否清晰完整？",
                            "流程设计是否合理？",
                            "执行过程是否有偏差？"
                        ],
                        "answer_type": "流程分析",
                        "validation": ["分析是否全面", "是否有改进空间"]
                    }
                ]
            },
            "prevention": {
                "description": "预防措施探讨阶段",
                "questions": [
                    {
                        "id": "how_prevent",
                        "question": "如何防止这类问题再次发生？",
                        "category": "预防措施",
                        "purpose": "制定有效的预防措施",
                        "follow_up": [
                            "需要修改哪些程序或标准？",
                            "需要增加哪些检查点？",
                            "需要哪些培训和能力提升？"
                        ],
                        "answer_type": "措施建议",
                        "validation": ["措施是否可行", "是否有针对性"]
                    }
                ]
            }
        }

    def start_interview(self, problem_description: str) -> Dict:
        """
        开始问题访谈

        Args:
            problem_description: 问题初始描述

        Returns:
            Dict: 访谈开始信息和第一个问题
        """
        self.conversation_history = []
        self.current_phase = "initial"
        self.questions_asked = []
        self.responses = {}

        # 记录初始问题
        initial_response = UserResponse(
            question_id="initial_problem",
            answer_text=problem_description,
            answer_details=[],
            confidence_level="initial",
            supporting_evidence=[],
            timestamp=datetime.now().isoformat()
        )
        self.responses["initial_problem"] = initial_response

        # 返回初始问题
        first_question = self.get_next_question()
        return {
            "status": "started",
            "current_phase": self.current_phase,
            "next_question": first_question,
            "progress": "初始问题已记录，开始5W1H追问"
        }

    def get_next_question(self) -> Optional[QuestionContext]:
        """获取下一个问题"""
        if self.current_phase not in self.question_templates:
            return None

        phase_questions = self.question_templates[self.current_phase]["questions"]

        # 找到下一个未提问的问题
        for question in phase_questions:
            if question["id"] not in self.questions_asked:
                return QuestionContext(
                    question_id=question["id"],
                    question_text=question["question"],
                    category=question["category"],
                    purpose=question["purpose"],
                    follow_up_questions=question["follow_up"],
                    expected_answer_type=question["answer_type"],
                    validation_criteria=question["validation"]
                )

        return None

    def process_response(self, question_id: str, answer_text: str,
                       answer_details: List[str] = None,
                       confidence_level: str = "medium",
                       supporting_evidence: List[str] = None) -> Dict:
        """
        处理用户回答

        Args:
            question_id: 问题ID
            answer_text: 回答文本
            answer_details: 回答详情
            confidence_level: 信心水平
            supporting_evidence: 支持证据

        Returns:
            Dict: 处理结果和下一步操作
        """
        # 创建用户回答记录
        user_response = UserResponse(
            question_id=question_id,
            answer_text=answer_text,
            answer_details=answer_details or [],
            confidence_level=confidence_level,
            supporting_evidence=supporting_evidence or [],
            timestamp=datetime.now().isoformat()
        )

        # 保存回答
        self.responses[question_id] = user_response
        self.questions_asked.append(question_id)

        # 检查是否可以进入下一阶段
        phase_completion = self._check_phase_completion()

        if phase_completion["is_complete"]:
            next_phase = self._get_next_phase()
            if next_phase:
                self.current_phase = next_phase
                return {
                    "status": "phase_complete",
                    "phase_summary": phase_completion["summary"],
                    "next_phase": self.current_phase,
                    "next_question": self.get_next_question(),
                    "progress": f"{phase_completion['summary']}，准备进入{next_phase}阶段"
                }

        # 返回下一个问题
        next_question = self.get_next_question()
        if next_question:
            return {
                "status": "question_answered",
                "next_question": next_question,
                "progress": f"问题{question_id}已回答，准备下一个问题"
            }
        else:
            return {
                "status": "interview_complete",
                "summary": self.generate_interview_summary(),
                "progress": "所有阶段的问题都已完成"
            }

    def _check_phase_completion(self) -> Dict:
        """检查当前阶段是否完成"""
        if self.current_phase not in self.question_templates:
            return {"is_complete": False}

        phase_questions = self.question_templates[self.current_phase]["questions"]
        phase_question_ids = [q["id"] for q in phase_questions]

        answered_count = len([qid for qid in phase_question_ids if qid in self.questions_asked])
        total_count = len(phase_question_ids)

        is_complete = answered_count >= total_count * 0.8  # 80%完成度即认为完成

        summary = f"{self.question_templates[self.current_phase]['description']} - {answered_count}/{total_count} 问题已完成"

        return {
            "is_complete": is_complete,
            "answered_count": answered_count,
            "total_count": total_count,
            "summary": summary
        }

    def _get_next_phase(self) -> Optional[str]:
        """获取下一个阶段"""
        phase_order = ["initial", "root_cause", "prevention"]
        current_index = phase_order.index(self.current_phase) if self.current_phase in phase_order else -1

        if current_index < len(phase_order) - 1:
            return phase_order[current_index + 1]

        return None

    def generate_interview_summary(self) -> Dict:
        """生成访谈总结"""
        summary = {
            "访谈完成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "访谈阶段": list(self.responses.keys()),
            "问题分析": {},
            "关键发现": [],
            "建议措施": []
        }

        # 分析回答质量
        for question_id, response in self.responses.items():
            summary["问题分析"][question_id] = {
                "回答内容": response.answer_text,
                "信心水平": response.confidence_level,
                "支持证据": response.supporting_evidence
            }

        # 提取关键发现
        key_findings = []
        for response in self.responses.values():
            if "原因" in response.answer_text or "导致" in response.answer_text:
                key_findings.append(response.answer_text)

        summary["关键发现"] = key_findings

        return summary

    def export_conversation(self, output_path: str) -> str:
        """导出对话记录"""
        export_data = {
            "访谈记录": {
                "开始时间": self.responses.get("initial_problem", {}).timestamp if hasattr(self, 'responses') else "",
                "完成时间": datetime.now().isoformat(),
                "当前阶段": self.current_phase,
                "对话历史": []
            }
        }

        # 添加所有问题和回答
        for question_id, response in self.responses.items():
            export_data["访谈记录"]["对话历史"].append({
                "问题ID": question_id,
                "回答": asdict(response)
            })

        # 添加总结
        export_data["访谈总结"] = self.generate_interview_summary()

        # 保存文件
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        return output_path

    def get_remaining_questions(self) -> List[str]:
        """获取剩余未问的问题"""
        remaining = []
        if self.current_phase in self.question_templates:
            phase_questions = self.question_templates[self.current_phase]["questions"]
            for question in phase_questions:
                if question["id"] not in self.questions_asked:
                    remaining.append(question["question"])

        return remaining

def main():
    """主函数，用于测试"""
    interviewer = FiveWInterviewer()

    # 开始访谈
    result = interviewer.start_interview("空调制冷效果不佳，客户投诉频繁")
    print("访谈开始:", result)

    # 模拟回答问题
    if result["next_question"]:
        question = result["next_question"]
        print(f"问题: {question.question_text}")

        # 模拟用户回答
        response = interviewer.process_response(
            question.question_id,
            "压缩机启动后立即停止工作",
            ["压缩机有异响", "外壳发热严重"],
            "high",
            ["现场照片", "维修记录"]
        )
        print("回答处理结果:", response)

    # 导出对话记录
    export_file = interviewer.export_conversation("interview_record.json")
    print(f"对话记录已导出: {export_file}")

if __name__ == "__main__":
    main()
