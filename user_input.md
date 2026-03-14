# AIMC 数字人主持系统 - 用户输入

## 语言设置

**Agent Blueprint Language**:
中文

**Report Output Language**:
中文

---

## 研究项目基本信息

**Project Identifier**:
aimc_hosting_system

**Research Topic and Core Questions**:
开发一套AI数字人主持系统，用于大会双主持场景。核心问题包括：
1. 如何准确检测人类主持人何时结束发言，确保数字人无缝衔接
2. 如何理解人类主持人的临场变化，生成自然的衔接内容
3. 如何支持数字人临场互动，使用现有skills进行即兴发挥
4. 如何实时记录演讲内容并生成专业评价

**Initial Ideas and Insights**:
- 采用POMASA多智能体架构，确保系统模块化和可扩展
- 语音检测采用音量检测与静默检测混合方案
- 应变响应采用预制库+实时生成混合策略
- 使用Seedance生成数字人视觉素材，我们负责控制逻辑

---

## 数据收集

**Data Sources**:
- 用户提供的主持稿（Markdown格式）
- Seedance生成的数字人动画素材
- 预生成的TTS音频文件
- 现场语音输入

**Existing Reference Materials**:
- /Users/chang_porsche/Documents/trae_projects/Claude Code/pomasa/skills/pomasa/

---

## 分析方法

**Analysis Methods**:
to be suggested by AI

---

## 输出格式

**Report Format**:
技术设计文档 + 研究报告

**Report Structure**:
to be suggested by AI

**Deliverable File Formats**:
- [x] Markdown (always generated)
- [x] DOCX (recommended, for editing)
- [x] PDF (recommended, for distribution)

---

## 模式选择

**Quality Assurance Level**:
- [ ] Simple: Only adopt required patterns, no additional quality checks
- [x] Standard (default): Adopt QUA-01 Embedded Quality Standards + BHV-05 Grounded Web Research
- [ ] Strict: Adopt QUA-01 + QUA-02 Multi-Layer Quality Assurance + BHV-05 Grounded Web Research

**Other Patterns to Enable or Disable**:
None

---

## 其他要求

**Other Requirements**:
1. 系统需要支持12月大会的主持需求
2. TTS为主，也支持预生成音频
3. 主持稿晚些时候给出，需要支持共创
4. 临场应变需要处理观众反应等即兴场景
5. 演讲评价需要记录嘉宾内容，夸表达和洞见
