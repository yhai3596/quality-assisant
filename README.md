# 品质问题处理专家技能

## 技能概述

这是一个专业的品质问题处理专家技能，专门针对北美空调产品的质量问题处理。技能采用三层架构设计，结合AI多媒体处理能力，提供完整的质量分析和问题解决流程。

## 核心特性

### 🎯 三层架构体系
1. **智能问题识别与分流** - 自动识别问题类型，选择对应流程
2. **深度分析处理** - 5W1H追问+根因分析，挖掘问题本质
3. **专业报告输出** - 8D报告生成，改进措施制定

### 🖼️ 多媒体内容处理
- 集成AI模型API进行图像/视频分析
- 支持图片质量缺陷检测
- 支持视频操作流程分析
- 支持故障现象自动识别

### 📋 标准化流程
- 遵循8D报告国际标准
- 采用5W1H分析方法论
- 应用PDCA持续改进循环
- 结合北美HVAC技术标准

## 文件结构

```
quality-problem-expert/
├── SKILL.md                              # 核心技能文档
├── README.md                             # 说明文档（本文件）
├── scripts/                              # 脚本工具
│   ├── multimedia_processor.py           # 多媒体内容处理器
│   ├── five_w_interviewer.py            # 5W1H追问引导器
│   └── eight_d_report_generator.py      # 8D报告生成器
├── references/                          # 参考资料
│   ├── 8d_report_standard.md           # 8D报告标准
│   ├── 5w_analysis_method.md            # 5W1H分析方法
│   └── north_america_hvac_standards.md  # 北美空调技术标准
└── assets/                              # 资产模板
    ├── 8D_report_template.md            # 8D报告模板
    └── problem_analysis_form.md         # 问题分析表格
```

## 使用方法

### 1. 快速开始
```python
# 导入多媒体处理器
from scripts.multimedia_processor import MultimediaProcessor

processor = MultimediaProcessor()
result = processor.process_image("defect.jpg", "quality_defect")
```

### 2. 5W1H问题分析
```python
from scripts.five_w_interviewer import FiveWInterviewer

interviewer = FiveWInterviewer()
result = interviewer.start_interview("空调制冷效果不佳")
```

### 3. 8D报告生成
```python
from scripts.eight_d_report_generator import EightDReportGenerator

generator = EightDReportGenerator()
report = generator.generate_report("output/8D_report.json")
```

## 主要功能模块

### 多媒体处理器 (multimedia_processor.py)
- **图片分析**: 质量缺陷检测、产品状态评估
- **视频分析**: 操作序列分析、故障现象分析
- **AI集成**: 支持多种AI模型API调用
- **报告生成**: 自动生成多媒体分析报告

### 5W1H追问器 (five_w_interviewer.py)
- **智能引导**: 系统性5W1H追问流程
- **信息收集**: 结构化信息收集和验证
- **深度挖掘**: 多轮追问挖掘根本原因
- **对话管理**: 完整的对话记录和导出

### 8D报告生成器 (eight_d_report_generator.py)
- **完整流程**: 支持D0-D8所有阶段
- **标准规范**: 遵循国际8D标准
- **多格式输出**: JSON、Word、Markdown格式
- **状态跟踪**: 实时跟踪报告完成状态

## 参考资料

### 8D报告标准
- 详细的8D方法论说明
- 每个阶段的具体要求
- 标准模板和格式
- 成功关键因素

### 5W1H分析方法
- 系统性问题分析框架
- 追问技巧和沟通方法
- 分析工具和模板
- 实际案例分析

### 北美HVAC标准
- AHRI、UL、ETL认证要求
- 技术性能标准
- 安装维修规范
- 质量问题预防

## 适用场景

### 产品生命周期
- **设计阶段**: 设计质量审查、DFMEA分析
- **生产阶段**: 质量问题诊断、缺陷分析
- **售后阶段**: 客户投诉分析、故障排除
- **改进阶段**: 持续改进、预防措施制定

### 应用领域
- ✅ 北美空调产品质量投诉分析
- ✅ 生产现场质量问题诊断
- ✅ 供应商质量评估
- ✅ 市场反馈问题处理
- ✅ 产品质量改进项目

## 技术优势

### 智能化
- 自动问题分类和分流
- AI驱动的多媒体分析
- 智能信息收集引导
- 个性化报告生成

### 标准化
- 遵循国际标准规范
- 统一的分析流程
- 专业的报告格式
- 完整的文档体系

### 模块化
- 独立的处理模块
- 可重用的组件
- 灵活的配置选项
- 易于扩展和维护

## 安装和使用

### 环境要求
- Python 3.7+
- 必要的Python包：
  - json, datetime, dataclasses
  - zipfile, os (内置)
  - base64 (内置)

### 快速安装
1. 解压 `quality-problem-expert.zip`
2. 导入所需的脚本模块
3. 按照示例代码调用相应功能

### 依赖库
```bash
# 基础库（通常已预装）
pip install json datetime dataclasses zipfile os base64

# 可选库（用于Word文档生成）
pip install python-docx

# AI API集成（根据需要）
pip install openai anthropic requests
```

## 最佳实践

### 问题分析
1. **充分收集信息**: 使用5W1H方法系统收集信息
2. **多媒体辅助**: 充分利用图片和视频证据
3. **标准化分析**: 严格遵循8D流程和标准
4. **数据驱动**: 基于事实和数据进行分析

### 报告生成
1. **及时更新**: 在分析过程中及时更新报告
2. **完整记录**: 确保所有阶段都有详细记录
3. **可追溯**: 建立完整的证据链
4. **可执行**: 提供具体可操作的改进措施

### 持续改进
1. **经验总结**: 定期总结经验教训
2. **流程优化**: 持续优化分析流程
3. **模板更新**: 根据实际情况更新模板
4. **知识分享**: 与团队分享最佳实践

## 注意事项

### 数据安全
- 确保问题描述的完整性和准确性
- 保护敏感的客户信息和商业机密
- 遵循公司数据安全政策
- 妥善处理多媒体文件

### 分析质量
- 对于复杂问题，需要多轮交互收集信息
- 报告内容必须基于事实和数据
- 改进措施需要结合实际情况制定
- 定期验证分析结论的准确性

## 扩展建议

### 功能扩展
- 集成更多AI模型
- 添加统计分析功能
- 开发Web界面
- 增加移动端支持

### 流程优化
- 自动化程度提升
- 分析速度优化
- 报告美观度改进
- 用户体验提升

## 技术支持

### 问题排查
- 检查Python环境
- 验证依赖库安装
- 查看错误日志
- 参考示例代码

### 功能增强
- 自定义分析流程
- 添加新的分析工具
- 集成外部系统
- 开发插件机制

## 版本信息

- **当前版本**: v1.0
- **创建日期**: 2024-01-21
- **兼容性**: Python 3.7+
- **许可证**: 根据使用场景确定

## 更新日志

### v1.0 (2024-01-21)
- 初始版本发布
- 完整的8D报告功能
- 多媒体内容处理
- 5W1H分析方法
- 北美HVAC标准支持
- 专业模板和文档

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue到项目仓库
- 发送邮件至开发团队
- 参与技术讨论

---

**版权声明**: 本技能遵循开源协议，欢迎贡献代码和建议。
