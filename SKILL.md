---
name: policy-weekly
description: Generate weekly policy research reports for AI policy, internet regulation, and investment/financing topics. Use this skill whenever users mention policy research, weekly reports, regulatory updates, or want to generate structured analysis of recent policy developments in AI, internet, or investment domains. Supports both generating all three topics at once or specifying a single topic.
---

# Policy Research Weekly Report Generator

Generate structured weekly reports for three policy research domains: AI policy, internet regulation, and investment/financing policy.

## When to Use This Skill

Trigger this skill when users:
- Ask for weekly policy reports or updates
- Say "generate weekly report" or "policy weekly"
- Mention any of: AI policy, internet regulation, investment policy, regulatory updates
- Want to track policy changes in tech/finance sectors
- Need structured analysis of recent policy developments

**Example triggers:**
- "生成本周政策周报"
- "/policy-weekly"
- "Generate AI policy weekly report"
- "What happened in internet regulation this week?"

## Supported Topics

1. **ai-policy** - AI policy and regulations
   - Large model regulations (filing, approval)
   - Compute export controls
   - AI content copyright
   - AI ethics and safety

2. **internet-policy** - Internet and platform regulation
   - Short video/live streaming regulations
   - Data security, personal information protection
   - Antitrust enforcement
   - Competitor regulatory actions

3. **finance-policy** - Investment and financing policy
   - Macroeconomic financial policy
   - AI sector investment trends
   - Tax and subsidy policies
   - State-owned capital layout

## Configuration Required

### Step 1: Install Dependencies

Ensure you have:
- **tavily-search** skill installed
- **Obsidian MCP** configured (optional, for auto-filing)
- **Tavily API key**

### Step 2: Set Environment Variables

```bash
# Required: Your Tavily API key
export TAVILY_API_KEY="tvly-your-api-key-here"

# Optional: Your Obsidian vault path
export OBSIDIAN_VAULT_PATH="/path/to/your/vault"
```

### Step 3: Configure Save Location

Edit the `SAVE_BASE_PATH` variable in the workflow section below:

```markdown
Default: ~/projects/research/
Structure:
  ~/projects/research/
  ├── ai-policy/
  ├── internet-policy/
  └── finance-policy/
```

## Usage Patterns

### Generate All Weekly Reports
```
/policy-weekly
```
Or:
```
生成本周所有政策周报
```

### Generate Specific Topic
```
/policy-weekly ai-policy
```
Or:
```
生成AI政策周报
```

**Supported topics:**
- `ai-policy` - AI policy weekly report
- `internet-policy` - Internet regulation weekly report
- `finance-policy` - Investment policy weekly report

## Workflow

### Step 0: Pre-flight Check

**Before generating any report, check user configuration:**

1. **Check if TAVILY_API_KEY is set:**
   ```bash
   if [ -z "$TAVILY_API_KEY" ]; then
     echo "❌ TAVILY_API_KEY not found!"
     echo ""
     echo "Please set your Tavily API key:"
     echo "  export TAVILY_API_KEY=\"tvly-your-key-here\""
     echo ""
     echo "Get your API key at: https://tavily.com"
     exit 1
   fi
   ```

2. **Verify API key format:**
   ```bash
   if [[ ! "$TAVILY_API_KEY" =~ ^tvly- ]]; then
     echo "⚠️  Warning: TAVILY_API_KEY should start with 'tvly-'"
     echo "Current value: $TAVILY_API_KEY"
   fi
   ```

3. **Create necessary directories:**
   ```bash
   SAVE_BASE_PATH="${POLICY_REPORT_PATH:-$HOME/projects/research}"
   mkdir -p "$SAVE_BASE_PATH"/{ai-policy,internet-policy,finance-policy}
   mkdir -p "${POLICY_CACHE_PATH:-$HOME/policy-weekly/cache}"/{ai-policy,internet-policy,finance-policy}
   ```

**Important:** Never use hardcoded API keys. Always read from environment variables.

### Step 1: Determine Scope
- If no topic specified → generate all three reports
- If topic specified → generate only that topic
- Get current week number: `YYYY-Wnn` format

```bash
# Get current week
date +"%Y-W%V"
# Example: 2026-W15
```

### Step 2: Search for Policy News (Past 7 Days)

Use `tavily-search` skill with optimized keywords:

**AI Policy Keywords:**
```bash
tvly search "AI 监管政策 大模型备案 算力出口管制 LLM regulation" \
  --topic news --time-range week --max-results 15 --json
```

**Internet Regulation Keywords:**
```bash
tvly search "短视频监管 直播监管 平台治理 约谈 处罚" \
  --topic news --time-range week --max-results 15 --json

# Additional searches:
tvly search "内容审核 整改 数据安全" --topic news --time-range week
```

**Investment Policy Keywords:**
```bash
tvly search "投融资 AI融资 VC 创投 货币政策" \
  --topic news --time-range week --max-results 15 --json
```

### Step 3: Cache Search Results

Save to: `~/projects/research/cache/[topic]/YYYY-Wnn.json`

**Purpose:** Prevent duplicate API calls when regenerating reports

```python
cache_file = f"~/projects/research/cache/{topic}/{week}.json"

if os.path.exists(cache_file):
    data = load_cache(cache_file)
    # Use cached data
else:
    data = tvly_search(...)
    save_cache(cache_file, data)
    # Save for future use
```

### Step 4: Generate Structured Report

Use this template:

```markdown
---
category: 政策研究
topic: [AI政策/互联网监管/投融资政策]
date: YYYY-MM-DD
week: YYYY-Wnn
period: 周报
time_range: 过去7天
---

# [主题]周报 YYYY年第nn周

## 一、本周核心关注

### [🔴重大事件标题]
**事件概述**：
- [关键信息点1]
- [关键信息点2]
- 时间节点：YYYY-MM-DD

**深度分析**：
[背景、原因、影响]

**对本企业影响**：
| 影响维度 | 具体影响 | 紧迫度 |
|---------|---------|--------|
| [维度] | [具体内容] | 🔴/🟡/🟢 |

**行动建议**：
1. 短期（本周）
2. 中期（本月）
3. 长期（本季度）

**数据来源**：[链接](URL)

---

## 二、全球政策动态汇总

### 中国
| 政策/事件 | 发布机构 | 时间 | 影响评级 | 核心内容 |
|-----------|----------|------|----------|----------|
| ... | ... | ... | 🔴/🟡/🟢 | ... |

### 美国
[同上格式]

### 欧盟
[同上格式]

---

## 三、对本企业业务的影响评估

### 业务线影响矩阵
| 业务线 | 政策影响 | 风险等级 | 应对建议 |
|--------|----------|----------|----------|
| ... | ... | 🔴/🟡/🟢 | ... |

### 风险提示
#### 🔴 高风险
- [风险点]

#### 🟡 中风险
- [风险点]

---

## 四、下周关注重点

### 📋 待发布政策
- [预计下周发布的政策]

### 📅 重要会议
- [相关会议、听证会]

### ⏰ 关键时间节点
- [需要关注的截止日期]

---

## 五、数据来源汇总

### 本次搜索信息
- **搜索时间**：YYYY-MM-DD HH:MM
- **时间范围**：过去7天
- **API调用**：[次数]次
- **结果总数**：[数量]条
- **缓存文件**：`~/projects/research/cache/[topic]/YYYY-Wnn.json`

### 主要数据来源
1. **[媒体名称]** - [文章标题](链接)
   - 发布时间：YYYY-MM-DD
   - 主题：[主题]
   - 可信度：⭐⭐⭐⭐⭐ 权威

---

*生成时间：YYYY-MM-DD*
*生成工具：Claude Code + Tavily Search*
*主题：[主题]政策监测*
*周期：YYYY年第nn周*
```

### Step 5: Save Report

**Option A: Save to Obsidian** (requires MCP)

Use Obsidian MCP to create file:
- Filename: `[主题]周报_YYYY-Wnn.md`
- Location: `OBSIDIAN_VAULT_PATH/政策研究/[主题]/`

**Option B: Save to Local Filesystem** (default)

```bash
# Create directory structure
mkdir -p ~/projects/research/{ai-policy,internet-policy,finance-policy}

# Save report
SAVE_PATH="~/projects/research/[topic]/[topic]周报_YYYY-Wnn.md"
```

## Report Quality Standards

### ✅ Required Elements

1. **At least 1-2 major events** with deep analysis
2. **Global policy dynamics** summary table (China/US/EU)
3. **Specific impact assessment** for business lines
4. **Action recommendations** (short/medium/long term)
5. **Next week's focus areas**
6. **Complete data source links** with credibility ratings

### ✅ Data Quality Standards

- Use **authoritative sources**: Reuters, Bloomberg, Forbes, government agencies
- Mark **source credibility**: ⭐⭐⭐⭐⭐ (权威) / ⭐⭐⭐⭐ (专业) / ⭐⭐⭐ (一般)
- Include **publication date** for each source
- Prefer **sources from past 7 days**, mark if older

### ✅ Analysis Depth

- **Don't just list news** - analyze trends and impacts
- Provide **comparative analysis** (vs last week, vs same period last year)
- Include **quantitative data** when available
- Give **actionable recommendations**, not vague suggestions

## Cache Mechanism

### Purpose

Avoid duplicate API calls for the same time period.

### Location

```
~/projects/research/cache/
├── ai-policy/
│   ├── 2026-W14.json
│   └── 2026-W15.json
├── internet-policy/
│   └── 2026-W14.json
└── finance-policy/
    └── 2026-W14.json
```

### Implementation

```python
import os
import json
from datetime import datetime

def get_week_number():
    return datetime.now().strftime("%Y-W%V")

def load_cache(topic, week):
    cache_file = f"~/projects/research/cache/{topic}/{week}.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

def save_cache(topic, week, data):
    cache_file = f"~/projects/research/cache/{topic}/{week}.json"
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(data, f)
```

## Error Handling

### No News Found

If search returns no relevant results:
1. Note in report: "本周无重大政策动态（静默期）"
2. Still generate report with continued tracking items
3. Suggest broadening search scope next time

### API Issues

If tavily-search fails:
1. Check error message
2. If quota exceeded, inform user
3. If temporary error, retry once

### File System Issues

If save fails:
1. Save report to `/tmp` as fallback
2. Inform user of location
3. Suggest manual move

## Example Usage

**User:** "生成本周政策周报"

**You:**
1. Determine current week: 2026-W15
2. Search all three topics (past 7 days)
3. Cache results
4. Generate three structured reports
5. Save to configured location

**Output:**
```
✅ 已生成三份周报：
- AI政策周报_2026-W15.md → ~/projects/research/ai-policy/
- 互联网监管周报_2026-W15.md → ~/projects/research/internet-policy/
- 投融资政策周报_2026-W15.md → ~/projects/research/finance-policy/

📅 本周重大发现：
- AI政策：[根据实际搜索结果]
- 互联网监管：[根据实际搜索结果]
- 投融资：[根据实际搜索结果]

💰 API调用：3次 | 缓存已保存
```

## Customization

### Adjust Search Keywords

Edit the search keywords in Step 2 to match your specific needs:

```bash
# Example: Focus on specific regions
tvly search "美国 AI 监管政策 FTC" --topic news --time-range week

# Example: Focus on specific topics
tvly search "中国 算法推荐 监管 新规" --topic news --time-range week
```

### Adjust Report Template

Modify the template in Step 4 to match your organization's needs:
- Change section headers
- Add organization-specific analysis frameworks
- Customize impact assessment criteria

### Adjust Save Location

Change the base path:

```markdown
# Default
~/projects/research/

# Alternative examples
~/Documents/PolicyReports/
~/Obsidian/Vault/政策研究/
```

## Notes

- Always use **past 7 days** for search (not past month)
- Cache prevents **duplicate searches** for the same week
- Reports should be **comprehensive but readable** (20-30 min reading time)
- Focus on **actionable insights** for your business
- **Customize the template** to match your organization's needs
