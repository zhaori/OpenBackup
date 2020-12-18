"""
文件系统监听守护模块
"""
import os
import subprocess
from tkinter import Tk, Button, Label
from config.Main_config import tk_title, logo, windll
from threading import Thread
import win32api
import win32con
import win32gui
import win32gui_struct


class SysTrayIcon(object):
    '''SysTrayIcon类用于显示任务栏图标'''
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 5320

    def __init__(self, icon, on_quit, tk_window=None, default_menu_index=None,
                 window_class_name=None):
        '''
        icon         需要显示的图标文件路径
        hover_text   鼠标停留在图标上方时显示的文字
        menu_options 右键菜单，格式: (('a', None, callback), ('b', None, (('b1', None, callback),)))
        on_quit      传递退出函数，在执行退出时一并运行
        tk_window    传递Tk窗口，self.root，用于单击图标显示窗口
        default_menu_index 不显示的右键菜单序号
        window_class_name  窗口类名
        '''
        self.hwnd = None
        self.icon = icon
        # s.hover_text = hover_text
        self.on_quit = on_quit
        self.root = tk_window

        # menu_options = menu_options + (('退出', None, s.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        # s.menu_options = s._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id

        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER + 20: self.notify, }
        # 注册窗口类。
        window_class = win32gui.WNDCLASS()
        window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # 也可以指定wndproc.
        self.classAtom = win32gui.RegisterClass(window_class)
        self.update()

    def update(self):
        '''显示任务栏图标，不用每次都重新创建新的托盘图标'''
        # 创建窗口。
        hinst = win32gui.GetModuleHandle(None)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()

        win32gui.PumpMessages()

    def _add_ids_to_menu_options(s, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in s.SPECIAL_ACTIONS:
                s.menu_actions_by_id.add((s._next_action_id, option_action))
                result.append(menu_option + (s._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               s._add_ids_to_menu_options(option_action),
                               s._next_action_id))
            s._next_action_id += 1
        return result

    def refresh_icon(self):
        # 尝试找到自定义图标
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:  # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER + 20,
                          hicon,
                          )
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

    def destroy(self, hwnd=None, msg=None, wparam=None, lparam=None, exit=1):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # 终止应用程序。
        if exit and self.on_quit:
            self.on_quit()  # 需要传递自身过去时用 self.on_quit(self)
        else:
            self.root.deiconify()  # 显示tk窗口

    def notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass
        elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起
            self.destroy(exit=0)
        return True

    def show_menu(self):
        menu_options = None
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, menu_options)

        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # 加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def execute_menu_option(self, id):
        menu_action = self.menu_actions_by_id[id]
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        else:
            menu_action(self)

    # Main = _Main()
    # Main.main()


class manage_listen(object):

    def __init__(self):
        self.pid = "listen_service.exe"

    def start(self):
        """
        启动进程
        """
        os.system(self.pid)

    def stop(self):
        """
        强行停止进程
        """
        return subprocess.Popen("taskkill /F /im {}".format(self.pid), shell=True, stdout=subprocess.PIPE) \
            .stdout.readlines()

    def find(self):
        """
        查找指定进程
        """
        return subprocess.Popen('tasklist | find "{}"'.format(self.pid), shell=True, stdout=subprocess.PIPE) \
            .stdout.readlines()


def start_watch():
    def start():
        manage_listen().start()

    t = Thread(target=start)
    t.start()

    # p.close()
    # time.sleep(2)


class Show_Window(object):
    def __init__(self):
        self.width = 250
        self.height = 90
        self.win = Tk()
        self.SysTrayIcon = None
        self.win.title(tk_title)
        self.win.iconbitmap(logo)
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')
        screenwidth = self.win.winfo_screenwidth()
        screenheight = self.win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.win.geometry(aligner)

    @staticmethod
    def _start():
        start_watch()

    @staticmethod
    def _stop():
        manage_listen().stop()

    def exit(self, _sysTrayIcon=None):
        """
        窗口退出
        """
        self.win.destroy()
        print('exit...')

    def Hidden_window(self, icon=logo):
        """
        隐藏窗口至托盘区，调用SysTrayIcon的重要函数
        """
        self.win.withdraw()  # 隐藏tk窗口
        if self.SysTrayIcon:
            self.SysTrayIcon.update()  # 已经有托盘图标时调用 update 来更新显示托盘图标
        else:
            self.SysTrayIcon = SysTrayIcon(icon,  # 图标
                                           on_quit=self.exit,  # 退出调用
                                           tk_window=self.win,  # Tk窗口
                                           )

    def show(self):
        self.win.bind("<Unmap>",
                      lambda event: self.Hidden_window() if self.win.state() == 'iconic' else False)
        Label(self.win, text='文件系统监听守护', font=("黑体", "12")).place(relx=0.23, rely=0.1, width=140, height=40)
        Button(self.win, text='启动', command=self._start).place(relx=0.1, rely=0.6, width=80, height=30)
        Button(self.win, text='停止', command=self._stop).place(relx=0.56, rely=0.6, width=80, height=30)
        self.win.mainloop()


if __name__ == '__main__':
    Show_Window().show()
