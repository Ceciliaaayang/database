import re


path=input('Enter the mane of txt:')

def terms():
    global path
    aid_start = "<aid>"
    aid_end = "</aid>"
    ti_start = "<ti>"
    ti_end = "</ti>"
    desc_start = "<desc>"
    desc_end = "</desc>"
    f = open (path, 'r+')
    f1 = open ("terms.txt","w+")
    line = f.readline()
    while line:
        if aid_start in line:
            aid = re.findall(aid_start+'(.*?)'+aid_end,line)[0]
            ti = re.findall(ti_start+"(.*?)"+ti_end,line)[0]
            new_ti = parser(ti).lower().split()
            desc = re.findall(desc_start + "(.*?)" + desc_end, line)[0]
            new_desc = parser(desc).lower().split()

            for i in new_ti:
                i = parser(i)
                if len(i) > 2:
                    new_line = str(i).lower() + ":" + str(aid) + '\n'
                    f1.writelines(new_line)

            for j in new_desc:
                j = parser(j)
                if len(j) > 2:
                    new_line= str(j).lower() + ":" + str(aid) + '\n'
                    f1.writelines(new_line)

        line = f.readline()
def parser(string):
    new_string = re.sub("&apos;","'",str(string))
    new_string = re.sub("&quot;",'"',new_string)
    new_string = re.sub('&amp;','&',new_string)
    new_string = re.sub('&#(\d*);','',new_string)
    new_string = re.sub('[^0-9a-zA-Z_-]',' ',new_string)
    return new_string
    f.close()
    f1.close()
terms()

def prices():
    global path
    aid_start = "<aid>"
    f = open(path, 'r+')
    f1 = open("prices.txt","w+")
    line = f.readline()
    while line:
        if aid_start in line:
            price= line[line.find("<price>")+len("<price>"):line.find("</price>")]
            aid = line[line.find("<aid>")+len("<aid>"):line.find("</aid>")]
            category =line[line.find("<cat>")+len("<cat>"):line.find("</cat>")]
            location = line[line.find("<loc>")+len("<loc>"):line.find("</loc>")]
            writestuff = '{:>12}'.format(price)+':'+aid+','+category+','+location
            print(writestuff)
            f1.write(writestuff+'\n')
        line = f.readline()    
    f.close()
    f1.close()
prices()

def pdates():
    global path
    aid_start = "<aid>"

    f = open(path, 'r+')
    f1 = open("pdates.txt","w+")
    line = f.readline()
    while line:
        if aid_start in line:
            aid = line[line.find("<aid>")+len("<aid>"):line.find("</aid>")]
            adate = line[line.find("<date>")+len("<date>"):line.find("</date>")]
            category =line[line.find("<cat>")+len("<cat>"):line.find("</cat>")]
            location = line[line.find("<loc>")+len("<loc>"):line.find("</loc>")]
            writestuff = adate+':'+aid+','+category+','+location
            print(writestuff)
            f1.write(writestuff+'\n')
        line = f.readline()
    f.close()
    f1.close()
pdates()


def ads():
    global path
    aid_start = "<aid>"
    aid_end = "</aid>"
    ad_start = "<ad>"
    ad_end = "</ad>"

    f = open(path, 'r')
    f1 = open("ads.txt","w+")

    line = f.readline()
    while line:
        if aid_start in line:
            aid = line[line.find(aid_start)+len(aid_start):line.rfind(aid_end)]
            rec = line
            ad = str(aid) + ":" + str(rec)
            f1.write(ad)
        line = f.readline()
    f.close()
    f1.close()
ads()


