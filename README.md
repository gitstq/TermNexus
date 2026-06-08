<div align="center">

# 🧠 TermNexus

**AI Terminal Workspace Intelligence Engine**

*AI终端工作区智能引擎 | AI終端工作區智慧引擎*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](https://github.com/gitstq/TermNexus)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-orange)](https://github.com/gitstq/TermNexus)

[English](#english) | [简体中文](#simplified-chinese) | [繁體中文](#traditional-chinese)

</div>

---

<a name="english"></a>
## English

### 🎉 Introduction

**TermNexus** is an intelligent terminal workspace management engine designed for the AI era. It solves the pain point of developers frequently switching between multiple AI Agent sessions, code projects, and shell environments.

**Core Problem Solved:**
- Constantly switching between Claude Code, Codex, Cursor, and other AI tools
- Losing context when jumping between different project directories
- No visibility into which AI Agents are running and where
- Manual environment variable management for each workspace

**Self-Developed Differentiation:**
- **Zero external dependencies** - Pure Python standard library implementation
- **AI Agent Session Awareness** - Auto-detects Claude, Codex, Cursor, Gemini, Aider, Continue, Copilot, Ollama
- **Smart Context Routing** - Intelligent workspace recommendations based on your current context
- **Beautiful TUI Dashboard** - Real-time monitoring of all workspaces and sessions
- **Cross-platform** - Works on Linux, macOS, and Windows

### ✨ Core Features

| Feature | Description | Icon |
|---------|-------------|------|
| **Workspace Management** | Create, organize, and switch between project workspaces with full context preservation | 📁 |
| **AI Agent Detection** | Automatically detect running AI Agent processes and associate them with workspaces | 🤖 |
| **Smart Routing** | Context-aware workspace recommendations based on recent commands and active agents | 🧭 |
| **TUI Dashboard** | Beautiful terminal dashboard with real-time workspace and session monitoring | 📊 |
| **Auto Type Detection** | Automatically detect project type (Python, Node.js, Rust, Go, Docker, etc.) | 🔍 |
| **Session Tracking** | Track shell sessions, agent sessions, and server processes per workspace | 💻 |
| **Environment Variables** | Per-workspace environment variable management | ⚙️ |
| **Git Integration** | Auto-detect git branch and repository information | 📦 |
| **Zero Dependencies** | No external packages required - works out of the box | 🎯 |

### 🚀 Quick Start

#### Requirements
- **Python 3.8+**
- Terminal with ANSI color support (optional but recommended)

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/TermNexus.git
cd TermNexus

# Install in development mode
pip install -e .

# Or install directly
python setup.py install
```

#### Basic Usage

```bash
# Create a new workspace
termnexus create my-project --path ./my-project

# List all workspaces
termnexus list

# Switch to a workspace (changes directory and sets env vars)
termnexus switch my-project

# Show full dashboard
termnexus dashboard

# Show AI Agent summary
termnexus agents

# Get workspace recommendations
termnexus recommend

# Show current context
termnexus context
```

**Alias:** `tnx` is a shorthand for `termnexus`
```bash
tnx create my-project
tnx list
tnx dashboard
```

### 📖 Detailed Usage Guide

#### Workspace Commands

```bash
# Create workspace with specific type
termnexus create backend-api --type python --tag api --tag flask

# Create workspace for AI Agent project
termnexus create ai-chatbot --type agent --tag claude

# List with filters
termnexus list --type python
termnexus list --tag claude

# Rename workspace
termnexus rename old-name new-name

# Delete workspace
termnexus delete my-project --force

# Show workspace details
termnexus info my-project
```

#### Session Management

```bash
# List all sessions
termnexus sessions

# List only AI Agent sessions
termnexus sessions --agent

# List sessions by type
termnexus sessions --type shell
```

#### Routing & Recommendations

```bash
# View routing rules
termnexus route rules

# Add custom routing rule
termnexus route add my-rule "pattern" "target-workspace" --priority 10

# View routing history
termnexus route history

# View switch patterns
termnexus route patterns
```

### 💡 Design Philosophy & Roadmap

**Design Philosophy:**
- **Simplicity First** - Zero dependencies means zero friction
- **Context Preservation** - Never lose your place when switching contexts
- **AI-Native** - Built from the ground up for the AI-assisted development era
- **Developer-Centric** - Every feature solves a real developer pain point

**Technology Choices:**
- Pure Python standard library for maximum compatibility
- ANSI escape codes for cross-platform terminal UI
- JSON-based persistence for human-readable data
- Modular architecture for easy extension

**Future Roadmap:**
- [ ] Plugin system for custom agent detectors
- [ ] Integration with popular terminal multiplexers (tmux, zellij)
- [ ] Workspace templates for quick project initialization
- [ ] Remote workspace support via SSH
- [ ] Web-based dashboard option
- [ ] Team workspace sharing

### 📦 Packaging & Deployment

#### From Source
```bash
git clone https://github.com/gitstq/TermNexus.git
cd TermNexus
pip install -e .
```

#### Build Distribution
```bash
# Build wheel and source distribution
make build

# Or manually
python -m build
```

#### Run Tests
```bash
make test
# Or
python -m unittest discover tests/ -v
```

### 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- Report issues via [GitHub Issues](https://github.com/gitstq/TermNexus/issues)
- Submit PRs following [Conventional Commits](https://www.conventionalcommits.org/)
- Write tests for new features
- Follow PEP 8 style guidelines

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<a name="simplified-chinese"></a>
## 简体中文

### 🎉 项目介绍

**TermNexus** 是一款专为 AI 时代设计的智能终端工作区管理引擎。它解决了开发者在多个 AI Agent 会话、代码项目和 Shell 环境之间频繁切换的痛点。

**解决的核心问题：**
- 在 Claude Code、Codex、Cursor 等 AI 工具之间不断切换
- 在不同项目目录间跳转时丢失上下文
- 无法了解哪些 AI Agent 正在运行以及它们的位置
- 每个工作区需要手动管理环境变量

**自研差异化亮点：**
- **零外部依赖** - 纯 Python 标准库实现
- **AI Agent 会话感知** - 自动检测 Claude、Codex、Cursor、Gemini、Aider、Continue、Copilot、Ollama
- **智能上下文路由** - 基于当前上下文提供智能工作区推荐
- **精美 TUI 仪表盘** - 实时监控所有工作区和会话
- **跨平台兼容** - 支持 Linux、macOS 和 Windows

### ✨ 核心特性

| 特性 | 描述 | 图标 |
|---------|-------------|------|
| **工作区管理** | 创建、组织工作区，完整保留上下文 | 📁 |
| **AI Agent 检测** | 自动检测运行中的 AI Agent 进程并关联到工作区 | 🤖 |
| **智能路由** | 基于最近命令和活跃 Agent 的上下文感知工作区推荐 | 🧭 |
| **TUI 仪表盘** | 精美的终端仪表盘，实时监控工作区和会话 | 📊 |
| **自动类型检测** | 自动检测项目类型（Python、Node.js、Rust、Go、Docker 等） | 🔍 |
| **会话追踪** | 按工作区追踪 Shell 会话、Agent 会话和服务器进程 | 💻 |
| **环境变量管理** | 每个工作区独立的环境变量管理 | ⚙️ |
| **Git 集成** | 自动检测 Git 分支和仓库信息 | 📦 |
| **零依赖** | 无需外部包，开箱即用 | 🎯 |

### 🚀 快速开始

#### 环境要求
- **Python 3.8+**
- 支持 ANSI 颜色的终端（可选但推荐）

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/TermNexus.git
cd TermNexus

# 开发模式安装
pip install -e .

# 或直接安装
python setup.py install
```

#### 基础用法

```bash
# 创建新工作区
termnexus create my-project --path ./my-project

# 列出所有工作区
termnexus list

# 切换到工作区（切换目录并设置环境变量）
termnexus switch my-project

# 显示完整仪表盘
termnexus dashboard

# 显示 AI Agent 概览
termnexus agents

# 获取工作区推荐
termnexus recommend

# 显示当前上下文
termnexus context
```

**快捷命令：** `tnx` 是 `termnexus` 的简写
```bash
tnx create my-project
tnx list
tnx dashboard
```

### 📖 详细使用指南

#### 工作区命令

```bash
# 创建指定类型的工作区
termnexus create backend-api --type python --tag api --tag flask

# 为 AI Agent 项目创建工作区
termnexus create ai-chatbot --type agent --tag claude

# 带过滤条件的列表
termnexus list --type python
termnexus list --tag claude

# 重命名工作区
termnexus rename old-name new-name

# 删除工作区
termnexus delete my-project --force

# 显示工作区详情
termnexus info my-project
```

#### 会话管理

```bash
# 列出所有会话
termnexus sessions

# 仅列出 AI Agent 会话
termnexus sessions --agent

# 按类型列出会话
termnexus sessions --type shell
```

#### 路由与推荐

```bash
# 查看路由规则
termnexus route rules

# 添加自定义路由规则
termnexus route add my-rule "pattern" "target-workspace" --priority 10

# 查看路由历史
termnexus route history

# 查看切换模式
termnexus route patterns
```

### 💡 设计思路与迭代规划

**设计理念：**
- **简洁优先** - 零依赖意味着零摩擦
- **上下文保留** - 切换上下文时永不丢失位置
- **AI 原生** - 从底层为 AI 辅助开发时代构建
- **开发者中心** - 每个功能都解决真实的开发者痛点

**技术选型原因：**
- 纯 Python 标准库实现，最大兼容性
- ANSI 转义码实现跨平台终端 UI
- JSON 持久化，数据人类可读
- 模块化架构，易于扩展

**后续迭代计划：**
- [ ] 自定义 Agent 检测器插件系统
- [ ] 与主流终端复用器集成（tmux、zellij）
- [ ] 工作区模板，快速项目初始化
- [ ] 通过 SSH 的远程工作区支持
- [ ] Web 仪表盘选项
- [ ] 团队工作区共享

### 📦 打包与部署指南

#### 从源码安装
```bash
git clone https://github.com/gitstq/TermNexus.git
cd TermNexus
pip install -e .
```

#### 构建分发包
```bash
# 构建 wheel 和源码分发包
make build

# 或手动构建
python -m build
```

#### 运行测试
```bash
make test
# 或
python -m unittest discover tests/ -v
```

### 🤝 贡献指南

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

- 通过 [GitHub Issues](https://github.com/gitstq/TermNexus/issues) 报告问题
- 提交 PR 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范
- 为新功能编写测试
- 遵循 PEP 8 代码风格

### 📄 开源协议

本项目采用 [MIT 协议](LICENSE) 开源。

---

<a name="traditional-chinese"></a>
## 繁體中文

### 🎉 專案介紹

**TermNexus** 是一款專為 AI 時代設計的智慧終端工作區管理引擎。它解決了開發者在多個 AI Agent 會話、程式碼專案和 Shell 環境之間頻繁切換的痛點。

**解決的核心問題：**
- 在 Claude Code、Codex、Cursor 等 AI 工具之間不斷切換
- 在不同專案目錄間跳轉時遺失上下文
- 無法了解哪些 AI Agent 正在執行以及它們的位置
- 每個工作區需要手動管理環境變數

**自研差異化亮點：**
- **零外部依賴** - 純 Python 標準庫實作
- **AI Agent 會話感知** - 自動偵測 Claude、Codex、Cursor、Gemini、Aider、Continue、Copilot、Ollama
- **智慧上下文路由** - 基於當前上下文提供智慧工作區推薦
- **精美 TUI 儀表板** - 即時監控所有工作區和會話
- **跨平台相容** - 支援 Linux、macOS 和 Windows

### ✨ 核心特性

| 特性 | 描述 | 圖示 |
|---------|-------------|------|
| **工作區管理** | 建立、組織工作區，完整保留上下文 | 📁 |
| **AI Agent 偵測** | 自動偵測執行中的 AI Agent 程序並關聯到工作區 | 🤖 |
| **智慧路由** | 基於最近命令和活躍 Agent 的上下文感知工作區推薦 | 🧭 |
| **TUI 儀表板** | 精美的終端儀表板，即時監控工作區和會話 | 📊 |
| **自動類型偵測** | 自動偵測專案類型（Python、Node.js、Rust、Go、Docker 等） | 🔍 |
| **會話追蹤** | 按工作區追蹤 Shell 會話、Agent 會話和伺服器程序 | 💻 |
| **環境變數管理** | 每個工作區獨立的環境變數管理 | ⚙️ |
| **Git 整合** | 自動偵測 Git 分支和倉庫資訊 | 📦 |
| **零依賴** | 無需外部套件，開箱即用 | 🎯 |

### 🚀 快速開始

#### 環境要求
- **Python 3.8+**
- 支援 ANSI 顏色的終端（可選但推薦）

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/TermNexus.git
cd TermNexus

# 開發模式安裝
pip install -e .

# 或直接安裝
python setup.py install
```

#### 基礎用法

```bash
# 建立新工作區
termnexus create my-project --path ./my-project

# 列出所有工作區
termnexus list

# 切換到工作區（切換目錄並設定環境變數）
termnexus switch my-project

# 顯示完整儀表板
termnexus dashboard

# 顯示 AI Agent 概覽
termnexus agents

# 獲取工作區推薦
termnexus recommend

# 顯示目前上下文
termnexus context
```

**快捷命令：** `tnx` 是 `termnexus` 的簡寫
```bash
tnx create my-project
tnx list
tnx dashboard
```

### 📖 詳細使用指南

#### 工作區命令

```bash
# 建立指定類型的工作區
termnexus create backend-api --type python --tag api --tag flask

# 為 AI Agent 專案建立工作區
termnexus create ai-chatbot --type agent --tag claude

# 帶過濾條件的列表
termnexus list --type python
termnexus list --tag claude

# 重新命名工作區
termnexus rename old-name new-name

# 刪除工作區
termnexus delete my-project --force

# 顯示工作區詳情
termnexus info my-project
```

#### 會話管理

```bash
# 列出所有會話
termnexus sessions

# 僅列出 AI Agent 會話
termnexus sessions --agent

# 按類型列出會話
termnexus sessions --type shell
```

#### 路由與推薦

```bash
# 查看路由規則
termnexus route rules

# 新增自訂路由規則
termnexus route add my-rule "pattern" "target-workspace" --priority 10

# 查看路由歷史
termnexus route history

# 查看切換模式
termnexus route patterns
```

### 💡 設計思路與迭代規劃

**設計理念：**
- **簡潔優先** - 零依賴意味著零摩擦
- **上下文保留** - 切換上下文時永不遺失位置
- **AI 原生** - 從底層為 AI 輔助開發時代建構
- **開發者中心** - 每個功能都解決真實的開發者痛點

**技術選型原因：**
- 純 Python 標準庫實作，最大相容性
- ANSI 轉義碼實現跨平台終端 UI
- JSON 持久化，資料人類可讀
- 模組化架構，易於擴展

**後續迭代計畫：**
- [ ] 自訂 Agent 偵測器外掛系統
- [ ] 與主流終端複用器整合（tmux、zellij）
- [ ] 工作區模板，快速專案初始化
- [ ] 透過 SSH 的遠端工作區支援
- [ ] Web 儀表板選項
- [ ] 團隊工作區共享

### 📦 打包與部署指南

#### 從原始碼安裝
```bash
git clone https://github.com/gitstq/TermNexus.git
cd TermNexus
pip install -e .
```

#### 建置發布包
```bash
# 建置 wheel 和原始碼發布包
make build

# 或手動建置
python -m build
```

#### 執行測試
```bash
make test
# 或
python -m unittest discover tests/ -v
```

### 🤝 貢獻指南

歡迎貢獻！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

- 透過 [GitHub Issues](https://github.com/gitstq/TermNexus/issues) 報告問題
- 提交 PR 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範
- 為新功能編寫測試
- 遵循 PEP 8 程式碼風格

### 📄 開源協議

本專案採用 [MIT 協議](LICENSE) 開源。
