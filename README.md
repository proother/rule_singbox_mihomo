Mihomo内核的二进制文件`msr`目前`behavior`仅支持 `domain`/`ipcidr`，`classical`的`yaml`和`text`支持路由规则的全部类型，因此所有的Mihomo的rule-providers我们都采用`yaml`格式。

Mihomo的引用方法：
```yaml
rule-providers:
  Apple_Classical:
    type: http
    path: ./ruleset/Apple_Classical.yaml
    url: "https://github.com/proother/rule_singbox_mihomo/raw/refs/heads/release/meta-rule/Apple_Classical.yaml"
    interval: 86400
    behavior: classical
    format: yaml
  Microsoft:
    type: http
    path: ./ruleset/Microsoft.yaml
    url: "https://cdn.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/Microsoft.yaml"
    interval: 86400
    behavior: classical
    format: yaml
  OpenAI:
    type: http
    path: ./ruleset/OpenAI.yaml
    url: "https://testingcf.jsdelivr.net/gh/proother/rule_singbox_mihomo@release/meta-rule/OpenAI.yaml"
    interval: 86400
    behavior: classical
    format: yaml
```

sing-box内核的二进制文件`srs`支持路由规则的全部类型，因此所有的sing-box的rule-set我们同时提供`srs`和`json`文件格式。

sing-box的引用方法：

```json

 "rule_set": [
      {
        "type": "remote",
        "tag": "Apple_Classical",
        "format": "binary",
        "url": "https://github.com/proother/rule_singbox_mihomo/raw/refs/heads/release/sing-rule/Apple_Classical.srs"
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
