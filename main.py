
import os
import shutil
import Parse
from time import sleep
import downloader
import time
import sys

class exitError(Exception):
    trynum = 0
    print('프로그램을 종료합니다. 아무 키나 3번 눌러주세요.')
    print('press any key 3 times to exit program')
    while trynum != 3:       
        input('Press any Key. : ')
        trynum = trynum + 1

Version = 0.1
print('현재 버전은 v' + str(Version) + '입니다.')
print('current program version is' + str(Version))
print('\n')
time.sleep(1)

#백업라인
#------------------------------------------------
#VM 머신에선 여기가 없어서 오류가 남...
try:
    temp = os.environ['userprofile']
    rimsavedir = '{}/appdata/locallow/Ludeon Studios\RimWorld by Ludeon Studios\Config'.format(temp)
    os.chdir(rimsavedir)
except:
    print('림월드 SAVE 폴더를 찾을 수 없습니다. 림월드를 설치하신 게 맞나요?')
    raise(exitError)

print('기존 컨픽 파일을 백업하는 중...')
print('saving old config files...')
now_time = time.strftime('%d_%H_%M', time.localtime(time.time()))
shutil.copy('ModsConfig.xml', 'ModsConfig.xml.backup{}'.format(now_time))
#------------------------------------------------

print('template를 받아오는 중입니다...')
print('downloading mod DB from github...')
data = downloader.update()
print('현재 다운받은 파일은 마지막으로 {} 시각에 업데이트 된 파일입니다. 잠시만 기다려 주세요...'.format(data['time']))
print('DB last updated time : {}'.format(data['time']))
lastest_Version = data['Version']
if Version < lastest_Version:
    print('업데이트 버전이 발견되었습니다. Discord에서 업데이트를 확인해주세요.')
    print('newer version available!, please upgrade.')
    sys.exit(0)

sleep(2)

mod_dic = {} # 모드와 번호 연결, 번호 : 이름
mod_list_workshop = [] # 모드 리스트(이름만)
mod_dic_num = {} #이름 : 번호
mod_nlist = []

rim64win_path = Parse.Parser(mod_dic,mod_dic_num, mod_list_workshop) # 파싱 작업을 수행 후, 림월드 실행을 위한 파일 경로를 return
print('현재 구독중인 모드 리스트를 불러옵니다...')
print('checking available workshop mods...')

for x in mod_list_workshop:
    sleep(0.1)
    print(x)

config_num = Parse.mod_sort() # config 리스트에 현재 로딩중인 모드를 리스트로 저장
print('모드 세팅에서 로딩한 모드를 재배열 합니다...')
print('sorting mods....')
sleep(1)

mod_list_sorted = list()
for mod in config_num: #mod는 숫자
    if mod == 'Core':
        continue
    try:
        modname = mod_dic[mod] #mod는 숫자
        mod_list_sorted = mod_list_sorted + [[data[modname], mod]]
    except:
        mod_nlist.append(mod)
        print(mod_dic[mod],' 모드는 template에 없어 제외되었습니다.')
        print(mod_dic[mod],' this mod is not supported, template need update.')
        print('\n')
        sleep(0.2)    

mod_list_sorted.sort()

Parse.setconfig(mod_list_sorted)
print('배열한 모드 순서는 다음과 같습니다. \n')
print('mods will be loaded in the following order')
for i in mod_list_sorted:
    sleep(0.1)
    if i[1].isdigit():
        print(mod_dic[i[1]])
    else:
        print(i)

if len(mod_nlist) != 0:
    print('\n')
    print('\n')
    print('다음 모드는 로드 목록에 있었으나, template에 없어서 로드가 해제된 모드입니다. 인-게임에서 수동으로 모드를 배열해주세요.')
    print('These Mods were in load_list, but not in template. please sort mod manually in game')
    print('\n')
    for x in mod_nlist:
        sleep(0.05)
        print(mod_dic[x])

print('\n')
print('배열이 끝났습니다.')
print('sort complete.')
print('\n')
print('림월드를 실행합니다.')
print('launching Rimworld...')
os.startfile(rim64win_path)

print('로그를 확인해주세요.')
sleep(1)

print('아무 키를 3번 누르면 프로그램을 종료합니다...')
print('press any key 3 times to exit program...')
raise(exitError)



