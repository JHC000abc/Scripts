# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: convert_reqs_to_toml.py
@time: 2025/7/14 00:32 
@desc: 

"""
import json
import sys

import toml

project = {}
with open("pyproject.toml", "r") as f:
    for i in f.readlines():
        line = i.strip().split(" = ")
        if len(line) == 2:
            key, value = line
            project.update({
                key: value.strip('"')
            })
            if key == "dependencies" and value.strip('"') != "[]":
                print("已存在 dependencies")
                sys.exit()

# 读取 requirements-locked.txt
with open("requirements-locked.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and '==' in line]
project["dependencies"] = requirements
# 构建 pyproject.toml 结构
pyproject = {
    "project": project
}
pyproject = json.loads(json.dumps(pyproject, indent=4, ensure_ascii=False))

# 写入 pyproject.toml
with open("pyproject.toml", "w") as f:
    toml.dump(pyproject, f)

print("转换完成！")
