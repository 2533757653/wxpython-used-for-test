def write_record(name, xuehao, mark):
    record = f"姓名：{name}\n学号：{xuehao}\n得分：{mark}\n"

    try:
        with open("highest_scores.txt", "w") as file:
            file.write(record)
        print("记录已成功写入文件。")
    except Exception as e:
        print(f"写入记录时出错：{e}")

write_record("张明", "2300000001", 15)
