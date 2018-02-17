# -*- coding: utf-8 -*-
# !/usr/bin/python3

import os.path

dict_path = "word.data"

ziranma_v1 = {
    'i': 'ch',
    'u': 'sh',
    'v': 'zh'
}

ziranma_v2 = {
    'b': 'ou',
    'c': 'iao',
    'd': 'uang iang',
    'f': 'en',
    'g': 'eng',
    'h': 'ang',
    'j': 'an',
    'k': 'ao',
    'l': 'ai',
    'm': 'ian',
    'n': 'in',
    'o': 'uo',
    'p': 'un vn',
    'q': 'iu',
    'r': 'uan van',
    's': 'ong iong',
    't': 'ue ve',
    'v': 'ui',
    'w': 'ia ua',
    'x': 'ie',
    'y': 'uai ing',
    'z': 'ei'
}

ziranma_special = {
    'ah': 'ang'
}

ziranma_config = """%gen_inp
%ename ziranma
%cname 自然码双拼
%selkey 123456789
%space_style 2
%AUTO_COMPOSE false
%max_keystroke 2"""

key_list = "abcdefghijklmnopqrstuvwxyz"

def load_dict():
    if not os.path.exists(dict_path):
        raise IOError("NotFoundFile")

    word_dict = {}
    with open(dict_path, 'r') as f_obj:
        for f_line in f_obj.readlines():
            try:
                line = f_line.split('    ')
                if len(line[0]) is 4:
                    key = '\\u%s' % line[0]
                else:
                    key = '\\U000%s' % line[0]
                key = key.encode('latin-1').decode('unicode_escape')
                word_dict[key] = line[1]
            except:
                line = f_line.split('   ')
                if len(line[0]) is 4:
                    key = '\\u%s' % line[0]
                else:
                    key = '\\U000%s' % line[0]
                key = key.encode('latin-1').decode('unicode_escape')
                word_dict[key] = line[1]

    for key in word_dict:
        word_dict[key] = word_dict[key].\
                         replace('\n', '').\
                         replace('1', '').\
                         replace('2', '').\
                         replace('3', '').\
                         replace('4', '').\
                         replace('5', '')
        if word_dict[key].find(' ') is not -1:
                    newlist = list(set(word_dict[key].split(' ')))
                    word_dict[key] = " ".join(newlist)
    return word_dict

def todp(ori, v1, v2, sp):
    p1 = ''
    p2 = ''
    for key in v1:
        if ori.find(v1[key]) is 0:
            p1 = key
            break
    if p1 is '':
        p2 = ori[-len(ori)+1:]
        p1 = ori[0]
    else:
        p2 = ori[-len(ori)+2:]
    for key in v2:
        for i in v2[key].split(' '):
            if p2 == i:
                p2 = key
                break

    final = p1+p2
    for key in sp:
        if final == sp[key]:
            final = key
    return final

def gencin(word_dict, config, fpath='out.cin'):
    with open(fpath, 'w') as fp:
        fp.write(config + '\n')
        fp.write('%keyname begin\n')
        for x in key_list:
            fp.write('%s %s\n' % (x, x))
        fp.write('%keyname end\n')
        fp.write("%chardef begin\n")
        for key in word_dict:
            for i in word_dict[key].split(' '):
                fp.write('%s %s\n' % (
                    todp(i.lower(), ziranma_v1, ziranma_v2, ziranma_special),
                    key
                ))
        fp.write("%chardef end\n")



if __name__ == '__main__':
    print("Generating Ziranma CIN table...")
    gencin(load_dict(), ziranma_config, 'ziranma.cin')
    print("Done!")
