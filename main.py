import os
import shutil
import subprocess

import colorama
from colorama import Fore


def check_admin():
    try:
        result = subprocess.run('net session', shell=True, capture_output=True)
        if result.returncode != 0:
            print(Fore.RED + "请以管理员身份运行此脚本!")
            input("按任意键退出...")
            exit(1)
    except Exception as e:
        print(Fore.RED + f"检查管理员权限时出错: {e}")
        input("按任意键退出...")
        exit(1)


def check_os_compatibility():
    try:
        result = subprocess.run('ver', shell=True, capture_output=True, text=True)
        if '5.1.' in result.stdout:
            print(Fore.YELLOW + "批处理可能对于Windows XP及其更早的操作系统兼容性存在问题")
            input("按任意键继续...")
    except Exception as e:
        print(Fore.RED + f"检查操作系统兼容性时出错: {e}")


def print_warnings():
    print(Fore.YELLOW + "**警告**")
    print("我们更推荐使用LittleSkin和MUA高校联盟等第三方认证方式代替离线登录解决该问题!")
    print("使用该批处理后可能会导致微软正版登录出现异常!")
    print("若您是正版用户(或有使用正版登录需求)请谨慎使用该批处理解决离线登录服务器消息问题!")
    print(Fore.YELLOW + "**注意**")
    print("安全软件可能会阻止批处理编辑hosts文件")
    print("若存在安全软件可以暂时关闭防护(或退出)")
    print("或出现防护提示时选择允许操作放行批处理")
    input("按任意键继续...")


def create_directories():
    data_dir = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'SakuraMaple', 'hosts_Backups')
    cache_dir = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'SakuraMaple', 'hosts_Backups')

    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            print(Fore.GREEN + f"已创建当前用户数据目录: {data_dir}")
        except PermissionError:
            print(Fore.RED + f"发生错误, 无法创建当前用户数据目录, 请检查权限问题!")
            input("按任意键退出...")
            exit(1)
    else:
        print(Fore.GREEN + f"当前用户数据目录已存在: {data_dir}")

    if not os.path.exists(cache_dir):
        try:
            os.makedirs(cache_dir)
            print(Fore.GREEN + f"已创建当前用户缓存目录: {cache_dir}")
        except PermissionError:
            print(Fore.RED + f"发生错误, 无法创建当前用户缓存目录, 请检查权限问题!")
            input("按任意键退出...")
            exit(1)
    else:
        print(Fore.GREEN + f"当前用户缓存目录已存在: {cache_dir}")


def check_hosts_file():
    hosts_path = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc', 'hosts')
    if not os.path.exists(hosts_path):
        try:
            open(hosts_path, 'w').close()
            print(Fore.GREEN + "已创建hosts文件")
        except PermissionError:
            print(Fore.RED + "发生错误, 无法创建hosts文件, 请检查是否以管理员身份运行或文件夹/文件拒绝访问, 如:存在安全软件阻止!")
            input("按任意键退出...")
            exit(1)
    else:
        print(Fore.GREEN + "hosts文件存在!")


def show_menu():
    print(Fore.CYAN + "==================================================")
    print("+ 键入a备份并写入(自动执行)(注:请勿重复执行!)")
    print("+ 键入o遍历 %windir%\System32\drivers\etc\下的文件")
    print("+ 键入p输出hosts文件内容")
    print("+ 键入t向hosts文件写入host信息(注:请勿重复执行!)")
    print("+ 键入b备份hosts文件")
    print("+ 键入r从最新的备份文件还原hosts文件")
    print("+ 键入c清空控制台(部分终端无效)")
    print("+ 键入x退出")
    print("==================================================")


def backup_hosts_file():
    hosts_path = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc', 'hosts')
    backup_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'SakuraMaple', 'hosts_Backups',
                               'host_last')
    try:
        shutil.copy2(hosts_path, backup_path)
        print(Fore.GREEN + "已备份hosts文件")
    except Exception as e:
        print(Fore.RED + f"备份hosts文件时出错: {e}")


def write_hosts_file():
    hosts_path = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc', 'hosts')
    lines = [
        "",
        "# Minecraft-Java-Edition-1-16-Series-Offline-Client-Send-Server-Message-Fix-Tool",
        "127.0.0.1 authserver.mojang.com",
        "127.0.0.1 api.mojang.com",
        "127.0.0.1 sessionserver.mojang.com",
        "127.0.0.1 api.minecraftservices.com",
        "::1 authserver.mojang.com",
        "::1 api.mojang.com",
        "::1 sessionserver.mojang.com",
        "::1 api.minecraftservices.com",
        "# ====================================================="
    ]
    with open(hosts_path, 'a', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
    print(Fore.GREEN + "已写入hosts文件")


def print_hosts_file():
    hosts_path = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc', 'hosts')
    try:
        with open(hosts_path, 'r', encoding='utf-8') as f:
            print(Fore.CYAN + "当前hosts文件内容:")
            print(f.read())
    except Exception as e:
        print(Fore.RED + f"读取hosts文件时出错: {e}")


def list_etc_directory():
    etc_dir = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc')
    try:
        print(Fore.CYAN + f"{etc_dir}下的文件:")
        for item in os.listdir(etc_dir):
            print(item)
    except Exception as e:
        print(Fore.RED + f"遍历目录时出错: {e}")


def restore_hosts_file():
    local_backup = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'SakuraMaple', 'hosts_Backups',
                                'host_last')
    roaming_backup = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'SakuraMaple', 'hosts_Backups',
                                  'host_last')
    hosts_path = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc', 'hosts')

    if os.path.exists(local_backup):
        recovery_file = 'Local'
    elif os.path.exists(roaming_backup):
        recovery_file = 'Roaming'
    else:
        print(Fore.RED + "没有找到hosts备份文件")
        while True:
            choice = input(
                "请尝试切换位置(键入 s ) 或手动放入文件到指定文件夹(键入 o 打开文件夹,实验性) 并命名为'hosts_last'(注:没有扩展名!)"
                "(注:打开文件夹功能仅支持有图形化的Windows或Windows Server操作系统), 键入 r 重新检测: "
            ).lower()
            if choice == 's':
                modify_recovery_location()
                return
            elif choice == 'o':
                try:
                    os.startfile(os.path.join(os.environ['USERPROFILE'], 'Roaming', 'Local', 'SakuraMaple',
                                              'hosts_Backups'))
                except Exception as e:
                    print(Fore.RED + f"打开文件夹时出错: {e}")
            elif choice == 'r':
                restore_hosts_file()
                return
            else:
                print(Fore.RED + "无效选择，请重新输入")
                continue

    recovery_text = '数据' if recovery_file == 'Local' else '缓存'
    while True:
        choice = input(f"是否要使用 {recovery_text} 的备份文件还原hosts?(不可逆!) 键入 Y 开始还原,键入 N 取消还原,键入 m 查看其它选项: ").lower()
        if choice == 'y':
            try:
                with open(local_backup if recovery_file == 'Local' else roaming_backup, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(hosts_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(Fore.GREEN + "已还原hosts文件")
                print_hosts_file()
                break
            except Exception as e:
                print(Fore.RED + f"还原hosts文件时出错: {e}")
        elif choice == 'n':
            break
        elif choice == 'm':
            modify_recovery_location()
            break
        else:
            print(Fore.RED + "无效选择，请重新输入")


def modify_recovery_location():
    print("当前使用的是{RecoveryText}的备份文件还原hosts")
    print("若要使用Local文件夹下的备份(默认备份),请键入 A")
    print("若要使用Roaming文件夹下的备份,请键入 R")
    while True:
        choice = input().lower()
        if choice == 'a':
            recovery_file = 'Local'
            break
        elif choice == 'r':
            recovery_file = 'Roaming'
            break
        else:
            print(Fore.RED + "无效选择，请重新输入")
    backup_path = os.path.join(os.environ['USERPROFILE'], 'AppData', recovery_file, 'SakuraMaple', 'hosts_Backups',
                               'host_last')
    if os.path.exists(backup_path):
        restore_hosts_file()
    else:
        print(Fore.RED + "hosts备份文件不存在，请重新选择或检查文件位置")


def clear_console():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(Fore.RED + f"清屏时出错: {e}")


def main():
    colorama.init()
    check_admin()
    check_os_compatibility()
    print_warnings()
    create_directories()
    check_hosts_file()

    while True:
        show_menu()
        choice = input("请输入选项: ").lower()
        if choice == 'a':
            backup_hosts_file()
            write_hosts_file()
        elif choice == 'o':
            list_etc_directory()
        elif choice == 'p':
            print_hosts_file()
        elif choice == 't':
            write_hosts_file()
        elif choice == 'b':
            backup_hosts_file()
        elif choice == 'r':
            restore_hosts_file()
        elif choice == 'c':
            clear_console()
        elif choice == 'x':
            break
        else:
            print(Fore.RED + "无效选择，请重新输入")


if __name__ == "__main__":
    main()
