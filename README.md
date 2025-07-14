# Rule Singbox Mihomo

自动生成适用于 **sing-box** 和 **Mihomo** 的规则集，每日更新。

## ✨ 特色功能

### 🎯 sing-box 规则 (更新：使用 Python 脚本方式)
- **Python 脚本生成**: 使用修改版的 senshinya/singbox_ruleset 方式
- **平铺目录结构**: 所有规则文件在同一目录，便于管理
- **完整版**: 支持所有规则类型（~15k规则）
- **精简版 (Lite)**: 仅包含 IP-CIDR + DOMAIN + DOMAIN-SUFFIX，体积小90%，加载飞快
- **双格式支持**: 
  - `.json` - 人类可读，方便调试
  - `.srs` - 二进制格式，性能最优

### 🛡️ Mihomo 规则
- **三种格式任选**（~30k规则）：
  - `.yaml` - 标准格式，兼容性最好
  - `.list` - 纯文本格式，加载更快
  - `.mrs` - 二进制格式，性能最优（仅支持纯domain/ipcidr规则）

### 🌍 GeoIP 规则
- **MaxMind 数据源**: 基于 Dreamacro/maxmind-geoip 项目
- **200+ 国家/地区**: 完整的全球 IP 地址段数据
- **sing-box 专用**: SRS 二进制格式，加载速度快
- **文件命名**: `geoip-{国家代码}.srs`（如 geoip-cn.srs）

## 📦 下载使用

### 方式一：下载ZIP包（推荐）
访问 [最新Release](../../releases/latest) 下载打包好的规则集：

| 文件名 | 说明 | 适用场景 |
|--------|------|----------|
| **sing-box 规则** |
| `sing-rules-json.zip` | 完整版JSON格式 | 需要查看/编辑规则 |
| `sing-rules-srs.zip` | 完整版SRS二进制 | 追求性能 |
| `sing-rules-lite-json.zip` | 精简版JSON格式 | 低配设备 |
| `sing-rules-lite-srs.zip` | 精简版SRS二进制 | 路由器/嵌入式设备 |
| **Mihomo 规则** |
| `meta-rules-yaml.zip` | YAML格式 | 标准用法 |
| `meta-rules-list.zip` | LIST纯文本格式 | 快速加载 |
| `meta-rules-mrs.zip` | MRS二进制格式 | 极致性能 |
| **GeoIP 规则** |
| `sing-box-geoip-srs.zip` | IP地址段规则集 | 按国家分流 |

### 方式二：CDN直链（在线更新）

```bash
# GitHub Raw（稳定但可能被墙）
https://raw.githubusercontent.com/proother/rule_singbox_mihomo/release/{规则文件}

# jsDelivr CDN（国内加速）
https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/{规则文件}
```

示例：
- Sing-box: `https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/sing-rule/apple.srs`
- Mihomo: `https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/apple.yaml`

## 📝 配置示例

### Sing-box 配置
```json
{
  "route": {
    "rule_set": [{
      "tag": "cn",
        "type": "remote",
      "format": "binary",
      "url": "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/sing-rule/apple.srs",
      "download_detour": "direct"
    }],
    "rules": [{
      "rule_set": "cn",
        "outbound": "direct"
    }]
  }
}
```

### Mihomo 配置
```yaml
rule-providers:
  cn:
    type: http
    behavior: domain
    format: yaml  # 可选: yaml/list/mrs
    url: https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/apple.yaml
    interval: 86400

rules:
  - RULE-SET,cn,DIRECT
```

### GeoIP 配置（Sing-box）
```json
{
  "route": {
    "rule_set": [{
      "tag": "geoip-cn",
      "type": "remote",
      "format": "binary",
      "url": "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/sing-geoip/geoip-cn.srs"
    }],
    "rules": [{
      "rule_set": "geoip-cn",
      "outbound": "direct"
    }]
  }
}
```

## 🔄 更新机制

- **更新时间**: 每日北京时间 20:00（UTC 12:00）
- **更新方式**: GitHub Actions 自动构建
- **缓存刷新**: 自动清理 jsDelivr CDN 缓存

## 📊 数据来源

| 规则集 | 数据源 | 规则数量 |
|--------|--------|----------|
| **Sing-box** | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | ~15,000 |
| **Mihomo** | 多源整合：GFWList + China Domains + v2fly社区 | ~30,000 |
| **GeoIP** | [Dreamacro/maxmind-geoip](https://github.com/Dreamacro/maxmind-geoip) | 200+ 国家/地区 |

> 注意：Sing-box 规则生成时会跳过 IP-ASN 规则，仅包含 DOMAIN、DOMAIN-SUFFIX、DOMAIN-KEYWORD、IP-CIDR 和 PROCESS-NAME 规则。

## 🏗️ 技术架构

```mermaid
graph LR
    A["GitHub Actions
    北京时间 20:00"] --> B["并行Job 1
    Sing-box规则生成
    (Python脚本)"]
    A --> C["并行Job 2
    Mihomo规则生成"]
    A --> D["并行Job 3
    GeoIP规则生成"]
    B --> E[上传Artifacts]
    C --> E
    D --> E
    E --> F["发布Job
    整合打包"]
    F --> G["GitHub Release
    ZIP包下载"]
    F --> H["Git Push
    release分支"]
    F --> I["CDN刷新
    jsDelivr"]
```

### 核心优势
- **并行构建**: Sing-box、Mihomo 和 GeoIP 同时生成，效率提升3倍
- **Python 脚本**: Sing-box 使用 Python 脚本处理，更灵活
- **官方工具**: Mihomo 使用 MetaCubeX 官方 meta-rules-converter
- **智能去重**: 自动去除冗余规则，优化体积
- **多格式输出**: 满足不同性能和兼容性需求

## 📈 性能对比

| 格式 | 体积 | 加载速度 | 内存占用 | 兼容性 |
|------|------|----------|----------|--------|
| JSON/YAML | 大 | 慢 | 高 | ⭐⭐⭐⭐⭐ |
| LIST | 中 | 快 | 中 | ⭐⭐⭐⭐ |
| SRS/MRS | 小 | 极快 | 低 | ⭐⭐⭐ |

## 🤝 贡献

欢迎提交 Issue 或 PR！

## 📄 许可证

MIT License


