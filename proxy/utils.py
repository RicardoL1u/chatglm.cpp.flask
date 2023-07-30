import random
import math
import datetime
import json
planes = json.load(open('refined_planes.json','r'))
airports = json.load(open('refined_airports.json','r'))
planes = {
    plane['name']:plane for plane in planes
}
airports = {
    airport['name']:airport for airport in airports
}

chinese_step_tags = ['第一步','第二步','第三步','第四步','第五步','第六步','第七步','第八步','第九步','第十步']

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
            'results':[
                '第一步: 获取飞机信息失败，无法继续推理',
            ]
        }
    else:
        ret.append('获取飞机信息成功，飞机名称为' + plane_name + '，飞机类型为' + plane_type + '，飞机起飞所需的最小跑道长度为' + str(plane_min_runway_length) + '米')
    
    if airport_name == None:
        ret.append('获取机场信息失败，无法继续推理')
        # add chinese step tags
        ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
        return {
            'success':True,
            'results':ret
        }
    else:
        ret.append('获取机场推理信息成功，机场名称为' + airport_name + '，机场最大跑道长度为' + str(airport_max_runway_length) + '米')

    
    # get now date in YYYY-MM-DD format
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # get month
    month = int(datetime.datetime.now().strftime('%m'))
    temperature = 30-6*abs(month - 6.5) + random.randint(-10,10)
    weather = None
    if temperature < 0:
        weather = random.choice(['小雪','中雪','大雪','暴雪'])
    else:
        weather = random.choice(['晴','多云','阴','小雨','中雨','大雨','暴雨'])
    

    
    ret.append('获取天气信息成功，天气为' + weather + '，日期为' + date + '，温度为' + str(temperature) + '摄氏度')
    
    
    
    if weather in ['大雨','暴雨','中雪','大雪','暴雪']:
        if plane_type == '直升机':
            ret.append('天气恶劣，飞机为直升机，直升机无法在'+weather+'天气起飞，推理结束')
            ret.append(f'{plane_name}无法在{weather}天气起飞，推理结束')
            # add chinese step tags
            ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
            return {
                'success':True,
                'results':ret
            }
        else:
            plane_min_runway_length = plane_min_runway_length * 1.5
            ret.append(f'天气恶劣，对于{plane_name}，飞机起飞所需的最小跑道长度增加0.5倍，最终为' + str(plane_min_runway_length) + '米')
    elif weather in ['小雨','中雨','小雪']:
        plane_min_runway_length = plane_min_runway_length * 1.2
        ret.append(f'天气稍劣，对于{plane_name}，飞机起飞所需的最小跑道长度增加0.2倍，最终为' + str(plane_min_runway_length) + '米')
    else:
        plane_min_runway_length = plane_min_runway_length * 0.8
        ret.append(f'天气良好，对于{plane_name}，飞机起飞所需的最小跑道长度减少0.2倍，最终为' + str(plane_min_runway_length) + '米')
        
    if plane_min_runway_length > airport_max_runway_length:
        ret.append(f'{plane_name}所需的最小跑道长度大于{airport_name}的最大跑道长度，{plane_name}无法在{airport_name}起飞，推理结束')
    else:
        ret.append(f'{plane_name}所需的最小跑道长度小于{airport_name}的最大跑道长度，{plane_name}可以在{airport_name}起飞，推理结束')
    
    # add chinese step tags
    ret = [chinese_step_tags[i] + ': ' + ret[i] for i in range(len(ret))]
    return {
        'success':True,
        'results':ret
    }

# existing missile

missile_names = ['DF-41','DF-17','民兵-3','白杨','和平护卫者']
target_with_hardness = [''] 
def getMissileEffect(entity_info:dict):
    for ent_name, ent_props in entity_info.items():
    
    return