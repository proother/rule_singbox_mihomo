# README

本仓库会自动从 [@blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) 中每日**获取**并**转换**规则，生成适用于 sing-box 的 `json` 和 `srs` 格式，以及适用于 Mihomo 的 `yaml` 和`list`格式，并发布在[proother/rule_singbox_mihomo@release](https://github.com/proother/rule_singbox_mihomo/tree/release)。

### 背景

Mihomo 和 sing-box 官方提供的 `geosite` 和 `geoip` 整合了互联网社区整理的大部分域名和 IP 地址。为了提高程序的效率，他们会将一个服务的域名和 IP 分别拆分到两个文件中，但这使得普通用户在日常使用时难以维护。

本项目的目的是将这些服务提供商的域名、IP，甚至软件包名保存在同一个文件中，方便我们日常使用时对某个服务进行统一的分流管理。

两个内核的作者化繁为简，我们再次地化繁为简（bushi... 但大家的目标永远只有一个：

**Make Rules Great Again!**

### 引用

我们提供了三种 URL，您可以根据您的网络环境自行选择：

- GitHub Release：[https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/](https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/)
- jsDelivr：[https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/](https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/)
- jsDelivr-CF：[https://testingcf.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/](https://testingcf.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/)

您也可以使用类似 [https://ghproxy.cn/](https://ghproxy.cn/) 的前置加速服务。

### Mihomo 示例

由于 Mihomo 内核的二进制文件 `msr` 当前的behavior仅支持domain和ipcidr，而classical的 `yaml` 和 `text` 支持所有类型的路由规则，因此我们为Mihomo的rule-providers同时提供 `yaml` 和`list`文件格式。

相关文档：[https://wiki.metacubex.one/en/config/rule-providers/?h=classical](https://wiki.metacubex.one/en/config/rule-providers/?h=classical)

| 文件格式              | format写法                                                                                                                              |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| *.yaml        | yaml                                                 |
| *.list        | text                                                 |


```yaml
rule-providers:
  Apple_Classical:
    type: http
    path: ./ruleset/Apple_Classical.yaml
    url: "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/meta-rule/Apple_Classical.yaml"
    interval: 86400
    behavior: classical
    format: yaml
  Microsoft:
    type: http
    path: ./ruleset/Microsoft.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Microsoft.list"
    interval: 86400
    behavior: classical
    format: text
```


### sing-box 示例：

sing-box内核的二进制文件`srs`支持路由规则的全部类型，因此所有的sing-box的rule-set我们同时提供`srs`和`json`文件格式。

相关文档：[https://sing-box.sagernet.org/configuration/route/rule/](https://sing-box.sagernet.org/configuration/route/rule/)

| 文件格式              | format写法                                                                                                                              |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| *.srs        | binary                                                 |
| *.json       | source                                                 |


```json

 "rule_set": [
      {
        "type": "remote",
        "tag": "Apple_Classical",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Apple_Classical.srs"
      },
      {
        "type": "source",
        "tag": "Microsoft",
        "format": "source",
        "url": "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/sing-rule/Microsoft.json"
      }
    ]
```

## Mihomo懒人配置
```yaml

# Mihomo懒人配置
# 国外常用服务单独分流：YouTube，Netflix，Disney+，HBO，Spotify，Telegram，PayPal，Twitter，Facebook，Google，TikTok，GitHub，ChatGPT。
# 国内常用服务单独分流：苹果服务，微软服务，哔哩哔哩，网易云音乐，游戏平台，亚马逊，百度，豆瓣，微信，抖音，新浪，知乎，小红书。
rule-providers:
  Apple:
    type: http
    path: ./ruleset/Apple_Classical.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Apple_Classical.list"
    interval: 86400
    behavior: classical
    format: text
  BiliBili:
    type: http
    path: ./ruleset/BiliBili.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/BiliBili.list"
    interval: 86400
    behavior: classical
    format: text
  NetEaseMusic:
    type: http
    path: ./ruleset/NetEaseMusic.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/NetEaseMusic.list"
    interval: 86400
    behavior: classical
    format: text
  Baidu:
    type: http
    path: ./ruleset/Baidu.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Baidu.list"
    interval: 86400
    behavior: classical
    format: text
  DouBan:
    type: http
    path: ./ruleset/DouBan.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/DouBan.list"
    interval: 86400
    behavior: classical
    format: text
  WeChat:
    type: http
    path: ./ruleset/WeChat.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/WeChat.list"
    interval: 86400
    behavior: classical
    format: text
  DouYin:
    type: http
    path: ./ruleset/DouYin.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/DouYin.list"
    interval: 86400
    behavior: classical
    format: text
  Sina:
    type: http
    path: ./ruleset/Sina.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Sina.list"
    interval: 86400
    behavior: classical
    format: text
  Zhihu:
    type: http
    path: ./ruleset/Zhihu.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Zhihu.list"
    interval: 86400
    behavior: classical
    format: text
  XiaoHongShu:
    type: http
    path: ./ruleset/XiaoHongShu.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/XiaoHongShu.list"
    interval: 86400
    behavior: classical
    format: text
  YouTube:
    type: http
    path: ./ruleset/YouTube.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/YouTube.list"
    interval: 86400
    behavior: classical
    format: text
  Netflix:
    type: http
    path: ./ruleset/Netflix_Classical.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Netflix_Classical.list"
    interval: 86400
    behavior: classical
    format: text
  Disney:
    type: http
    path: ./ruleset/Disney.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Disney.list"
    interval: 86400
    behavior: classical
    format: text
  HBO:
    type: http
    path: ./ruleset/HBO.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/HBO.list"
    interval: 86400
    behavior: classical
    format: text
  Spotify:
    type: http
    path: ./ruleset/Spotify.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Spotify.list"
    interval: 86400
    behavior: classical
    format: text
  Telegram:
    type: http
    path: ./ruleset/Telegram.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Telegram.list"
    interval: 86400
    behavior: classical
    format: text
  PayPal:
    type: http
    path: ./ruleset/PayPal.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/PayPal.list"
    interval: 86400
    behavior: classical
    format: text
  Twitter:
    type: http
    path: ./ruleset/Twitter.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Twitter.list"
    interval: 86400
    behavior: classical
    format: text
  Facebook:
    type: http
    path: ./ruleset/Facebook.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Facebook.list"
    interval: 86400
    behavior: classical
    format: text
  Amazon:
    type: http
    path: ./ruleset/Amazon.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Amazon.list"
    interval: 86400
    behavior: classical
    format: text
  OpenAI:
    type: http
    path: ./ruleset/OpenAI.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/OpenAI.list"
    interval: 86400
    behavior: classical
    format: text
  Sony:
    type: http
    path: ./ruleset/Sony.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Sony.list"
    interval: 86400
    behavior: classical
    format: text
  Nintendo:
    type: http
    path: ./ruleset/Nintendo.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Nintendo.list"
    interval: 86400
    behavior: classical
    format: text
  Epic:
    type: http
    path: ./ruleset/Epic.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Epic.list"
    interval: 86400
    behavior: classical
    format: text
  SteamCN:
    type: http
    path: ./ruleset/SteamCN.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/SteamCN.list"
    interval: 86400
    behavior: classical
    format: text
  Steam:
    type: http
    path: ./ruleset/Steam.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Steam.list"
    interval: 86400
    behavior: classical
    format: text
  Game:
    type: http
    path: ./ruleset/Game.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Game.list"
    interval: 86400
    behavior: classical
    format: text
  GitHub:
    type: http
    path: ./ruleset/GitHub.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/GitHub.list"
    interval: 86400
    behavior: classical
    format: text
  Microsoft:
    type: http
    path: ./ruleset/Microsoft.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Microsoft.list"
    interval: 86400
    behavior: classical
    format: text
  Google:
    type: http
    path: ./ruleset/Google.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Google.list"
    interval: 86400
    behavior: classical
    format: text
  TikTok:
    type: http
    path: ./ruleset/TikTok.list
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/TikTok.list"
    interval: 86400
    behavior: classical
    format: text
rules:
  #RULE-SET 规则
  - RULE-SET,Apple,DIRECT
  - RULE-SET,BiliBili,DIRECT
  - RULE-SET,NetEaseMusic,DIRECT
  - RULE-SET,Baidu,DIRECT
  - RULE-SET,DouBan,DIRECT
  - RULE-SET,WeChat,DIRECT
  - RULE-SET,DouYin,DIRECT
  - RULE-SET,Sina,DIRECT
  - RULE-SET,Zhihu,DIRECT
  - RULE-SET,XiaoHongShu,DIRECT
  - RULE-SET,Microsoft,DIRECT
  - RULE-SET,Sony,DIRECT
  - RULE-SET,Nintendo,DIRECT
  - RULE-SET,Epic,DIRECT
  - RULE-SET,SteamCN,DIRECT
  - RULE-SET,YouTube,PROXY
  - RULE-SET,Netflix,PROXY
  - RULE-SET,Disney,PROXY
  - RULE-SET,HBO,PROXY
  - RULE-SET,Spotify,PROXY
  - RULE-SET,Telegram,PROXY
  - RULE-SET,PayPal,PROXY
  - RULE-SET,Twitter,PROXY
  - RULE-SET,Facebook,PROXY
  - RULE-SET,Amazon,PROXY
  - RULE-SET,OpenAI,PROXY
  - RULE-SET,Steam,PROXY
  - RULE-SET,Game,PROXY
  - RULE-SET,GitHub,PROXY
  - RULE-SET,Google,PROXY
  - RULE-SET,TikTok,PROXY

  #GEOSITE 规则，来自官方geosite.db,建议保留
  - GEOSITE,geolocation-!cn,PROXY
  - GEOSITE,cn,DIRECT

  #GEOIP 规则，来自官方geoip.db,建议保留
  - GEOIP,private,DIRECT,no-resolve
  - GEOIP,CN,DIRECT
  - DST-PORT,80/8080/443/8443,PROXY
  #MATCH 匹配所有请求用来兜底,建议保留
  - MATCH,DIRECT
```

## sing-box懒人配置
```json

{
// sing-box懒人配置
// 国外常用服务单独分流：YouTube，Netflix，Disney+，HBO，Spotify，Telegram，PayPal，Twitter，Facebook，Google，TikTok，GitHub，ChatGPT。
// 国内常用服务单独分流：苹果服务，微软服务，哔哩哔哩，网易云音乐，游戏平台，亚马逊，百度，豆瓣，微信，抖音，新浪，知乎，小红书。
// 食用之前，请删掉本配置里的所有注释，不然无法使用。
  "route": {
    "auto_detect_interface": true,
    "rule_set": [
      {
        "type": "remote",
        "tag": "Apple",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Apple_Classical.srs"
      },
      {
        "type": "remote",
        "tag": "BiliBili",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/BiliBili.srs"
      },
      {
        "type": "remote",
        "tag": "NetEaseMusic",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/NetEaseMusic.srs"
      },
      {
        "type": "remote",
        "tag": "Baidu",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Baidu.srs"
      },
      {
        "type": "remote",
        "tag": "DouBan",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/DouBan.srs"
      },
      {
        "type": "remote",
        "tag": "WeChat",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/WeChat.srs"
      },
      {
        "type": "remote",
        "tag": "DouYin",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/DouYin.srs"
      },
      {
        "type": "remote",
        "tag": "Sina",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Sina.srs"
      },
      {
        "type": "remote",
        "tag": "Zhihu",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Zhihu.srs"
      },
      {
        "type": "remote",
        "tag": "XiaoHongShu",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/XiaoHongShu.srs"
      },
      {
        "type": "remote",
        "tag": "YouTube",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/YouTube.srs"
      },
      {
        "type": "remote",
        "tag": "Netflix",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Netflix_Classical.srs"
      },
      {
        "type": "remote",
        "tag": "Disney",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Disney.srs"
      },
      {
        "type": "remote",
        "tag": "HBO",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/HBO.srs"
      },
      {
        "type": "remote",
        "tag": "Spotify",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Spotify.srs"
      },
      {
        "type": "remote",
        "tag": "Telegram",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Telegram.srs"
      },
      {
        "type": "remote",
        "tag": "PayPal",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/PayPal.srs"
      },
      {
        "type": "remote",
        "tag": "Twitter",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Twitter.srs"
      },
      {
        "type": "remote",
        "tag": "Facebook",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Facebook.srs"
      },
      {
        "type": "remote",
        "tag": "Amazon",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Amazon.srs"
      },
      {
        "type": "remote",
        "tag": "OpenAI",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/OpenAI.srs"
      },
      {
        "type": "remote",
        "tag": "Sony",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Sony.srs"
      },
      {
        "type": "remote",
        "tag": "Nintendo",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Nintendo.srs"
      },
      {
        "type": "remote",
        "tag": "Epic",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Epic.srs"
      },
      {
        "type": "remote",
        "tag": "SteamCN",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/SteamCN.srs"
      },
      {
        "type": "remote",
        "tag": "Steam",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Steam.srs"
      },
      {
        "type": "remote",
        "tag": "Game",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Game.srs"
      },
      {
        "type": "remote",
        "tag": "GitHub",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/GitHub.srs"
      },
      {
        "type": "remote",
        "tag": "Microsoft",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Microsoft.srs"
      },
      {
        "type": "remote",
        "tag": "Google",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/Google.srs"
      },
      {
        "type": "remote",
        "tag": "TikTok",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/proother/rule_singbox_mihomo/refs/heads/release/sing-rule/TikTok.srs"
      },
// 官方geoip geosite 建议保留
      {
        "format": "binary",
        "tag": "geoip-cn",
        "type": "remote",
        "url": "https://cdn.jsdelivr.net/gh/SagerNet/sing-geoip@rule-set/geoip-cn.srs"
      },
      {
        "format": "binary",
        "tag": "geosite-geolocation-cn",
        "type": "remote",
        "url": "https://cdn.jsdelivr.net/gh/SagerNet/sing-geosite@rule-set/geosite-geolocation-cn.srs"
      },
      {
        "format": "binary",
        "tag": "geosite-geolocation-!cn",
        "type": "remote",
        "url": "https://cdn.jsdelivr.net/gh/SagerNet/sing-geosite@rule-set/geosite-geolocation-!cn.srs"
      }
    ],
    "rules": [
      {
        "type": "logical",
        "mode": "or",
        "rules": [
          {
            "protocol": "dns"
          },
          {
            "port": 53
          }
        ],
        "outbound": "dns-out"
      },
      {
        "ip_is_private": true,
        "outbound": "direct"
      },
      {
        "clash_mode": "Direct",
        "outbound": "direct"
      },
      {
        "clash_mode": "Global",
// 请将oubound 配置为你的代理服务器
        "outbound": "Proxy"
      },
      {
        "type": "logical",
        "mode": "or",
        "rules": [
          {
            "port": 853
          },
          {
            "network": "udp",
            "port": 443
          },
          {
            "protocol": "stun"
          }
        ],
        "outbound": "block"
      },
      {
        "outbound": "direct",
        "rule_set": [
          "Apple",
          "BiliBili",
          "NetEaseMusic",
          "Baidu",
          "DouBan",
          "WeChat",
          "DouYin",
          "Sina",
          "Zhihu",
          "XiaoHongShu",
          "Microsoft",
          "Sony",
          "Nintendo",
          "Epic",
          "SteamCN",
          "geoip-cn",
          "geosite-geolocation-cn"
        ]
      },
      {
        "rule_set": [
          "YouTube",
          "Netflix",
          "Disney",
          "HBO",
          "Spotify",
          "Telegram",
          "PayPal",
          "Twitter",
          "Facebook",
          "Amazon",
          "OpenAI",
          "Steam",
          "Game",
          "GitHub",
          "Google",
          "TikTok",
          "geosite-geolocation-!cn"
        ],
// 请将oubound 配置为你的代理服务器
        "outbound": "Proxy"
      }
    ]
  }
}
```
