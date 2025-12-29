def log_in():
    print("---登录---\n")
    print("1.学生登录\n")
    print("2.教室登录\n")
    print("3.激活账号\n")
    choice = input("请选择: ")

    match choice:
        case 1:
            print("登录")
        case 2:
            print("注册")
        case 3:
            print("退出")
        case _:
            print("无效选择")

def action():