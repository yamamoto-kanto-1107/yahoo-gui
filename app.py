from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv
import main
import os

# Comboboxの選択項目用リスト
cb_judge = [True, False]

# ウィンドウを作成
root = Tk()

# ウィンドウサイズを指定
root.geometry("320x240")

# ウィンドウタイトルを指定
root.title('入力フォーム')

frame1 = ttk.Frame(root, padding=(32))
frame1.grid()

# 開始行
label1 = ttk.Label(frame1, text='開始行', padding=(5, 2))
label1.grid(row=0, column=0, sticky=E)

# 取得行数
label2 = ttk.Label(frame1, text='取得行数', padding=(5, 2))
label2.grid(row=1, column=0, sticky=E)

# 電話番号
label3 = ttk.Label(frame1, text='電話番号', padding=(5, 2))
label3.grid(row=2, column=0, sticky=E)

# TestMode
label3 = ttk.Label(frame1, text='TestMode', padding=(5, 2))
label3.grid(row=3, column=0, sticky=E)

# 開始行
startRow = StringVar()
startRow_txt = ttk.Entry(
    frame1,
    textvariable=startRow,
    width=20)
startRow_txt.grid(row=0, column=1)

# 行数
RowContents = StringVar()
RowContents_txt = ttk.Entry(
    frame1,
    textvariable=RowContents,
    width=20)
RowContents_txt.grid(row=1, column=1)

# 電話番号
PhoneNumber = StringVar()
phone_txt = ttk.Entry(
    frame1,
    textvariable=PhoneNumber,
    width=20)
phone_txt.grid(row=2, column=1)

# Combobox
JudgeCombo = StringVar()
Judge_cb = ttk.Combobox(
    frame1,
    textvariable=JudgeCombo,
    values=cb_judge,
    width=20)
Judge_cb.bind('<<ComboboxSelected>>')
Judge_cb.grid(row=3, column=1)

def btn_click():
    # 値の取得
    start_value = int(startRow.get()) + 1  # ヘッダー分Add
    row_contents_value = int(RowContents.get()) - 1  # ヘッダー分Del
    judge_combo_value = str(JudgeCombo.get())

    print(judge_combo_value)
    add_value = start_value + row_contents_value

    phone_number_value = str(PhoneNumber.get())

    # CSVファイル読み込み
    with open('./syupin.csv') as f:
        reader = csv.reader(f)
        # 初期化
        output_arr = []

        # 指定した行から指定した行数分取得して配列に格納する
        for row, i in enumerate(reader, start=1):
            if start_value <= row <= add_value:
                output_arr.append(i)

        # 挿入の確認
        ret = messagebox.askquestion('質問', 'ヤフオクに出品しますか？')
        if ret:
            main.insertDataToYahoo(output_arr, judge_combo_value, phone_number_value,judge_combo_value)
        else:
            print('no')

# Button
button1 = ttk.Button(
    frame1, text='Insert',
    command=btn_click
)
button1.grid(row=4, column=1)

# ウィンドウ表示継続
root.mainloop()
