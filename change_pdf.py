#!/usr/bin/python3
# -*- coding: UTF-8 -*- 

from utils import *
from wqxtDownloader import *;

# 初始化全局变量
globalvar_init();
# 初始化urllib
initUrllibNoCookies();
# 初始化logging


def run(bid):
	# usage: python3 change_pdf.py <book_id> <start> <end>
	loggingLevel("INFO");
	LSArg = len(sys.argv);
	if LSArg == 1:
		# bid = input("请输入需要下载的bid：");
		book = wqxtDownloader(bid);
		book.start();
	else:
		bid = sys.argv[1];
		book = wqxtDownloader( bid );
		book.start( *(int(x) for x in sys.argv[2:]) );


if __name__ == "__main__":
	kid = input("输入书籍id:")
	run(kid)

