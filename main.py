from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
import enchant
import re
import requests

def translate(query):
    url = 'http://fanyi.youdao.com/translate'
    data = {
        "i": query,  # 待翻译的字符串
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "16081210430989",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION"
    }
    res = requests.post(url, data=data).json()
    
    len_of_translated = len(res['translateResult'][0])
    
    translated_text = ''
    for i in range(len_of_translated): # 翻译结果有多个，通过循环拼接全部翻译结果
        translated_text = translated_text + res['translateResult'][0][i]['tgt']
        
    return translated_text

## functions
d = enchant.Dict("en_US")
# 检测是否是合法单词
def legal_str(str):
    if (str==''): return True
    return d.check(str)
    

# check function
def check(str):
    
    str = str.strip() # 去除str首尾空格
    
    if (str.find('-')): # 对包含-的字符串判断
        if (legal_str(str)):
            return True
        else :
            return False
        
# delete_slash function
def delete_slash(str):
    
    str = str.strip() # 去除str首尾空格
    
    cnt = 0
    
    # 从前往后删除连字符，直到legal_str返回true 或者删除5次后自动返回
    tmp_str = re.sub(r'[^\w\s-]','',str) # 去除str中的标点符号
    while(legal_str(tmp_str)==False and cnt !=5):
        
        cnt = cnt + 1
        
        # print(tmp_str)
        len_of_str = len(str)
        for i in range(len_of_str):
            if (str[i] == '-'):
                str = list(str)
                str[i] = ''
                str = ''.join(str)
                break;
        tmp_str = re.sub(r'[^\w\s-]','',str) # 去除str中的标点符号
    
    return str
    
# delete ori function
def delete_fun():
    
    ori_text = form.oriText.toPlainText() # 获取原文
    
    print("ori:", ori_text)
    
    str_split = str(ori_text).split()
    
    print("ori_split:", str_split)
    
    # check and delete
    len_of_str = len(str_split)
    
    for i in range(len_of_str):
        if (check(str_split[i]) == False):
            str_split[i] = delete_slash(str_split[i]) # delete 
            
    print("delete_split", str_split)
    
    str_merge = list(str_split)
    str_merge = ' '.join(str_merge)
    
    form.deletedOri.setPlainText(str_merge)    
    
    
## translate into chinese

def translate_fun():
    
    # 自动执行自动删除再翻译
    delete_fun()
    
    ori_text = form.deletedOri.toPlainText() # 获取修改好的原文
    translated_text = translate(ori_text)
    
    form.translatedText.setPlainText(translated_text)    


if __name__=='__main__':
    
    Form, Window = uic.loadUiType("dialog.ui")

    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)

    form.deleteButton.clicked.connect(delete_fun) # 按钮联动
    form.translateButton.clicked.connect(translate_fun) # 按钮联动
    print(dir(form))
    # print(dir(form.oriText))

    window.show()
    app.exec()