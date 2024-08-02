car_models = """
Defender
Discovery
Discovery Sport
Freelander
Range Rover
Range Rover Evoque
Range Rover Evoque Coupe
Range Rover Sport
Range Rover Velar
"""

# 將多行字符串分割成列表，去除每行的空白字符
car_model_list = car_models.strip().split('\n')

# 格式化列表中的每個元素為帶引號的字符串
formatted_car_model_list = [f'"{model}"' for model in car_model_list]

# 將格式化後的列表元素用逗號和換行符號分隔
formatted_car_models = ",\n".join(formatted_car_model_list)

# 打印結果
print(formatted_car_models)