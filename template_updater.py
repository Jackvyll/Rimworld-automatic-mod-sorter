import pickle
import os
import xml.etree.ElementTree as ET
import json
import sys
from time import sleep
import downloader
import time
import tkinter as tk
from tkinter import filedialog
import logging
from colorama import init
from colorama import Fore as Color
init(autoreset=True)

def Listhandler(template_list): #구독한 모드 리스트 불러오기, template_list에 모드 이름 저장
    root = tk.Tk()
    rim64win_path = filedialog.askopenfilename(initialdir = 'C:/', title = 'Select rimworldwin64.exe', filetype = [('RimworldWin64.exe', 'RimWorldWin64.exe')])
    rim64win_folder = os.path.dirname(rim64win_path)
    root.destroy()

    localmod_path = '{}/Mods'.format(rim64win_folder) #림월드 내 Mods 폴더 경로
    localmod_moddir = os.listdir(localmod_path)


    os.chdir(rim64win_folder)
    os.chdir('../')
    os.chdir('../')
    os.chdir('./workshop/content/294100')
    moddir = os.listdir('./')
    rimmoddir = os.getcwd() 

    for num in moddir: # num은 모드 번호
        try:
            temp = '{}/{}/About'.format(rimmoddir,num)
            os.chdir(temp) #각 모드의 About 폴더로 이동
            doc = ET.parse('About.Xml') #About.Xml 파싱
            root = doc.getroot()
            name = root.find('name').text # 이름을 저장
            template_list.append(name)
        
        except:
            pass

    for num in localmod_moddir:
        temp = '{}/Mods/{}/About'.format(rim64win_folder,num)
        os.chdir(temp)
        doc = ET.parse('About.xml')
        root = doc.getroot()
        name = root.find('name').text
        template_list.append(name)

def sort_num_update(template_dic, overlap_list): #template_dic는 template에 모드이름 : 번호로 추가, overlap_list는 기존의 template 받아오기
    template_list = []
    Listhandler(template_list)

    print('현재 확인된 모드의 개수는 ' + Color.LIGHTGREEN_EX + '{}'.format(len(template_list)) + Color.WHITE + '개 입니다.')
    sleep(0.2)
    
    #중복되는 모드를 제거하는 라인
    print('중복되는 모드를 리스트에서 제거하는 중...')
    sleep(0.4)
    for val in overlap_list:
        try:
            indexnum = template_list.index(val)
            del template_list[indexnum]
        except:
            pass

    
    print(Color.LIGHTGREEN_EX + len(template_list), + Color.LIGHTGREEN_EX + ' 개의 모드가 확인되었습니다...')
    sleep(0.2)
    print('중단하려면 숫자 대신 X 키를 입력해주세요')
    print('모드 배열의 순서는 Dcinside Rimworld 갤러리의 닉네임 개념글에서 닉네임 "forge"를 찾아주세요.')
    sleep(0.2)
    for temp in template_list: # 모드 리스트를 불러줌
        print('Mod name : {}'.format(temp))
        breakloop = False
        test = False
        while test == False:
            i = (input('번호는 1~20번입니다. : '))
            if i == 'X' or i == 'x':
                print('작업이 중단되었습니다.')
                breakloop = True
                test = True
            try:
                template_dic[temp] = float(i)
                if float(i) > 20 or float(i) < 0:
                    raise ValueError
                print('\n\n')
                test = True
            
            except:
                print('올바르지 않는 입력입니다... 1~20에 해당하는 숫자를 입력해주세요.')
        
        if breakloop == True:
            break

    print('다음과 같은 template를 입력하였습니다.\n')
    if len(template_dic) != 0:
        for temp in template_dic:
            print(temp,' : ', template_dic[temp]) 

    else:
        if breakloop == False:
            print('이미 Load한 모든 모드가 template에 저장되어있습니다. 프로그램을 종료합니다...')
            sys.exit(0)
        if breakloop == True:
            print('작업을 중단하였습니다. 지금까지 한 작업물을 저장합니다...')

        
#print (os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':

        downloaded_list = downloader.update() # 
        template_dic = {}
        temp = False
        while temp == False:
            a = input('Y를 입력하면 모드 번호를 설정하고, N을 입력하면 프로그램을 종료합니다. Y/N : ')
            if a == 'Y' or a == 'y' :   
                sort_num_update(template_dic, downloaded_list)
                temp = True

            elif a == 'N' or a == 'n':
                temp = True

            else:
                print('잘못 입력하였습니다. Y 또는 N만 입력해주세요.')

        downloaded_list.update(template_dic)
        downloaded_list.update({'time' : time.ctime()})
        json_val = json.dumps(downloaded_list) #string 형식
        
        homedir = os.environ['HOMEPATH']
        os.chdir('C:/')
        os.chdir(homedir)
        os.chdir('./desktop')
        if os.path.isfile('db_template.json'):
            os.remove('db_template.json')
            
        with open('db_template.json', 'w') as f:
            f.write(json_val)
            f.close()

        