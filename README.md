# Policy Weekly - 政策研究周报生成器

一个自动化生成政策研究周报的 AI Skill，帮助你每周自动监测 AI 政策、互联网监管、投融资政策动态。

> **兼容性说明**：本 Skill 采用通用 AI Skill 格式（标准 YAML frontmatter + Markdown），兼容所有支持该格式的 AI 编程助手，包括 Claude Code、Codeflicker 等，并非 Claude Code 专属。

## ✨ 功能特点

- 🤖 **一键生成周报** - 自动搜索过去7天政策新闻，生成结构化报告
- 📊 **三大主题覆盖** - AI政策、互联网监管、投融资政策
- 🔍 **权威数据源** - 集成 Tavily Search，获取全球权威媒体报道
- 💾 **智能缓存** - 避免重复搜索，节省 API 配额
- 📝 **标准模板** - 包含深度分析、影响评估、行动建议
- 📁 **自动归档** - 支持 Obsidian MCP 自动归档

## 📦 安装

### 前置要求

1. **支持 AI Skill 格式的工具**，如 Claude Code、Codeflicker 等
2. **Tavily API Key** - [获取地址](https://tavily.com)
3. **tavily-search skill** - 需在你使用的工具中已安装

### 安装步骤

```bash
# 1. 下载或克隆此 skill
git clone https://github.com/gloria-oss/policy-weekly.git

# 2. 复制到 skills 目录（Claude Code 和 Codeflicker 共用同一目录）
cp -r policy-weekly ~/.claude/skills/

# 3. 配置环境变量
export TAVILY_API_KEY="tvly-your-api-key-here"

# 4. （可选）配置 Obsidian 路径
export OBSIDIAN_VAULT_PATH="/path/to/your/vault"
```

### 验证安装

```bash
# 检查是否安装成功
ls ~/.claude/skills/policy-weekly

# 在你使用的 AI 工具中测试
/policy-weekly ai-policy
```

## 🚀 快速开始

### 1. 配置 API Key（⚠️ 必需）

**你的 Tavily API Key 是必需的，不会使用其他人的 API key。**

```bash
# 临时设置（当前终端session）
export TAVILY_API_KEY="tvly-your-api-key-here"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export TAVILY_API_KEY="tvly-your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**重要提示：**
- ✅ Skill 会在首次使用时检查你的 API key 是否已设置
- ✅ 如果未设置，会提示你如何配置
- ✅ 不会使用其他人的 API key
- ✅ API key 应该以 `tvly-` 开头

**获取 API Key：** 访问 https://tavily.com 注册并获取

### 2. 配置保存路径（可选）

默认保存到 `~/projects/research/`，你可以修改：

```bash
# 设置自定义报告保存路径
export POLICY_REPORT_PATH="/your/custom/path"

# 设置自定义缓存路径（默认: ~/policy-weekly/cache）
export POLICY_CACHE_PATH="/your/custom/cache/path"
```

### 3. 生成第一份周报

```bash
# 生成所有主题
/policy-weekly

# 或生成单个主题
/policy-weekly ai-policy
```

## 📖 使用指南

### 命令格式

```bash
# 生成所有三个主题的周报
/policy-weekly

# 生成指定主题的周报
/policy-weekly ai-policy
/policy-weekly internet-policy
/policy-weekly finance-policy

# 中文指令
生成本周政策周报
生成AI政策周报
```

### 输出文件

生成的周报保存在：

```
~/projects/research/
├── ai-policy/
│   └── AI政策周报_2026-W15.md
├── internet-policy/
│   └── 互联网监管周报_2026-W15.md
└── finance-policy/
    └── 投融资政策周报_2026-W15.md
```

### 周报结构

每份周报包含：

1. **本周核心关注** - 重大事件深度分析（1-2个）
2. **全球政策动态汇总** - 中国/美国/欧盟政策表格
3. **对本企业业务的影响评估** - 业务线影响矩阵
4. **下周关注重点** - 待发布政策、重要会议
5. **数据来源汇总** - 权威媒体链接 + 可信度评级

## ⚙️ 配置

### 搜索关键词自定义

你可以修改 `SKILL.md` 中的搜索关键词：

```bash
# AI 政策关键词
tvly search "AI 监管政策 大模型备案 算力出口管制" --topic news --time-range week

# 添加更多关键词
tvly search "生成式AI 监管 算法备案 网信办" --topic news --time-range week
```

### 报告模板自定义

修改 `SKILL.md` 中的报告模板，适配你的组织需求：

- 修改章节标题
- 添加组织特定的分析框架
- 自定义影响评估标准

### Obsidian 集成

如果你想使用 Obsidian 自动归档：

1. **安装 Obsidian Local REST API 插件**
   - 在 Obsidian 中安装 "Local REST API" 插件
   - 配置端口（默认 27124）

2. **配置 Claude Code MCP**

   创建或编辑 `~/.claude/settings.json`：

   ```json
   {
     "mcpServers": {
       "obsidian": {
         "command": "uvx",
         "args": ["mcp-obsidian"],
         "env": {
           "OBSIDIAN_API_KEY": "your-api-key",
           "OBSIDIAN_HOST": "127.0.0.1",
           "OBSIDIAN_PORT": "27124"
         }
       }
     }
   }
   ```

3. **设置环境变量**

   ```bash
   export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"
   ```

## 💰 API 配额消耗

```
每次搜索：1次 API 调用
生成所有主题：3次 API 调用/周
月度总计：12次 API 调用

对比日报模式：节省87%配额 ✅
```

### 缓存机制

相同的周数不会重复搜索：

```
~/projects/research/cache/
├── ai-policy/2026-W15.json
├── internet-policy/2026-W15.json
└── finance-policy/2026-W15.json
```

第二次生成同一周的周报时，会从缓存读取，**0次 API 调用**。

## 📂 目录结构

```
policy-weekly/
├── SKILL.md              # 主要逻辑和模板
├── README.md             # 使用文档（本文件）
├── INSTALL.md            # 详细安装指南
├── references/
│   ├── quick-reference.md # 快速参考
│   └── keywords.md       # 搜索关键词库
├── scripts/
│   └── cache-manager.py  # 缓存管理脚本（可选）
└── assets/
    └── logo.png          # Logo（可选）
```

## 🎯 使用场景

### 个人研究者

- 每周追踪 AI 政策动态
- 生成研究报告素材
- 建立政策知识库

### 企业战略团队

- 监测行业监管变化
- 评估政策对业务的影响
- 制定合规策略

### 投资机构

- 跟踪政策驱动的投资机会
- 评估政策风险
- 行业政策研究

## 🔧 高级用法

### 定时自动生成

使用 cron 定时任务：

```bash
# 编辑 crontab
crontab -e

# 每周日晚8点自动生成
0 20 * * 0 /usr/local/bin/claude-code /policy-weekly
```

### 批量生成历史周报

```python
import subprocess
from datetime import datetime, timedelta

def generate_historical_reports(start_week, end_week):
    for week in range(start_week, end_week + 1):
        subprocess.run([
            'claude-code',
            '/policy-weekly',
            '--week', f'2026-W{week:02d}'
        ])
```

### 集成到工作流

```yaml
# GitHub Actions example
name: Weekly Policy Report
on:
  schedule:
    - cron: '0 20 * * 0'  # Every Sunday 8pm

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Policy Weekly
        run: claude-code /policy-weekly
```

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 此仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 贡献方向

- 🔍 新增搜索关键词
- 📊 改进报告模板
- 🌍 支持更多地区政策
- 📈 添加数据分析功能
- 🔌 集成更多数据源

## 📝 更新日志

### v1.0.0 (2026-04-07)

- ✅ 初始版本发布
- ✅ 支持三大主题：AI政策、互联网监管、投融资政策
- ✅ 集成 Tavily Search
- ✅ 智能缓存机制
- ✅ Obsidian MCP 支持

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Tavily](https://tavily.com) - 提供高质量的新闻搜索 API
- [Claude Code](https://github.com/anthropics/claude-code) - AI 编程助手
- [Codeflicker](https://codeflicker.com) - AI 编程助手
- [Obsidian](https://obsidian.md) - 优秀的知识管理工具

## 📮 联系方式

- **问题反馈**: [GitHub Issues](https://github.com/gloria-oss/policy-weekly/issues)
- **功能建议**: [GitHub Discussions](https://github.com/gloria-oss/policy-weekly/discussions)

---

**如果这个 skill 对你有帮助，请给一个 ⭐ Star！**
