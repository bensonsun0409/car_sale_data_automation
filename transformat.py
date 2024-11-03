car_models = """
胎壓偵測  
動態穩定系統 
防盜系統 
keyless免鑰系統 
循跡系統 
中控鎖 
剎車輔助系統  
兒童安全椅固定裝置  
ABS防鎖死 
安全氣囊 
定速系統 
LED頭燈 
倒車顯影系統 
衛星導航 
多功能方向盤 
倒車雷達 
恆溫空調 
自動停車系統 
電動天窗 
真皮/皮革座椅
"""
city="""
南竿鄉、北竿鄉、莒光鄉、東引鄉
"""

# car_model_list = car_models.strip().split('\n')
city_list = city.strip().split('、')
# 格式化列表中的每個元素為帶引號的字符串
format_city=[f"{color}" for color in city_list]
# format_city_link=",".join(city_list)
print(format_city)
# # formatted_car_model_list = [f'"{model}"' for model in car_model_list]
# color_list = color.replace("'", "").strip().split('\n')

# 格式化列表中的每個元素為帶引號的字符串
# formatted_color = [f'"{color.strip()}"' for color in color_list if color.strip()]  # 檢查是否為空字符串

# 用逗號連接列表中的元素
# formatted_color_link = ",\n".join(formatted_color)

# 輸出結果
# print(formatted_color_link)
# # 將格式化後的列表元素用逗號和換行符號分隔
# formatted_car_models = ",\n".join(formatted_car_model_list)

# # 打印結果
# print(formatted_car_models)