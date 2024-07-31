import sys
import time


def main():
    # 獲取命令行參數
    args = sys.argv[1:]

    print(f"Script1 接收到的參數：{args}")

    # 模擬一些處理時間
    time.sleep(2)

    # 在這裡添加您的主要邏輯，使用這些參數
    if len(args) == 1:
        print(f"Script1 處理單個參數: {args[0]}")
    elif len(args) == 2:
        print(f"Script1 處理兩個參數: {args[0]}, {args[1]}")
    else:
        print("Script1 錯誤：參數數量不正確")


if __name__ == "__main__":
    main()