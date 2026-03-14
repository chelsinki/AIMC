# AIMC 数字人主持系统 (MVP)

## 🚀 项目概述

AIMC（AI Master of Ceremonies）是一套基于 **POMASA (Prompt-Defined Multi-Agent System Architecture)** 架构的数字人主持系统。本项目专为大会“双主持”场景设计，通过多智能体协作，实现 AI 主持人与人类主持人的无缝配合、临场应变及专业演讲评价。

## ✨ 核心能力

### 🎙️ P0 - 基础主持
- **智能语音检测**: 精准捕捉人类主持人发言结束时点。
- **流程控制**: 严格遵循预设脚本，推进大会议程。
- **无缝衔接**: 数字人自然切入，模拟真实主持节奏。

### 🧠 P1 - 临场应变
- **语义理解**: 深度解析人类主持人的即兴发言。
- **动态衔接**: 自动生成过渡词，平滑过渡回主流程。

### 📊 P3 - 演讲评价
- **要点提取**: 实时记录并提炼嘉宾发言精华。
- **专业点评**: 基于预设标准生成高水平评价内容。

## 🏗️ 技术架构

### 基于 POMASA 的结构化设计
```text
AIMC/
├── agents/          # 智能体蓝图 (Blueprint)
├── methodology/     # 行为准则与方法论
├── materials/       # 脚本、词库、动画等原始素材
├── src/             # 核心运行代码 (MVP 实现)
└── README.md        # 项目导航
```

### 核心智能体集群
1. **Orchestrator**: 流程总控，负责环节流转。
2. **HumanDetector**: 语音/状态感知。
3. **AILineDeliver**: 台词交付与播放。
4. **ContextAnalyzer**: 语义环境深度分析。
5. **ResponseGenerator**: 动态应变生成。
6. **SpeechEvaluator**: 演讲复盘与评价。

## 🛠️ 快速开始

### 1. 环境准备
- Python 3.11+
- 安装依赖:
  ```bash
  pip install -r requirements.txt
  ```

### 2. 运行 MVP 演示
项目内置了一个 MVP 演示脚本，展示了从脚本解析、头像生成到模拟主持的全流程：
```bash
python mvp_main.py
```

## 📂 项目结构详细说明

- **[agents/](agents/)**: 遵循 `COR-01` 模式定义的 Agent 蓝图。
- **[methodology/](methodology/)**: 包含主持稿规范、应变策略及评价标准。
- **[src/aimc/](src/aimc/)**: 系统核心逻辑，包括 TTS 引擎、头像生成器和脚本解析器。
- **[materials/](materials/)**: 存储生成的素材及预设的词库。

## 📈 未来路线图
- **Phase 1**: 完善实时语音识别 (ASR) 接入。
- **Phase 2**: 集成 Seedance 等专业级数字人动画引擎。
- **Phase 3**: 增强多语种主持能力。

---

## 📄 许可证
Apache License 2.0

## 🤝 贡献与反馈
欢迎通过 Issue 或 Pull Request 提交您的建议。
项目负责人: **Chang Ma** ([chang.ma@outlook.com](mailto:chang.ma@outlook.com))
GitHub: [https://github.com/chelsinki/AIMC](https://github.com/chelsinki/AIMC)
