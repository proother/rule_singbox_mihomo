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

由于 Mihomo 内核的二进制文件 `msr` 当前的 `behavior` 仅支持 `domain` 和 `ipcidr`，而classical的 `yaml` 和 `text` 支持所有类型的路由规则，因此我们为 Mihomo 的rule-providers）同时提供 `yaml` 和`list`文件格式。

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
  OpenAI:
    type: http
    path: ./ruleset/OpenAI.list
    url: "https://testingcf.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/OpenAI.list"
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
      },
      {
        "type": "remote",
        "tag": "OpenAI",
        "format": "binary",
        "url": "https://testingcf.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/sing-rule/OpenAI.srs"
      }
    ]
```
