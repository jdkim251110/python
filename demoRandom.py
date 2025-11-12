# demoRandom.py 

import random

print(random.random())
print(random.random())
print(random.uniform(2.0, 5.0))
print( [random.randrange(20) for i in range(10)] )
print( [random.randrange(20) for i in range(10)] )
print( random.sample(range(20), 10))
print( random.sample(range(20), 10))
#로또 
print( random.sample(range(1,46), 5) ) 

from os.path import * 
import os 

fileName = "c:\\python310\\python.exe"
print( basename(fileName) )
print( abspath("python.exe") )

if exists(fileName):
    print( "파일 크기:", getsize(fileName) )
else: 
    print( "파일이 존재하지 않습니다." )

#운영체제정보
print( os.name )
print( os.environ ) 
#print( os.system("notepad.exe") )
print( os.getcwd() )

import glob 

#print( glob.glob("c:\\work\\*.py") )
#raw string
print( glob.glob(r"c:\work\*.py") )
#Linux스타일 표기 
print( glob.glob("c:/work/*.py") )



