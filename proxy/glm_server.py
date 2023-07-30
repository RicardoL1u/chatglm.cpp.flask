from flask import Flask, request
import requests
import random
import time
import datetime
from utils import airplaneTakeoffWithAirportAndWeather
app = Flask(__name__)
import logging
import os
ip_addr = os.environ.get('IP_ADDR')
if ip_addr is None:
    ip_addr = "192.168.27.145"
print(ip_addr)

import re

def extract_steps(text):
    # 使用正则表达式匹配“第x步”的模式，注意这里使用的是懒惰模式的量词
    pattern = r"(第[一二三四五六七八九十百千万亿]+步[:：].*?)(?=第[一二三四五六七八九十百千万亿]+步[:：]|$)"
    steps = re.findall(pattern, text, re.S)  # re.S 使 . 包括换行符在内的任意字符
    # 去除字符串最后的换行符
    steps = [step.strip() for step in steps]
    return steps

@app.route('/chat_reason', methods=['POST'])
def chat_reason():
    # get question
    question = request.json['question']
    print('recieved question is: ',question)
    # get decision
    decision = request.json['decision']
    print(decision)
    entity_info = request.json['entity_info']
    if '飞机起降' in decision:
        return airplaneTakeoffWithAirportAndWeather(entity_info)
        
    prompt = ''
    for ent_name,ent_props in entity_info.items():
        if 'entity_properties' not in ent_props.keys():
            continue
        ent_props = ent_props['entity_properties']
        prompt += ent_name + ': \n'
        for prop in ent_props:
            prompt += '\t' + str(prop['dpName']) + ': ' + str(prop['dpValue']) + '\n'
    prompt += '可能的思考角度：'+ decision.replace('决策','') + '\n'
    prompt += '请你基于以上信息，一步步思考，并给出中间过程，回答以下问题：' + question + '\n'

        
    print(prompt)

    
    url = "http://"+ip_addr+":8183/chat"
    # history = []
    response = requests.post(url, json={"prompt": prompt,"history":[]})
    rationale = response.json()['response']
    format_rationale = rationale
    # history.append(prompt)
    # history.append(rationale)
    # print(rationale)
    # format_rationale = requests.post(url, json={"prompt": "请你把你的推理过程，按照第一步，第二步，第三步...第N步的方式整理出来。","history":history})
    # format_rationale = format_rationale.json()['response']
    # if '第一步' not in format_rationale:
    #     print('retry: 1')
    #     format_rationale = requests.post(url, json={"prompt": "请你把你的推理过程，按照第一步，第二步，第三步...第N步的方式整理出来。","history":history})
    #     format_rationale = format_rationale.json()['response']
    # print(format_rationale)
    chinese_step_tags = ['第一步','第二步','第三步','第四步','第五步','第六步','第七步','第八步','第九步','第十步']
    steps = extract_steps(format_rationale)
    if len(steps) <= 2:
        steps = format_rationale.split('\n')
        steps = [tag+': '+step.strip() for tag, step in zip(chinese_step_tags,steps)]
    
    
    return {
        "success": True,
        "result": steps
    }
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# give me a curl test script
# curl -X POST -H "Content-Type: application/json" -d '{"question":"波音737-300能否在松山机场起降？"}' http://localhost:8080/chat_reason