import random
import math
import datetime
import json
from hashlib import md5
planes = json.load(open('refined_planes.json','r'))
airports = json.load(open('refined_airports.json','r'))
planes = {
    plane['name']:plane for plane in planes
}
airports = {
    airport['name']:airport for airport in airports
}

chinese_step_tags = [f'第{i}步' for i in range(1,101)]

def airplaneTakeoffWithAirportAndWeather(entity_info:dict):

    plane_name = None
    plane_min_runway_length = None
    plane_type = None
    airport_name = None
    airport_max_runway_length = None
    for ent_name in entity_info.keys():
        if ent_name in planes.keys():
            plane_name = ent_name
            plane_min_runway_length = planes[ent_name]['min_runway_length']
            plane_type = planes[ent_name]['type']
        if ent_name in airports.keys():
            airport_name = ent_name
            airport_max_runway_length = airports[ent_name]['max_runway_length']
    
    ret = []
    
    if plane_name == None:
        return {
            'success':True,
            'result':[
                '第一步: 获取飞机信息失败，无法继续推理',
            ]
        }
    else:
        ret.append('获取飞机信息成功，飞机名称为' + plane_name + '，飞机类型为' + plane_type + '，飞机起降所需的最小跑道长度为' + str(plane_min_runway_length) + '米')
    
    if airport_name == None:
        ret.append('获取机场信息失败，无法继续推理')
        # add chinese step tags
        ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
        return {
            'success':True,
            'result':ret
        }
    else:
        ret.append('获取机场推理信息成功，机场名称为' + airport_name + '，机场最大跑道长度为' + str(airport_max_runway_length) + '米')

    
    # get now date in YYYY-MM-DD format
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # get month
    month = int(datetime.datetime.now().strftime('%m'))
    random.seed(md5((airport_name+date).encode('utf-8')).hexdigest())
    temperature = 30-6*abs(month - 6.5) + random.randint(-10,10)
    weather = None
    if temperature < 0:
        weather = random.choice(['小雪','中雪','大雪','暴雪'])
    else:
        weather = random.choice(['晴','多云','阴','小雨','中雨','大雨','暴雨'])
    

    
    ret.append('获取基础天气信息成功，天气为' + weather + '，日期为' + date + '，温度为' + str(temperature) + '摄氏度')
    
    # get detail weather info
    wind_seed = random.randint(0,30)
    cloud_height = None
    precipitation = None
    if weather in ['晴','多云','阴']:
        precipitation = 0
        cloud_height = random.randint(4000,10000)
        visibility = random.randint(3000,5000)
    elif weather in ['小雨','中雨','大雨','小雪']:
        precipitation = random.randint(0,100)
        cloud_height = random.randint(1000,4000)
        visibility = random.randint(1000,3000)
    elif weather in ['暴雨', '中雪', '大雪', '暴雪']:
        precipitation = random.randint(100,300)
        cloud_height = random.randint(0,1000)
        visibility = random.randint(0,1000)
    
    ret.append('获取详细天气信息成功，风速为' + str(wind_seed) + '米/秒，能见度为' + str(visibility) + '米，云高为' + str(cloud_height) + '米，降水量为' + str(precipitation) + '毫米')
    
    if wind_seed < 25 and  visibility > 1800 and cloud_height > 2400 and precipitation < 200:
        ret.append('天气初步预检通过，整体满足起降条件，继续进针对{plane_name}的具体情况推理')
    else:
        weather_primary_check = '天气初步预检失败，'
        if wind_seed >= 25:
            weather_primary_check += '风速>25米/秒，风速过大，'
        if visibility <= 1800:
            weather_primary_check += '能见度<=1800米，能见度过低，'
        if cloud_height <= 2400:
            weather_primary_check += '云高<=2400米，云高过低，'
        if precipitation >= 200:
            weather_primary_check += '降水量>=200毫米，降水量过大，'
        ret.append(weather_primary_check + '天气初步预检失败，整体不满足起降条件，推理结束')
        ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
        return {
            'success':True,
            'result':ret
        }
    
    if weather in ['大雨','暴雨','中雪','大雪','暴雪']:
        if plane_type == '直升机':
            ret.append('天气恶劣，飞机为直升机，直升机无法在'+weather+'天气起降，推理结束')
            ret.append(f'{plane_name}无法在{weather}天气起降，推理结束')
            # add chinese step tags
            ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
            return {
                'success':True,
                'result':ret
            }
        else:
            plane_min_runway_length = plane_min_runway_length * 1.5
            ret.append(f'天气恶劣，对于{plane_name}，飞机起降所需的最小跑道长度增加0.5倍，最终为' + str(plane_min_runway_length) + '米')
    elif weather in ['小雨','中雨','小雪']:
        plane_min_runway_length = plane_min_runway_length * 1.2
        ret.append(f'天气稍劣，对于{plane_name}，飞机起降所需的最小跑道长度增加0.2倍，最终为' + str(plane_min_runway_length) + '米')
    else:
        plane_min_runway_length = plane_min_runway_length * 0.8
        ret.append(f'天气良好，对于{plane_name}，飞机起降所需的最小跑道长度减少0.2倍，最终为' + str(plane_min_runway_length) + '米')
        
    if plane_min_runway_length > airport_max_runway_length:
        ret.append(f'{plane_name}所需的最小跑道长度大于{airport_name}的最大跑道长度，{plane_name}无法在{airport_name}起降，推理结束')
    else:
        ret.append(f'{plane_name}所需的最小跑道长度小于{airport_name}的最大跑道长度，{plane_name}可以在{airport_name}起降，推理结束')
    
    # add chinese step tags
    ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
    return {
        'success':True,
        'result':ret
    }

# existing missile

missile_names = ['DF-41','DF-17','民兵-3','白杨','和平护卫者']
target_with_hardness = ['台北松山机场','横田空军基地','阿萨德空军基地'] 
def getMissileEffect(entity_info:dict):
    
    ret = []
    
    missile_data = {}
    target_data = {}
    for ent_name, ent_props in entity_info.items():
        ent_props = ent_props['entity_properties']
        if ent_name in missile_names:
            for prop in ent_props:
                missile_data[prop['dpName']] = prop['dpValue']
            break
        
        for prop in ent_props:
            target_data[prop['dpName']] = prop['dpValue']
    
    # if '射程' in missile_data:
    #     effective_range = missile_data['射程'] 
    #     ret.append(f'获取导弹射程成功，导弹射程为{missile_data["射程"]}公里')
    # else:
    #     return {
    #         'success':True,
    #         'result':[
    #             '第一步: 获取导弹射程失败，无法继续推理',
    #         ]
    #     }
    
    # if '数量' in missile_data:
    #     missile_exist_num = missile_data['数量']
    #     ret.append(f'获取导弹现存数量成功，导弹数量为{missile_data["数量"]}枚')
    # else:
    #     ret.append('获取导弹现存数量失败，无法继续推理')
    #     ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
    #     return {
    #         'success':True,
    #         'result':ret
    #     }
    
    if '当量' in missile_data:
        missile_equivalent = int(missile_data['当量'])
        ret.append(f'获取导弹当量成功，导弹当量为{missile_data["当量"]}吨')
    else:
        ret.append('获取导弹当量失败，无法继续推理')
        ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
        return {
            'success':True,
            'result':ret
        }
        
    if '分弹头数量' in missile_data:
        missile_warhead_num = int(missile_data['分弹头数量'])
        ret.append(f'获取导弹分弹头数量成功，导弹分弹头数量为{missile_data["分弹头数量"]}枚')
    else:
        ret.append('获取导弹分弹头数量失败，无法继续推理')
        ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
        return {
            'success':True,
            'result':ret
        }

    if '抗打击硬度' in target_data:
        target_hardness = int(target_data['抗打击硬度'])
        ret.append(f'获取目标抗打击硬度成功，目标抗打击硬度为{target_data["抗打击硬度"]}吨')
    else:
        target_hardness = 10
        ret.append('获取目标抗打击硬度失败，采用默认值10吨')
    
    unit_warhead_effect = round(missile_equivalent / missile_warhead_num, 2)
    ret.append(f'依据导弹当量和分弹头数量计算得到，每个分弹头的当量为{unit_warhead_effect}吨')
    
    strike_effect = round(unit_warhead_effect / target_hardness * 50, 2)
    ret.append(f'根据经验公式，将每个分弹头的当量除以目标抗打击硬度，再乘以50，得到每个分弹头对目标的打击效果为{strike_effect}个单位')
    
    function_effect = strike_effect * 1 # 机能
    ability_effect = strike_effect * 0.8 # 功能
    physical_effect = strike_effect * 0.6 # 物理
    # keep 2 decimal places
    function_effect = round(function_effect, 2)
    ability_effect = round(ability_effect, 2)
    physical_effect = round(physical_effect, 2)
    ret.append(f'根据经验公式，将每个分弹头的打击效果分别乘以1、0.8、0.6，得到每个分弹头对目标的机能、功能、物理效果分别为{function_effect}、{ability_effect}、{physical_effect}个单位')
            
    # if function_effect == 0 or ability_effect or 0 or physical_effect == 0:
    #     ret.append('由于机能、功能、物理效果均为0，所以最终打击效果分类为：无效，推理结束')
        
    # elif function_effect < 30 or ability_effect < 30 or physical_effect < 30:
    #     ret.append('由于机能、功能、物理效果均小于各自的轻度阈值 30、30、30，所以最终打击效果分类为：轻度，推理结束')

    # elif function_effect < 60 or ability_effect < 60 or physical_effect < 60:
    #     ret.append('由于机能、功能、物理效果均小于各自的中度阈值 60、60、60，所以最终打击效果分类为：中度，推理结束')

    # elif function_effect < 80 or ability_effect < 80 or physical_effect < 80:
    #     ret.append('由于机能、功能、物理效果均小于各自的重度阈值 80、80、80，所以最终打击效果分类为：重度，推理结束')
    # # function > 80 and ability > 80 and physical > 80 -> 毁灭性
    # elif function_effect > 80 or ability_effect > 80 or physical_effect > 80:
    #     ret.append('由于机能、功能、物理效果均大于各自的重度阈值 80、80、80，所以最终打击效果分类为：毁灭性，推理结束')
    
    
    def check_effect(effect, effect_name, level_list, ret):
        levels = ["无效", "轻度", "中度", "重度", "毁灭性"]
        for i, level in enumerate(level_list):
            if effect < level:
                ret.append(f'由于{effect_name}小于阈值 {level}，所以最终打击效果分类为：{levels[i]}，推理结束')
                return True
        return False

    effect_names = ['机能', '功能', '物理效果']
    effects = [function_effect, ability_effect, physical_effect]
    level_list = [0, 30, 60, 80, 100]

    ret = []
    for effect, effect_name in zip(effects, effect_names):
        if check_effect(effect, effect_name, level_list, ret):
            break
    else:
        ret.append('由于机能、功能、物理效果均大于各自的毁灭性阈值 80、80、80，所以最终打击效果分类为：毁灭性，推理结束')

    
    ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
    
    return {
        'success':True,
        'result':ret
    }