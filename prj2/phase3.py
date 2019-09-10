from bsddb3 import db
import re
import sys
from Search import *
import datetime

aId=[]

dataA = None
dataD = None
dataP = None
dataT = None

curA = None
curD = None
curP = None
curT = None

def date_add(datestr, days): #return a string of date + days
    date = datetime.datetime.strptime(datestr, "%Y/%m/%d")
    dateup = str(date + datetime.timedelta(days))[:10]
    dateup = dateup.replace('-','/')
    return dateup

def createDB():
    global dataA, dataD, dataP, dataT
    global curA, curD, curP, curT

    dataA = db.DB()
    #dataA.set_flags(db.DB_DUP)
    dataA.open("ad.idx", None, db.DB_HASH, db.DB_CREATE)
    curA = dataA.cursor()
    
    
    dataD = db.DB()
    dataD.set_flags(db.DB_DUP)
    dataD.open("da.idx", None, db.DB_BTREE, db.DB_CREATE)
    curD = dataD.cursor()

    dataP = db.DB()
    dataP.set_flags(db.DB_DUP)
    dataP.open("pr.idx", None, db.DB_BTREE, db.DB_CREATE)
    curP = dataP.cursor()

    dataT = db.DB()
    dataT.set_flags(db.DB_DUP)
    dataT.open("te.idx", None, db.DB_BTREE, db.DB_CREATE)
    curT = dataT.cursor()


def closeDB():
    global dataA, dataD, dataP, dataT
    global curA, curD, curP,curT

    curA.close()
    dataA.close()
    curD.close()
    dataD.close()
    curP.close()
    dataP.close()
    curT.close()
    dataT.close()


def search(que):
    global aId
    adlist=[]
    alist=[]

    if len(aId)==0:    
        result = curT.set(que.encode("utf-8")) 
        if(result != None):
            aId.append(result[1].decode("utf-8"))
            dup = curT.next_dup()
            while(dup != None):
                aId.append(dup[1].decode("utf-8"))
                dup = curT.next_dup() 
                
    else:
        result = curT.set(que.encode("utf-8")) 
        if(result != None):
            adlist.append(result[1].decode("utf-8"))
            dup = curT.next_dup()
            while(dup != None):
                adlist.append(dup[1].decode("utf-8"))
                dup = curT.next_dup()                    
        for i in adlist:
            if i in aId:
                alist.append(i)
        aId=alist
                
def prange(sym,pri):
    
    global aId
    adList=[]
    if len(aId)==0:
        m=1
    else:
        m=0
    
    pri = '{:>12}'.format(pri)
    if sym=='=':
        result = curP.set(pri.encode("utf-8")) 
        if(result != None):
            aid=str(result[1].decode("utf-8")) 
            aid = re.split(',',aid) 
            if aid[0] in aId or m==1:
                adList.append(aid[0])            
            dup = curP.next_dup()
            while(dup != None):
                aid=str(dup[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])                 
                dup = curP.next_dup() 

    elif sym=='>':
        result = curP.set_range('{:>12}'.format(str(int(pri)+1)).encode("utf-8"))
        if(result != None):
            while(result != None):
                aid=str(result[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])            
                result = curP.next()  

    elif sym=='>=':
        result = curP.set_range(pri.encode("utf-8"))
        if(result != None):
            while(result != None):
                aid=str(result[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])            
                result = curP.next() 

    elif sym=='<':
        result = curP.set_range(''.encode("utf-8"))
        if(result != None):
            while(result != None):
                if(str(result[0].decode("utf-8"))>=pri): 
                    break                
                aid=str(result[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])            
                result = curP.next()     

    elif sym=='<=':
        result = curP.set_range(''.encode("utf-8"))
        if(result != None):
            while(result != None):
                if(str(result[0].decode("utf-8"))>pri): 
                    break                
                aid=str(result[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])            
                result = curP.next()   
    aId=[]
    aId=adList        
    return    
        
def drange(sym,da):
    global aId
    
    adList=[]
    if len(aId)==0:
        m=1
    else:
        m=0

    if sym=='=':
        result = curD.set(da.encode("utf-8")) 
        if(result != None):
            aid=str(result[1].decode("utf-8")) 
            aid = re.split(',',aid) 
            if aid[0] in aId or m==1:
                adList.append(aid[0])            
            dup = curD.next_dup()
            while(dup != None):
                aid=str(dup[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])                 
                dup = curD.next_dup() 

    elif sym=='>':
        result = curD.set_range(date_add(da,+1).encode("utf-8"))
        if(result != None):
            while(result != None):
                aid=str(result[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])            
                result = curD.next()  

    elif sym=='>=':
        result = curD.set_range(da.encode("utf-8"))
        if(result != None):
            while(result != None):
                aid=str(result[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])            
                result = curD.next() 

    elif sym=='<':
        result = curD.set_range(''.encode("utf-8"))
        if(result != None):
            while(result != None):
                if(str(result[0].decode("utf-8"))>=da): 
                    break                
                aid=str(result[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])            
                result = curD.next()     

    elif sym=='<=':
        result = curD.set_range(''.encode("utf-8"))
        if(result != None):
            while(result != None):
                if(str(result[0].decode("utf-8"))>da): 
                    break                
                aid=str(result[1].decode("utf-8")) 
                aid = re.split(',',aid) 
                if aid[0] in aId or m==1:
                    adList.append(aid[0])            
                result = curD.next()
    aId=adList        
    return
        
def searchc(cate):
    global aId
    adlist=[]
    if len(aId)==0:
        iter = curP.first()
        while iter:
            cat=str(iter[1].decode("utf-8")) 
            cat = re.split(',',cat) 
            if cat[1].lower()==cate.lower():
                aId.append(cat[0])
            iter = curP.next()
    
    else:
        iter = curP.first()
        while iter:
            cat=str(iter[1].decode("utf-8"))
            cat = re.split(',',cat) 
            if cat[0] in aId:
                if cat[1].lower()==cate.lower():
                    adlist.append(cat[0])
            iter = curP.next()
        aId=[]
        aId=adlist
    
def searchl(loc):
    
    global aId
    adlist=[]
    if len(aId)==0:
        iter = curP.first()
        while iter:
            cat=str(iter[1].decode("utf-8")) 
            cat = re.split(',',cat) 
            if cat[2].lower()==loc.lower():
                aId.append(cat[0])
            iter = curP.next()
    
    else:
        iter = curP.first()
        while iter:
            cat=str(iter[1].decode("utf-8"))
            cat = re.split(',',cat) 
            if cat[2].lower()==loc.lower():
                if cat[0] in aId:
                    adlist.append(cat[0])
            iter = curP.next()
        aId=adlist
        
def start(que):
    global aId
    adlist=[]
    if len(aId)==0:
        iter = curT.first()
        while iter:
            cat=str(iter[0].decode("utf-8"))  
            d=str(iter[1].decode("utf-8"))
            if cat.startswith(que):
                if d not in aId:
                    aId.append(iter[1].decode("utf-8"))
            iter = curT.next()
    else:
        aidlist1=[]
        aidlist2=[]
        result = curT.first()
        while result:
            tc=str(result[0].decode("utf-8"))
            if tc.startswith(que):
                if result[1].decode("utf-8") not in aidlist1:
                    aidlist1.append(result[1].decode("utf-8"))
            result = curT.next()
        for i in aidlist1:
            if i in aId:
                aidlist2.append(i)
        aId=aidlist2
   
def brief():
    global aId
    for i in aId:
        print(i)
        result = curA.set(i.encode("utf-8")) 
        title = str(result[1].decode("utf-8"))        
        title = re.split('<ti>|</ti>',title) 
        print(title[1])
        title = None       
        
def fullp():
    global aId
    for i in aId:
        result = curA.set(i.encode("utf-8")) 
        ad = str(result[1].decode("utf-8"))   
        aid=re.split('<aid>|</aid>',ad)
        title = re.split('<ti>|</ti>',ad)
        date=re.split('<date>|</date>',ad)
        loc=re.split('<loc>|</loc>',ad)
        cat=re.split('<cat>|</cat>',ad)
        desc=re.split('<desc>|</desc>',ad)
        price=re.split('<price>|</price>',ad)
        print('Id:  ' + aid[1] +'\n' + 'Title:  ' + title[1] +'\n' + 'Description:  ' + desc[1] +'\n' + 'Category:  ' + cat[1] +'\n' + 'Price:  ' + price[1] +'\n' +'Location:  ' + loc[1] +'\n' + 'Date:  ' + date[1] +'\n')
        title = None

def main():
    global aId
    createDB()
    full = False
    qus= str(input('Enter query')) 
    qus_list = standardization(qus)
    print(qus_list)
    for qu in qus_list:
        pa=parse_query(qu)
        if len(pa)==1:
            if pa[0][-1]=='%':
                pa[0] = pa[0][:-1]
                start(pa[0])
            else:
                search(pa[0])
                
    for qu in qus_list:
        pa=parse_query(qu)
        if pa[0]=='date':
            drange(pa[1],pa[2])
        elif pa[0]=='price':
            prange(pa[1],pa[2])
            
    for qu in qus_list:
        pa=parse_query(qu)
        if pa[0]=='cat':
            searchc(pa[2])
        if pa[0]=='location':
            searchl(pa[2])


    while True:
        out=input('Output: Brief(b) or Full(f)')
        if out=='B' or out=='b' or out=='F' or out=='f' or out=='output=full' or out=='output=brief':
            break;
        
    if out=='B' or out=='b' or out=='output=brief':
        brief()
        
    elif out=='F' or out=='f' or out=='output=full':
        fullp()       
        
    print(len(aId))
    
    closeDB()
    
if __name__ == "__main__":
    main()