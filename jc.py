import os.path
import sys
import time
from glob import glob
import autoit
import pyautogui

def open_app():
    while True:
        if not autoit.win_exists("金昌Ex9000 ---- 印花智能设计分色系统"):
            print('>> 未运行，先启动软件')
            autoit.run('Ex9000.exe')
            time.sleep(2)
            if autoit.win_exists("Dialog", text="下次起动显示"):
                autoit.control_click("Dialog", "[Class:Button; instance:2]")
                autoit.send('{ENTER}')
                time.sleep(2)
            if autoit.win_exists("Dialog", text="使用了其他版本"):
                autoit.send('{ENTER}')
                autoit.win_wait_active("Dialog", 3, text="智能修复后")
                autoit.send('{ENTER}')
                autoit.win_wait_active("Dialog", 3, text="系统修复完毕")
                autoit.send('{ENTER}')
                time.sleep(2)
                continue
            if autoit.win_exists("疑问", text="越权访问"):
                autoit.send('!N')
                time.sleep(1)
                autoit.process_close('Ex9000.exe')
                time.sleep(2)
                continue
                # pyautogui.alert(title='软件启动错误', text='请重新运行本软件')
                # sys.exit(0)
        autoit.win_set_state("金昌Ex9000 ---- 印花智能设计分色系统", autoit.properties.SW_SHOW)
        autoit.win_set_state("金昌Ex9000 ---- 印花智能设计分色系统", autoit.properties.SW_MAXIMIZE)
        # autoit.win_move("金昌Ex9000 ---- 印花智能设计分色系统", 0, 0, 800, 600)
        autoit.control_focus("金昌Ex9000 ---- 印花智能设计分色系统", "[Class:MDIClient; instance:1]")
        autoit.win_activate("金昌Ex9000 ---- 印花智能设计分色系统")
        autoit.win_wait_active("金昌Ex9000 ---- 印花智能设计分色系统", 3)
        print('>> 软件启动成功!')
        break

def open_jch(file_path):
    print('>> 打开文件：' + file_path)
    autoit.send("^w")
    time.sleep(0.5)
    autoit.send("^o")
    autoit.win_wait_active("打开文件", 5)
    autoit.control_send("打开文件", "[Class:Edit; instance:1]", file_path)
    autoit.send("{ENTER}")
    autoit.send("{ENTER}")
    autoit.win_wait_active("金昌Ex9000 ---- 印花智能设计分色系统", 5, text="标准工具条")
    print('>> 文件打开成功!')

def merge_jch():
    print('>> 合并图层')
    if autoit.win_exists("", text="混合模式"):
        text_mode = "混合模式"
    elif autoit.win_exists("", text="覆盖模式"):
        text_mode = "覆盖模式"
    else:
        text_mode = "图层"
        print('>> 调出图层')
        autoit.send("{F3}")
    print('>> 激活图层 => ' + text_mode)
    autoit.win_activate("", text=text_mode)
    time.sleep(1)
    autoit.control_click("", control="[Class:Button; instance:2]", text=text_mode)
    autoit.send("{down 6}")
    autoit.send("{ENTER}")
    print('>> 图层合并成功!')

def save_jch(file_path):
    print('>> 保存文件：' + file_path)
    autoit.send("^+s")
    autoit.win_wait_active("另存为", 5)
    autoit.control_send("另存为", "[Class:Edit; instance:1]", file_path)
    autoit.send("{ENTER}")
    autoit.send("{ENTER}")
    print('>> 文件保存成功!')

def close_app():
    autoit.win_close("金昌Ex9000 ---- 印花智能设计分色系统")
    print('>> 软件关闭成功!')




if __name__ == '__main__':
    input_dir_path = pyautogui.prompt(text="请输入JCH文件所在路径").strip()
    if input_dir_path is None:
        pyautogui.alert('欢迎下次使用!')
        sys.exit(0)
    print('>> input_dir_path: ' + input_dir_path)
    if not os.path.isdir(input_dir_path):
        pyautogui.alert('不是文件夹或路径不存在: ' + input_dir_path)
        sys.exit(0)

    output_dir_path = pyautogui.prompt(text="请确认(或修改)输出图片所在路径", default=os.path.join(input_dir_path, 'images')).strip()
    print('>> output_dir_path: ' + output_dir_path)
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    image_format = pyautogui.prompt(text="请确认(或修改)输出图片的格式\n支持bmp、jpg", default='bmp').strip()
    if image_format is None:
        pyautogui.alert('欢迎下次使用!')
        sys.exit(0)
    print('>> image_format: ' + image_format)

    jchs = glob(os.path.join(input_dir_path, '*.jch'))
    print(f">> 共搜索到{len(jchs)}个JCH文件")
    # print(jchs)

    confirm = pyautogui.confirm(title="即将开始转换", text=f"共搜索到{len(jchs)}个JCH文件\n运行过程中请不要动鼠标和键盘！！！", buttons=['OK', 'Cancel'])
    if confirm == 'Cancel':
        pyautogui.alert('欢迎下次使用!')
        sys.exit(0)


    try:
        open_app()
        for jch_file in jchs:
            # jch_file = jchs[0]  # only for test
            open_jch(jch_file)
            time.sleep(2)
            merge_jch()
            time.sleep(2)
            jch_name = jch_file.split(os.sep)[-1]
            output_file_path = os.path.join(output_dir_path, jch_name.split('.')[0] + '.' + image_format)
            save_jch(output_file_path)
        # wait for complete
        time.sleep(2)
        close_app()
        pyautogui.confirm(title='转换完成', text='欢迎下次使用!')
    except Exception as e:
        pyautogui.alert(title='脚本异常终止', text=str(e))
    input('>> 输入任意键退出...')

