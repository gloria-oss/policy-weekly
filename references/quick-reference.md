# Policy Weekly - Quick Reference

## 常用命令

### 生成周报
```bash
# 生成所有主题
/policy-weekly

# 生成单个主题
/policy-weekly ai-policy
/policy-weekly internet-policy
/policy-weekly finance-policy

# 中文指令
生成本周政策周报
生成AI政策周报
```

### 检查环境
```bash
# 检查 Tavily API Key
echo $TAVILY_API_KEY

# 检查保存路径
echo $POLICY_REPORT_PATH

# 检查缓存路径
echo $POLICY_CACHE_PATH

# 检查 Obsidian 路径（可选）
echo $OBSIDIAN_VAULT_PATH
```

### 管理缓存
```bash
# 查看缓存大小
du -sh ~/projects/research/cache/

# 清理旧缓存（保留最近4周）
find ~/projects/research/cache/ -name "*.json" -mtime +28 -delete

# 清空所有缓存
rm -rf ~/projects/research/cache/*/
```

---

## 输出文件位置

```
~/projects/research/
├── ai-policy/
│   └── AI政策周报_YYYY-Wnn.md
├── internet-policy/
│   └── 互联网监管周报_YYYY-Wnn.md
└── finance-policy/
    └── 投融资政策周报_YYYY-Wnn.md
```

---

## 搜索关键词

### AI 政策
```
AI 监管政策
大模型备案
算力出口管制
生成式AI 管理
算法推荐 监管
```

### 互联网监管
```
短视频监管
直播监管
平台治理
约谈 处罚
数据安全
内容审核
未成年人保护
```

### 投融资政策
```
投融资 AI融资
VC 创投
货币政策
AI 投资
数据中心 融资
```

---

## 报告结构

每份周报包含：

1. **本周核心关注** (1-2个重大事件)
   - 事件概述
   - 深度分析
   - 影响评估
   - 行动建议

2. **全球政策动态汇总**
   - 中国政策表格
   - 美国政策表格
   - 欧盟政策表格

3. **对本企业业务的影响评估**
   - 业务线影响矩阵
   - 风险提示（高/中）

4. **下周关注重点**
   - 待发布政策
   - 重要会议
   - 关键时间节点

5. **数据来源汇总**
   - 权威媒体链接
   - 发布时间
   - 可信度评级

---

## API 配额消耗

```
单次搜索：1次 API 调用
生成所有主题：3次/周
月度总计：12次
年度总计：156次

对比日报：节省87% ✅
```

### 配额查询
```bash
tvly account
```

---

## 常见问题

**Q: 如何修改保存路径？**
A: 设置环境变量 `POLICY_REPORT_PATH`

**Q: 如何禁用缓存？**
A: 删除 `~/projects/research/cache/` 目录

**Q: 如何使用 Obsidian 归档？**
A: 参考 `INSTALL.md` 的 Obsidian 集成章节

**Q: 如何自定义关键词？**
A: 编辑 `SKILL.md` 中的搜索关键词部分

---

## 高级用法

### 定时任务
```bash
# 每周日晚8点自动生成
0 20 * * 0 /usr/local/bin/claude-code /policy-weekly
```

### 批量生成历史周报
```bash
# 生成最近4周的周报
for week in 12 13 14 15; do
  claude-code "/policy-weekly --week 2026-W$week"
done
```

---

**更多详情请查看完整 README.md**
