# encoding: utf-8
# ******************************************************
# Author       : zzw922cn
# Last modified: 2018-01-10 11:00
# Email        : zzw922cn@gmail.com
# Filename     : processDigit.py
# Description  : Converting digit into Chinese character 
#                according to its pronunciation
# ******************************************************

import re
import os

def replaceDecimal(decimal_set, sub_str):
    ''' 
    Replacing decimal numbers with Chinese expression
    '''
    dec_str_set = []
    for dec in decimal_set:
        dec_str=float2Chinese(float(dec))
        dec_str_set.append(dec_str)
    newStr=''
    count=0
    for c in sub_str:
        if c=='_':
            newStr+=dec_str_set[count]
            count+=1
        else:
            newStr+=c
    return newStr
    
def replaceInteger(integer_set, sub_str):
    ''' 
    Replacing integer numbers with Chinese expression
    '''
    int_str_set = []
    for inte in integer_set:
        int_str=integer2Chinese(int(inte))
        int_str_set.append(int_str)
    newStr=''
    count=0
    for c in sub_str:
        if c=='_':
            newStr+=int_str_set[count]
            count+=1
        else:
            newStr+=c
    return newStr

def replaceSpecial(integer_set, sub_str):
    ''' 
    Replacing special numbers with Chinese expression, eg: 2018年 --> 二年一八年
    '''
    charNumSet=['零', '一', '二', '三', '四', '五', '六',
             '七', '八', '九']
    int_str_set = []
    for inte in integer_set:
        int_sub_result=''
        for c in inte:
            if c=='年':
                int_sub_result+='年'
            else:
                int_sub_result+=charNumSet[int(c)]
        int_str_set.append(int_sub_result)
    newStr=''
    count=0
    for c in sub_str:
        if c=='_':
            newStr+=int_str_set[count]
            count+=1
        else:
            newStr+=c
    return newStr

def prepString(string, lang='zh'):
    '''
    Preprocessing the sentence and splitting the decimal, integer or special
    '''
    decimal_set = re.findall(r'\d+\.\d+', string)
    sub_str = re.sub(r'\d+\.\d+', '_', string)
    newStr=replaceDecimal(decimal_set, sub_str)

    integer_set = re.findall(r'\d+年', newStr)
    sub_str = re.sub(r'\d+年', '_', newStr)
    newStr=replaceSpecial(integer_set, sub_str)

    integer_set = re.findall(r'\d+', newStr)
    sub_str = re.sub(r'\d+', '_', newStr)
    newStr=replaceInteger(integer_set, sub_str)
    print('原句子:', string)
    print('新句子:', newStr)
    print('\n')

def section2Chinese(section):
    '''
    Converting section to Chinese expression
    '''
    result=''
    charNumSet=['零', '一', '二', '三', '四', 
                '五', '六', '七', '八', '九']
    charUnitSet=['', '十', '百', '千']
    zero=True
    unitPos=0
    while section>0:
        v=section%10
        if v==0:
            if section==0 or zero is False:
                zero=True
                result=charNumSet[v]+result
        elif (section//10)==0 and v==1 and unitPos==1:
            result=charUnitSet[1]+result
        else:
            zero=False
            strIns=charNumSet[v]
            strIns+=charUnitSet[unitPos] 
            result=strIns+result
        unitPos+=1
        section=section//10
    return result

def integer2Chinese(number):
    '''
    Converting integer to Chinese expression
    '''
    charSectionSet=['', '万', '亿', '万亿']
    result=''
    zero=False
    unitPos=0
    if number==0:
        return '零'
    while number>0:
        section=number%10000
        if zero:
            result='零'+result
        sec_result = section2Chinese(section)
        if section!=0:
            sec_result+=charSectionSet[unitPos]
        result=sec_result+result
        if section<1000 and section>0:
            zero=True
        number=number//10000
        unitPos+=1
    return result

def float2Chinese(number):
    '''
    Converting floating number to Chinese expression
    '''
    charNumSet=['零', '一', '二', '三', '四', '五', '六',
             '七', '八', '九']
    integer_part, decimal_part=str(number).split('.')
    int_result=integer2Chinese(int(integer_part))
    dec_result=''
    for c in decimal_part:
        dec_result+=charNumSet[int(c)]
    return int_result+'点'+dec_result

if __name__ == '__main__':
    prepString('这些苹果的重量是105.23千克')
    prepString('310岁')
    prepString('中国面积9600000平方公里')
    prepString('现在时间是12点15分')
    prepString('现在是2012年11月')
    rootdir='/media/pony/DLdigest/data/ASR_zh'
    r1 = re.compile(r'\d+')
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            fullFilename = os.path.join(subdir, file)
            filenameNoSuffix =  os.path.splitext(fullFilename)[0]
            if file.endswith('.label'):
                with open(fullFilename, 'r') as f:
                    line = f.read()
                    if re.match(r1, line):
                        print(fullFilename)
                        try:
                            prepString(line)
                        except IndexError:
                            pass
