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
