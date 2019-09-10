#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 23:09:39 2018

@author: ziyuan
"""

import os 

def main():
    '''sort text to keep only the unique rows'''
    os.system('sort -u ads.txt -o ad.txt')
    os.system('sort -u prices.txt -o price.txt')
    os.system('sort -u terms.txt -o term.txt')
    os.system('sort -u pdates.txt -o pdate.txt')
    '''removes backslashes'''
    os.system('perl break.pl =< ad.txt > adb.txt')
    os.system('perl break.pl =< price.txt > priceb.txt')
    os.system('perl break.pl =< term.txt > termb.txt')
    os.system('perl break.pl =< pdate.txt > pdateb.txt')
    '''create indexes'''
    os.system('db_load -T -c duplicates=0 -t hash -f adb.txt ad.idx')
    os.system('db_load -T -c duplicates=1 -t btree -f termb.txt te.idx')
    os.system('db_load -T -c duplicates=1 -t btree -f pdateb.txt da.idx')
    os.system('db_load -T -c duplicates=1 -t btree -f priceb.txt pr.idx')
    

if __name__ == "__main__":
    main()