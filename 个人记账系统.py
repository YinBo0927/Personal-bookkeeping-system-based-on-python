from tkinter import *
from functools import *
from time import *
from pickle import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from ttkbootstrap import Style

# 一些初始化
ls = [['日期', '事项', '金额']]
pf = open("个人账本.txt", "ab")
dump(ls, pf)
pf.close()
item = ""
w1 = ""
kind = "支出"
cost = 0
t = ""
ls = []

# 主页面的构建
# 总页面构建
style = Style(theme="minty")
root = style.master
root.title('Bobo Save')
root.geometry('900x800')
root.resizable(width=False, height=False)


# 记账功能
def remind():
    # 按下记账按钮后记账界面的弹窗
    remind_subWindow = Toplevel(root)
    remind_subWindow.title("记账")
    remind_subWindow.geometry("400x300")
    remind_subWindow.resizable(width=False, height=False)

    # 保存时弹出的提示语
    def without(s):
        done = Toplevel(remind_subWindow)
        if s is None:
            temp = Label(done, text="保存完毕，请继续")
            temp.grid(row=0)
        else:
            temp = Label(done, text="请填写" + s)
            temp.grid(row=0)
        did = partial(done.destroy)
        but = Button(done, text="确定", command=did)
        but.grid(row=1)

    # 保存记账
    def save():
        global w1, item, kind
        w1 = str(item_entry.get())
        if w1 == "":
            without("事项")
            return
        wh = [item, w1]
        cost = str(money_entry.get())
        if cost == "":
            without("金额")
            return
        t1 = str(time_entry.get())
        if t1 != "":
            t = ""
            for i in t1:
                if '0' <= i <= '9':
                    t += i
                else:
                    t += " "
        else:
            t = strftime("%Y %m %d", localtime())
        if kind == "支出":
            cost = '-' + cost
        pf = open("个人账本.txt", "br")
        ls = load(pf)
        pf.close()
        ls.append([t, wh, cost])
        pf = open("个人账本.txt", "bw")
        dump(ls, pf)
        pf.close()
        item_entry.delete(0, "end")
        money_entry.delete(0, "end")
        time_entry.delete(0, "end")
        w1 = ""
        without(None)

    # 关闭窗口
    def close():
        remind_subWindow.destroy()

    # 窗口栏显示记账事项
    def do(what):
        global item
        item = what
        out = Label(remind_subWindow, text="事项：" + item)
        out.grid(row=0, column=0)
        if item in ["饮食", "娱乐", "购物", "学习", "其他"]:
            do_k('支出')
        elif item == '其他':
            do_k('收入')
        else:
            do_k('收入')

    # 窗口栏显示操作为支出或收入
    def do_k(what):
        global kind
        kind = what
        out_k = Label(remind_subWindow, text='操作类型:' + kind)
        out_k.grid(row=0, column=1)

    # 窗口栏显示当前日期
    def do_time():
        out_time = Label(remind_subWindow, text='默认日期：' + strftime("%Y %m %d"))
        out_time.grid(row=1, column=0)

    # 初始化窗口界面
    do('其他')
    do_k('支出')
    do_time()

    # 菜单栏
    menu_ = Menu(remind_subWindow)
    remind_subWindow.config(menu=menu_)  # 在记账功能的小窗上添加菜单栏

    # 菜单
    # 出账
    pay = Menu(remind_subWindow)
    alist = ["饮食", "娱乐", "购物", "学习", "其他"]
    for i in alist:
        if i == "其他":
            pay.add_separator()  # 添加分割线
        do1 = partial(do, i)
        pay.add_command(label=i, command=do1)
    menu_.add_cascade(label='支出', menu=pay)
    # 入账
    booked = Menu(remind_subWindow)
    alist1 = ["工资", "福利", "理财", "其他"]
    for n in alist1:
        if n == "其他":
            booked.add_separator()
        do1 = partial(do, n)
        booked.add_command(label=n, command=do1)
    menu_.add_cascade(label='收入', menu=booked)

    # 用户输入框的构建
    # 具体事项输入框
    item_label = Label(remind_subWindow, text="具体事项:")
    item_label.grid(row=2, column=0)
    item_entry = Entry(remind_subWindow)
    item_entry.grid(row=2, column=1)

    # 金额输入框
    money_label = Label(remind_subWindow, text="金额:")
    money_label.grid(row=3, column=0)
    money_entry = Entry(remind_subWindow)
    money_entry.grid(row=3, column=1)

    # 时间输入框
    time_label = Label(remind_subWindow, text="时间:")
    time_label.grid(row=4, column=0)
    time_entry = Entry(remind_subWindow)
    time_entry.grid(row=4, column=1)

    # 确认以及取消按钮
    block = Label(remind_subWindow, text=" ")
    block.grid(row=5)
    ok_button = Button(remind_subWindow, width=10, text="确认", command=save)  # command=ok
    ok_button.grid(row=6, column=0)
    block1 = Label(remind_subWindow, text=" ")
    block1.grid(row=6, column=1)
    cancel_button = Button(remind_subWindow, width=10, text="取消", command=close)  # command=cancel
    cancel_button.grid(row=6, column=2)

    remind_subWindow.mainloop()


# 查询功能
def inquire():
    # 按下查询按钮弹出的查询窗口
    inquire_subWindow = Toplevel(root)
    inquire_subWindow.title('查询')
    inquire_subWindow.geometry('400x300')
    inquire_subWindow.resizable(width=False, height=False)

    def close():
        inquire_subWindow.destroy()

    def find(s):  # 查找完成时的提示语
        if s == "":
            messagebox.showinfo("提示", "没有找到你要的内容。")
        else:
            give = Toplevel(inquire_subWindow)
            give.title("结果")

            def close():
                give.destroy()

            need = Message(give, text=s, width=230)
            need.grid()
            x = Button(give, text="确定", command=close)
            x.grid(row=2)

    def search():  # 查找符合条件的账目
        global w1, w, kind
        right = ""
        wh = True
        m = True
        tim = True

        w1 = str(g.get())
        if w1 == "":
            wh = False
        cost = str(money_entry.get())
        if cost == "":
            m = False
        t1 = str(time_entry.get())
        if t1 == "":
            tim = False
        else:
            t = ""
            for i in t1:
                if '0' <= i <= '9':
                    t += i
                else:
                    t += " "
            t1 = t
        if kind == "支出":
            cost = '-' + cost

        pf = open("个人账本.txt", "br")
        ls = load(pf)
        pf.close()

        while ls != [["日期", "事项", "金额"]]:
            flag = True
            temp = ls.pop()
            if tim and temp[0] != t1:
                flag = False
            if wh and temp[1][1] != w1:
                flag = False
            if w != temp[1][0]:
                flag = False
            if m and temp[2] != cost:
                flag = False
            if flag:
                right += temp[0] + '    ' + temp[1][0] + '-' + temp[1][1] + '    ' + temp[2] + '\n'

        g.delete(0, "end")
        money_entry.delete(0, "end")
        time_entry.delete(0, "end")
        w1 = ""
        find(right)

    def do(what):  # 设置事项
        global w
        w = what
        out = Label(inquire_subWindow, text="事项: " + w)
        out.grid(row=0, column=0)
        if w in "饮食娱乐购物学习其他":
            do_k("支出")
        elif w == "其他 ":
            do_k("收入")
        else:
            do_k("收入")

    def do_k(what):  # 设置操作
        global kind
        kind = what
        out_k = Label(inquire_subWindow, text="操作类型： " + kind)
        out_k.grid(row=0, column=1)

    do("其他")
    do_k("支出")

    # 菜单条
    menubar = Menu(inquire_subWindow)
    inquire_subWindow.config(menu=menubar)

    # 菜单
    m = Menu(inquire_subWindow)
    for i in ["饮食", "娱乐", "购物", "学习", "其他"]:
        if i == "其他":
            m.add_separator()  # 添加分割线
        do1 = partial(do, i)
        m.add_command(label=i, command=do1)
    menubar.add_cascade(label="支出", menu=m)
    out = Menu(inquire_subWindow)
    for i in ["工资", "福利", "理财", "其他 "]:
        if i == "其他 ":
            out.add_separator()  # 添加分割线
        do1 = partial(do, i)
        out.add_command(label=i, command=do1)
    menubar.add_cascade(label="收入", menu=out)

    l = Label(inquire_subWindow, text="请输入具体事项:")  # 提示语
    l.grid(row=2, column=0)
    g = Entry(inquire_subWindow)  # 文本框
    g.grid(row=2, column=1)

    money_label = Label(inquire_subWindow, text="请输入金额:")
    money_label.grid(row=3, column=0)
    money_entry = Entry(inquire_subWindow)
    money_entry.grid(row=3, column=1)

    time_label = Label(inquire_subWindow, text="请输入时间:")
    time_label.grid(row=4, column=0)
    time_entry = Entry(inquire_subWindow)
    time_entry.grid(row=4, column=1)

    block = Label(inquire_subWindow, text=" ")
    block.grid(row=5)
    ok_button = Button(inquire_subWindow, width=10, text="确认", command=search)
    ok_button.grid(row=6, column=0)
    block1 = Label(inquire_subWindow, text=" ")
    block1.grid(row=6, column=1)
    cancel_button = Button(inquire_subWindow, width=10, text="取消", command=close)
    cancel_button.grid(row=6, column=2)


# 生成报告
def report():
    def income():
        show = Toplevel(root)
        show.title("统计")
        show.resizable(width=False, height=False)

        f = Label(show, text="请输入开始时间:")
        f.grid(row=0, column=0)
        g_f = Entry(show)
        g_f.grid(row=0, column=1)
        t = Label(show, text="请输入结束时间:")
        t.grid(row=1, column=0)
        g_t = Entry(show)
        g_t.grid(row=1, column=1)

        def g():
            s_i = 0
            s_o = 0
            d = {}

            fro = g_f.get()
            to = g_t.get()
            if fro == "":
                messagebox.showinfo("提示", "请输入开始时间")
                return
            if to == "":
                messagebox.showinfo("提示", "请输入结束时间")
                return
            g_f.delete(0, "end")
            g_t.delete(0, 'end')

            pf = open("个人账本.txt", "br")
            ls = load(pf)
            pf.close()
            ls.pop(0)

            for i in ls:
                flag = True
                for j in range(10):
                    if not (fro[j] <= i[0][j] <= to[j]):
                        flag = False
                if flag:
                    if int(i[2]) < 0:
                        s_o += abs(int(i[2]))
                        if d.get(i[1][0] + "消费", 0):
                            d[i[1][0] + "消费"] += abs(int(i[2]))
                        else:
                            d[i[1][0] + "消费"] = abs(int(i[2]))
                    else:
                        s_i += int(i[2])
                        if d.get(i[1][0], 0):
                            d[i[1][0]] += int(i[2])
                        else:
                            d[i[1][0]] = int(i[2])
            ans = Toplevel(show)
            ans.title("结果")

            # 饼状图绘制
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure(figsize=(6, 6))
            label = ['工资', '福利', '理财', "其他"]
            explode = [0.01, 0.01, 0.01, 0.01]
            values = [d.get("工资", 0), d.get("福利", 0), d.get("理财", 0), d.get("其他", 0)]
            plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')
            plt.title('该时段收入情况\n'
                      '总收入：' + str(d.get("工资", 0) + d.get("福利", 0) + d.get("理财", 0) + d.get("其他", 0)))
            plt.show()

            ans.mainloop()
            return

        def close():
            show.destroy()

        ok_Button = Button(show, text="确定", command=g)
        cancel_Button = Button(show, text="取消", command=close)
        ok_Button.grid(row=2, column=0)
        cancel_Button.grid(row=2, column=1)

    def pay():
        show = Toplevel(root)
        show.title("统计")
        show.resizable(width=False, height=False)

        f = Label(show, text="请输入开始时间:")
        f.grid(row=0, column=0)
        g_f = Entry(show)
        g_f.grid(row=0, column=1)
        t = Label(show, text="请输入结束时间:")
        t.grid(row=1, column=0)
        g_t = Entry(show)
        g_t.grid(row=1, column=1)

        def g():
            s_i = 0
            s_o = 0
            d = {}

            fro = g_f.get()
            to = g_t.get()
            if fro == "":
                messagebox.showinfo("提示", "请输入开始时间")
                return
            if to == "":
                messagebox.showinfo("提示", "请输入结束时间")
                return
            g_f.delete(0, "end")
            g_t.delete(0, 'end')

            pf = open("个人账本.txt", "br")
            ls = load(pf)
            pf.close()
            ls.pop(0)

            for i in ls:
                flag = True
                for j in range(10):
                    if not (fro[j] <= i[0][j] <= to[j]):
                        flag = False
                if flag:
                    if int(i[2]) < 0:
                        s_o += abs(int(i[2]))
                        if d.get(i[1][0] + "消费", 0):
                            d[i[1][0] + "消费"] += abs(int(i[2]))
                        else:
                            d[i[1][0] + "消费"] = abs(int(i[2]))
                    else:
                        s_i += int(i[2])
                        if d.get(i[1][0], 0):
                            d[i[1][0]] += int(i[2])
                        else:
                            d[i[1][0]] = int(i[2])
            ans = Toplevel(show)
            ans.title("结果")
            # 饼状图绘制
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure(figsize=(6, 6))
            label = ['饮食消费', '学习消费', '购物消费', "其他消费"]
            explode = [0.01, 0.01, 0.01, 0.01]
            values = [d.get("饮食消费", 0), d.get("学习消费", 0), d.get("购物消费", 0), d.get("其他消费", 0)]
            plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')
            plt.title('该时段支出情况\n'
                      '总支出：' + str(d.get("饮食消费", 0) + d.get("学习消费", 0) + d.get("购物消费", 0) + d.get("其他消费", 0)))
            plt.show()
            ans.mainloop()
            return

        def close():
            show.destroy()

        ok_Button = Button(show, text="确定", command=g)
        cancel_Button = Button(show, text="取消", command=close)
        ok_Button.grid(row=2, column=0)
        cancel_Button.grid(row=2, column=1)

    report_subWindow = Toplevel(root)
    report_subWindow.title('生成报告')
    report_subWindow.geometry('400x300')
    report_subWindow.resizable(width=False, height=False)
    report_subWindow_button_booked = Button(report_subWindow, text="一键生成收入报告", font=30, command=income, height=2,
                                            width=20)
    report_subWindow_button_booked.place(x=100, y=50)
    report_subWindow_button_pay = Button(report_subWindow, text="一键生成支出报告", command=pay, font=30, height=2, width=20)
    report_subWindow_button_pay.place(x=100, y=120)


# 一键删除账单
def cancel():
    msg = messagebox.askyesno("提示", "要执行此操作吗")  # 让用户再次确认是否删除
    if msg:
        f = open("个人账本.txt", "bw")
        f.truncate()
        f.close()


# 按钮构建
remind_button = Button(root, height=2, width=10, text='添加', command=remind, font="幼圆")
remind_button.grid(row=0, column=0)
inquire_button = Button(root, height=2, width=10, text='查询', command=inquire, font="幼圆")
inquire_button.grid(row=0, column=1)
report_button = Button(root, height=2, width=10, text='生成报告', command=report, font="幼圆")
report_button.grid(row=0, column=2)
cancel_button = Button(root, height=2, width=10, text='清空账本', command=cancel, font="幼圆")
cancel_button.grid(row=0, column=3)

# 背景构建
backdrop = Canvas(root, width=800, height=850)
photo = PhotoImage(file='R-C_gif.gif')
picture = backdrop.create_image(500, 300, image=photo)
backdrop.grid(row=1, columnspan=4)

root.mainloop()
