import json
import shutil
import change_pdf
import img2pdf
import requests
import threading
import os
import time

# with open("book_info.txt", "r", encoding="utf_8") as f:
#     data = f.read()
id = input("请输入书籍的id：")
print("访问："+"https://lib-nuanxin.wqxuetang.com/v1/read/initread?bid="+id)
data = input("输入访问网址的json串：")
with open("book_info.txt", "w", encoding="utf_8") as f:
    f.write(data)
da = json.loads(data)

# 当前路径
getcmd = ""
# 图片存放路径
fold = ""
# 书籍的总页码
sum_book = 0
# 书籍的id
book_uid = 0
# 书籍的总URL
book_url = ""
# 线程数
thread_count = 30

title_name = ""


# 计算书籍总页码
def count_book():
    global title_name, book_uid
    # count_url = "https://lib-nuanxin.wqxuetang.com/v1/read/initread?bid=" + book_uid
    # text = requests.get(count_url).text
    # # print(text)
    # js = json.loads(text)

    book_uid = str(da["data"]["bid"])
    title_name = da["data"]["name"]
    count = da["data"]["pages"]
    print("书籍id：："+book_uid+"---"+"书籍名称："+title_name+"---"+"页数:"+count)
    return int(count)


# 分批下载图片
def load_img(count):
    # print(threading.current_thread())
    thread_page = int(sum_book/thread_count)
    l = thread_page * count+1
    if count == thread_count - 1:
        r = sum_book
    else:
        r = thread_page * (count+1)

    for page in range(l, r+1):
        url = book_url + str(page) + ".jpeg"

        local_path = fold + "/" + str(page)+".jpeg"
        if os.path.exists(local_path) and os.path.getsize(local_path) !=0:
            print("已存在"+str(page)+"页图片，跳过。。。")
            continue

        with open(local_path, "wb") as f:
            while 1:
                try:
                    content = requests.get(url).content
                    break
                except Exception:
                    print("访问出错。。重新访问")
                    time.sleep(1)

            f.write(content)
        print("第" + str(page) + "页正在下载完成。。。")
        time.sleep(0.1)


def init(book_id):
    global getcmd
    global fold, book_uid, book_url,sum_book
    book_uid = book_id
    getcmd = os.getcwd()
    fold = getcmd+"\\books\\IMG\\"
    fold = fold + book_uid
    # if os.path.exists(fold):
    #     shutil.rmtree(fold)
    #     time.sleep(0.1)
    if not os.path.exists(fold):
        os.mkdir(fold)
    book_url = "http://img.bookask.com/book/read/" + book_id+"/"
    sum_book = count_book()


def down_load():
    # print(fold)
    threading_list =[]
    for i in range(thread_count):
        t = threading.Thread(target=load_img, args=(i,))
        t.start()
        threading_list.append(t)

    for i in threading_list:
        i.join()


def do_imge_pdf():
    file = getcmd + "\\" + title_name+".pdf"
    with open(file, "wb") as f:
        lst = list()
        for i in range(1, sum_book+1):
            lst.append(fold+"\\"+str(i)+".jpeg")
        # 将有文件目录的列表数据转换为字节数据放入文件
        pdfy = img2pdf.convert(lst)
        print(title_name+" : 已成功转换为pdf")
        f.write(pdfy)


def to_pdf():
    do_imge_pdf()


if __name__ == "__main__":
    print("程序启动。。。")
    count_book()
    id = str(book_uid)
    init(id)
    # print(getcmd)
    down_load()
    print("图片下载完成！！")
    # to_pdf()
    change_pdf.run(id)

    # f = open("in.txt")
    # line = f.readline()
    # while line:
    #     print(line.strip("\n"))
    #
    #     print("书籍号："+line + "下载中，，，，")
    #     id = line
    #     init(id)
    #     # print(getcmd)
    #     down_load()
    #     to_pdf()
    #     line = f.readline()