# GeoIP 规则集使用说明

本项目会自动从 MaxMind GeoIP 数据库生成 sing-box 格式的规则集文件。

## 规则集位置

生成的规则集文件位于 `release` 分支的 `sing-geoip/` 目录下：
- https://github.com/proother/rule_singbox_mihomo/tree/release/sing-geoip

## 生成方式

GeoIP 规则集现在作为统一工作流（unified.yml）的一部分自动生成：
- 与 Sing-box 规则和 Mihomo 规则并行构建
- 每日北京时间 20:00 自动更新
- 也可以通过 GitHub Actions 手动触发

## 文件格式

- 文件名格式：`geoip-{国家代码}.srs`
- 文件格式：sing-box 二进制规则集格式（SRS）
- 内容：包含该国家/地区的所有 IP CIDR 地址段

## 常用国家代码

- `cn` - 中国
- `us` - 美国
- `jp` - 日本
- `kr` - 韩国
- `sg` - 新加坡
- `hk` - 香港
- `tw` - 台湾

## 在 sing-box 中使用

### 1. 远程规则集（推荐）

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "geoip-cn",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/release/sing-geoip/geoip-cn.srs",
        "download_detour": "proxy"
      }
    ],
    "rules": [
      {
        "rule_set": "geoip-cn",
        "outbound": "direct"
      }
    ]
  }
}
```

### 2. 本地规则集

先下载规则集文件：
```bash
wget https://raw.githubusercontent.com/proother/rule_singbox_mihomo/release/sing-geoip/geoip-cn.srs
```

然后在配置中使用：
```json
{
  "route": {
    "rule_set": [
      {
        "tag": "geoip-cn",
        "type": "local",
        "format": "binary",
        "path": "./geoip-cn.srs"
      }
    ],
    "rules": [
      {
        "rule_set": "geoip-cn",
        "outbound": "direct"
      }
    ]
  }
}
```

## 更新频率

规则集每日自动更新（北京时间 20:00），也可以通过 GitHub Actions 手动触发更新。

## 数据来源

数据来源于 [Dreamacro/maxmind-geoip](https://github.com/Dreamacro/maxmind-geoip) 项目，该项目提供了免费的 MaxMind GeoIP 数据库。

## 下载方式

### GitHub Release
每次更新后会生成 `geoip-srs.zip` 包含所有国家的规则集文件，可从 [Releases](https://github.com/proother/rule_singbox_mihomo/releases) 页面下载。

### 直接访问
- GitHub Raw: `https://raw.githubusercontent.com/proother/rule_singbox_mihomo/release/sing-geoip/{文件名}`
- jsDelivr CDN: `https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/sing-geoip/{文件名}` 