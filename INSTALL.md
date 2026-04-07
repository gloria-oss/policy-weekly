# 安装指南

## 系统要求

- **操作系统**: macOS / Linux / Windows (WSL)
- **Python**: 3.8+ (可选，用于缓存管理脚本)
- **Claude Code**: 最新版本
- **Tavily API Key**: 必需

---

## 详细安装步骤

### 步骤 1: 安装 Claude Code CLI

如果你还没有安装 Claude Code：

```bash
# macOS/Linux
curl -fsSL https://claude.ai/code/install.sh | bash

# 验证安装
claude-code --version
```

### 步骤 2: 获取 Tavily API Key

1. 访问 [https://tavily.com](https://tavily.com)
2. 注册账号
3. 进入 Dashboard → API Keys
4. 创建新的 API Key
5. 复制你的 API Key（格式：`tvly-...`）

**免费配额**:
- 免费账户：1000次搜索/月
- 付费账户：根据套餐不同

### 步骤 3: 安装 tavily-search skill

通常 tavily-search 已经默认安装，如果没有：

```bash
# 检查是否已安装
ls ~/.claude/skills/tavily-search

# 如果未安装，手动安装
claude-code /install-skill tavily-search
```

### 步骤 4: 配置环境变量

**⚠️ 重要：必须配置你自己的 Tavily API Key**

Skill **不会使用其他人的 API key**，你必须在本地配置自己的 key：

**临时设置**（测试用）：

```bash
export TAVILY_API_KEY="tvly-your-actual-api-key-here"
```

**永久设置**（推荐）：

```bash
# 编辑配置文件
nano ~/.bashrc  # 或 ~/.zshrc

# 添加以下行
export TAVILY_API_KEY="tvly-your-actual-api-key-here"

# 保存并退出，然后重新加载
source ~/.bashrc  # 或 source ~/.zshrc
```

**验证配置**：

```bash
echo $TAVILY_API_KEY
# 应该输出你的 API Key（以 tvly- 开头）
```

**首次使用检查**：
- ✅ Skill 会在首次运行时检查 API key 是否已设置
- ✅ 如果未设置，会提示你如何配置并停止执行
- ✅ 确保你使用的是自己的 API key，不会产生混淆

### 步骤 5: 安装 policy-weekly skill

**方法 A: 从源码安装**

```bash
# 克隆仓库
git clone https://github.com/your-username/policy-weekly.git
cd policy-weekly

# 复制到 Claude Code skills 目录
cp -r . ~/.claude/skills/policy-weekly

# 验证安装
ls ~/.claude/skills/policy-weekly
```

**方法 B: 下载 ZIP 安装**

```bash
# 下载 ZIP 文件
wget https://github.com/your-username/policy-weekly/archive/refs/heads/main.zip

# 解压
unzip main.zip
cd policy-weekly-main

# 复制到 skills 目录
cp -r . ~/.claude/skills/policy-weekly
```

### 步骤 6: 创建必要的目录

```bash
# 创建报告保存目录
mkdir -p ~/projects/research/{ai-policy,internet-policy,finance-policy}

# 创建缓存目录
mkdir -p ~/projects/research/cache/{ai-policy,internet-policy,finance-policy}
```

### 步骤 7: 验证安装

```bash
# 重启 Claude Code
claude-code

# 测试 skill
/policy-weekly ai-policy
```

如果看到生成了 AI 政策周报，说明安装成功！

---

## Obsidian 集成（可选）

如果你想使用 Obsidian 自动归档功能，请按以下步骤操作：

### 步骤 1: 安装 Obsidian Local REST API 插件

1. 打开 Obsidian
2. 进入 Settings → Community plugins
3. 搜索 "Local REST API"
4. 安装并启用

### 步骤 2: 配置插件

1. 在 Obsidian Settings → Local REST API
2. 设置端口：`27124`（默认）
3. 启用 API
4. 复制 API Key

### 步骤 3: 配置 Claude Code MCP

创建或编辑 `~/.claude/settings.json`：

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "your-obsidian-api-key-here",
        "OBSIDIAN_HOST": "127.0.0.1",
        "OBSIDIAN_PORT": "27124"
      }
    }
  }
}
```

### 步骤 4: 设置 Obsidian 环境变量

```bash
# 设置 Obsidian vault 路径
export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"

# 永久设置
echo 'export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"' >> ~/.zshrc
source ~/.zshrc
```

### 步骤 5: 安装 Auto Move File 插件（可选）

自动将周报移动到对应文件夹：

1. 在 Obsidian 中安装 "Auto Move File" 插件
2. 配置规则：

```
topic: AI政策 → 政策研究/AI政策/
topic: 互联网监管 → 政策研究/互联网监管/
topic: 投融资政策 → 政策研究/投融资政策/
```

---

## 自定义配置

### 修改保存路径

默认保存到 `~/projects/research/`，你可以修改：

**方法 1: 环境变量**

```bash
# 设置报告保存路径
export POLICY_REPORT_PATH="/your/custom/path"

# 设置缓存路径（默认: ~/policy-weekly/cache）
export POLICY_CACHE_PATH="/your/custom/cache/path"
```

**方法 2: 修改 SKILL.md**

编辑 `~/.claude/skills/policy-weekly/SKILL.md`：

```markdown
### Step 5: Save Report

SAVE_BASE_PATH="${POLICY_REPORT_PATH:-~/projects/research}"
```

改为：

```markdown
SAVE_BASE_PATH="/your/custom/path"
```

### 修改搜索关键词

编辑 `~/.claude/skills/policy-weekly/SKILL.md`，找到搜索关键词部分：

```bash
# 当前关键词
tvly search "AI 监管政策 大模型备案 算力出口管制" --topic news --time-range week

# 改为你的关键词
tvly search "你的 关键词 列表" --topic news --time-range week
```

---

## 常见问题

### Q1: 提示 "TAVILY_API_KEY not found"

**原因**: 环境变量未设置或未生效

**解决**:
```bash
# 检查环境变量
echo $TAVILY_API_KEY

# 如果为空，重新设置
export TAVILY_API_KEY="tvly-your-key"
source ~/.zshrc
```

### Q2: 搜索返回空结果

**原因**: 
- API 配额用尽
- 网络问题
- 关键词不匹配

**解决**:
```bash
# 检查配额
tvly account

# 测试网络
curl -I https://api.tavily.com

# 尝试不同关键词
tvly search "AI policy" --topic news --time-range week
```

### Q3: Obsidian 归档不工作

**原因**: MCP 未配置或插件未启用

**解决**:
1. 检查 `~/.claude/settings.json` 是否正确
2. 确认 Obsidian Local REST API 插件已启用
3. 测试连接：
   ```bash
   curl http://127.0.0.1:27124/
   ```

### Q4: Skill 无法触发

**原因**: Claude Code 未识别 skill

**解决**:
```bash
# 检查 skill 是否存在
ls ~/.claude/skills/policy-weekly

# 重启 Claude Code
claude-code

# 使用完整路径触发
~/.claude/skills/policy-weekly/SKILL.md
```

### Q5: 缓存机制不工作

**原因**: 缓存目录权限问题

**解决**:
```bash
# 创建缓存目录
mkdir -p ~/projects/research/cache/{ai-policy,internet-policy,finance-policy}

# 检查权限
ls -la ~/projects/research/cache/
```

---

## 卸载

```bash
# 删除 skill
rm -rf ~/.claude/skills/policy-weekly

# 删除缓存和报告（可选）
rm -rf ~/projects/research/cache
rm -rf ~/projects/research/ai-policy
rm -rf ~/projects/research/internet-policy
rm -rf ~/projects/research/finance-policy

# 移除环境变量（可选）
# 编辑 ~/.bashrc 或 ~/.zshrc，删除相关 export 行
```

---

## 下一步

安装完成后：

1. ✅ 测试生成第一份周报：`/policy-weekly ai-policy`
2. ✅ 查看生成的报告，确认质量
3. ✅ 根据需要自定义关键词和模板
4. ✅ 配置定时任务（可选）
5. ✅ 集成到你的工作流

如有问题，请查看 [常见问题](#常见问题) 或提交 [Issue](https://github.com/your-username/policy-weekly/issues)。
