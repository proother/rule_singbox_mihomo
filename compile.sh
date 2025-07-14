#!/bin/bash

# 设置基础目录
base_dir="rule"

# 遍历 rule 文件夹下的所有 JSON 文件
for json_file in "$base_dir"/*.json; do
    # 检查文件是否存在
    if [[ -f "$json_file" ]]; then
        # 获取文件名（不含路径和扩展名）
        filename=$(basename "$json_file" .json)
        
        # 构建输出文件名 (与 JSON 相同，用 .srs 结尾)
        output_file="$base_dir/$filename.srs"
        
        # 执行 sing-box 命令
        sing-box rule-set compile --output "$output_file" "$json_file"
        
        # 输出处理信息
        echo "Processed: $json_file -> $output_file"
    fi
done