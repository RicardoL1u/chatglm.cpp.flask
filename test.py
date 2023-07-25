
test = """
以下是波音737-300的一些数据：
    乘客容量：128-149名乘客
    飞行范围：4200公里。
    动力装置：2台CFM International CFM56-3系列涡扇发动机。
    机翼跨度：28.88米。
    飞机长度：33.40米。
    飞机高度：11.13米。
    最短起飞距离：1,500米。
    最大起飞重量：63,500公斤。
    最大着陆重量：58,600公斤。
    最大巡航速度：870公里/小时。
以下是松山机场的一些数据
    IATA代码：TSA
    ICAO代码：RCSS
    类型：公共
    位置：台湾台北市
    海拔：5.5米（18英尺）
    跑道：1号跑道长度为2,605米（8,547英尺），方向10/28；2号跑道长度为2,500米（8,202英尺），方向16/34
    时间区：UTC+8
    经度：121.552200
    纬度：25.069722

你可以参考的判断飞机是否能够起降的决策流程
1. 获取飞机的最短起飞距离
2. 获取机场的跑道长度
3. 判断飞机的最短起飞距离是否小于等于机场的跑道长度
4. 如果是，则飞机可以起降，否则飞机不能起降

问题：波音737-300能否在松山机场起降？
"""
import chatglm_cpp

pipline = chatglm_cpp.Pipeline("chatglm2-ggml.bin")
print(pipline.chat([test]))