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
鹽埕區、鼓山區、左營區、楠梓區、三民區、新興區、前金區、苓雅區、前鎮區、旗津區、小港區、鳳山區、林園區、大寮區、大樹區、大社區、仁武區、鳥松區、岡山區、橋頭區、燕巢區、田寮區、阿蓮區、路竹區、湖內區、茄萣區、永安區、彌陀區、梓官區、旗山區、美濃區、六龜區、甲仙區、杉林區、內門區、茂林區、桃源區、那瑪夏區"""
# 將多行字符串分割成列表，去除每行的空白字符
car_model_list = car_models.strip().split('\n')
city_list = city.strip().split('、')
# 格式化列表中的每個元素為帶引號的字符串
format_city=[f'"{city}"' for city in city_list]
format_city_link=",\n".join(format_city)
print(format_city_link)
# formatted_car_model_list = [f'"{model}"' for model in car_model_list]

# # 將格式化後的列表元素用逗號和換行符號分隔
# formatted_car_models = ",\n".join(formatted_car_model_list)

# # 打印結果
# print(formatted_car_models)