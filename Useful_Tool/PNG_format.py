# -*- encoding:utf-8 -*-
import zlib
import termcolor
import binascii

# CRC_OPTION = How to deal CRC error
# 0: exit
# 1: ignore
# 2: change crc correctly(temporary)
# 3: change crc correctly(permanent)

CRC_OPTION = None
CRC_ARRAY = {'e':0, 'i':1, 'c':2}

ERROR_ICON = '[-]'
CORRECT_ICON = '[+]'

def conv(string):
    res = ''
    for i in string:
        tmp = hex(ord(i))[2:]
        res += '0'*(2-len(tmp))+tmp
    return str(int(res, 16))

def text_examine(data):
    case = ['Title', 'Author', 'Description', 'Copyright', 'CreationTime', 'Software', 'Disclaimer', 'Warning', 'Source', 'comment']
    output = []

    global CRC_OPTION

    for title in case:
        if title in data:
            cnt = data.count(title)
            start = 0
            for _ in range(cnt):
                start = data.find(title, start)
                crc_start = start-4
                if data[start-4:start].lower() == 'text':
                    length = data[start-8:start-4]
                    start += len(title)+1
                    end = start + int(conv(length))-4
                    crc = zlib.crc32(data[crc_start:end-4])&0xffffffff
                    output.append([CORRECT_ICON, title, data[start:end-4], conv(length), hex(crc)[2:]])
                    if int(conv(data[end-4:end])) != crc:
                        if CRC_OPTION == None:
                            p_str = 'CRC error occured (Calculated is %s In file is %s)\nOption: [E]xit\t[I]gnore\t[C]hange' %(hex(crc), hex(int(conv(data[end-4:end]))))
                            termcolor.cprint(p_str, 'red'),
                            CRC_OPTION = CRC_ARRAY[raw_input().lower()]
                        if CRC_OPTION == 0:
                            exit(1)
                        elif CRC_OPTION == 1:
                            output[-1][0] = ERROR_ICON
                            output[-1][-1] = hex(int(conv(data[end-4:end])))[2:]+' --> '+hex(crc)[2:]
                        elif CRC_OPTION == 2:
                            output[-1][0] = ERROR_ICON
                            output[-1][-1] = hex(int(conv(data[end-4:end])))[2:]+' --> '+hex(crc)[2:]
                            p_str = 'This process can\'t be undo\nDo you really want to do this? [Y/N]'
                            termcolor.cprint(p_str, 'red')
                            crc_selection = raw_input()
                            while True:
                                if crc_selection.lower() == 'y':
                                    tmp = hex(crc)[2:]
                                    data = data[:end-4] + binascii.unhexlify('0'*(8-len(tmp))+tmp) + data[end:]
                                    CRC_OPTION = 3
                                    break
                                if crc_selection.lower() == 'n':
                                    CRC_OPTION = 1
                                    break
                                crc_selection = raw_input()
                                termcolor.cprint('It\'s invalid option', 'red')
                        elif CRC_OPTION == 3:
                            output[-1][0] = ERROR_ICON
                            output[-1][-1] = hex(int(conv(data[end-4:end])))[2:]+' --> '+hex(crc)[2:]
                            tmp = hex(crc)[2:]
                            data = data[:end-4] + binascii.unhexlify('0'*(8-len(tmp))+tmp) + data[end:]
                        # raise ArithmeticError
    return output, data

def bin_examine(data):
    case = ['IHDR', 'PLTE', 'IEND', 'gAMA', 'cHRM', 'sRGB']
    output = []

    cnt = 0
    global CRC_OPTION

    for title in case:
        if title in data:
            start = data.find(title)
            end = start + int(conv(data[start-4:start])) + 8
            crc = zlib.crc32(data[start:end - 4]) &0xffffffff
            start += 4
            if title == 'IHDR':
                output.append([CORRECT_ICON, 'Width', conv(data[start:start+4]), '4', hex(crc)[2:]])
                output.append([CORRECT_ICON, 'Height', conv(data[start+4:start+8]), '4', '-'])
                output.append([CORRECT_ICON, 'Bit-depth', conv(data[start+8]), '1', '-'])
                output.append([CORRECT_ICON, 'Color-type', conv(data[start+9]), '1', '-'])
                output.append([CORRECT_ICON, 'Compression-method', conv(data[start+10]), '1', '-'])
                output.append([CORRECT_ICON, 'Filter-method', conv(data[start+11]), '1', '-'])
                output.append([CORRECT_ICON, 'Interlace-method', conv(data[start+12]), '1', '-'])
                cnt = 7

            if title == 'PLTE':
                output.append([CORRECT_ICON, 'PLTE-red', conv(data[start:start+3]), '3', hex(crc)[2:]])
                output.append([CORRECT_ICON, 'PLTE-green', conv(data[start+3:start+6]), '3', '-'])
                output.append([CORRECT_ICON, 'PLTE-blue', conv(data[start+6:start+9]), '3', '-'])
                cnt = 3

            if title == 'IEND':
                output.append([CORRECT_ICON, 'IEND', 'NULL', '0', hex(crc)[2:]])
                cnt = 1

            if title == 'gAMA':
                output.append([CORRECT_ICON, 'GAMA', conv(data[start:start+4]), '4', hex(crc)[2:]])
                cnt = 1

            if title == 'cHRM':
                output.append([CORRECT_ICON, 'White-x', conv(data[start:start+4]), '4', hex(crc)[2:]])
                output.append([CORRECT_ICON, 'White-y', conv(data[start+4:start+8]), '4', '-'])
                output.append([CORRECT_ICON, 'Red-x', conv(data[start+8:start+12]), '4', '-'])
                output.append([CORRECT_ICON, 'Red-y', conv(data[start+12:start+16]), '4', '-'])
                output.append([CORRECT_ICON, 'Green-x', conv(data[start+16:start+20]), '4', '-'])
                output.append([CORRECT_ICON, 'Green-y', conv(data[start+20:start+24]), '4', '-'])
                output.append([CORRECT_ICON, 'Blue-x', conv(data[start+24:start+28]), '4', '-'])
                output.append([CORRECT_ICON, 'Blue-y', conv(data[start+28:start+32]), '4', '-'])
                cnt = 8

            if title == 'sRGB':
                output.append([CORRECT_ICON, 'Rendering', conv(data[start]), '1', hex(crc)[2:]])
                cnt = 1

            if int(conv(data[end-4:end])) == crc:
                pass
            else:
                if CRC_OPTION == None:
                    p_str = 'CRC error occured (Calculated is %s In file is %s)\nOption: [E]xit\t[I]gnore\t[C]hange' %(hex(crc), hex(int(conv(data[end-4:end]))))
                    termcolor.cprint(p_str, 'red'),
                    CRC_OPTION = CRC_ARRAY[raw_input().lower()]
                if CRC_OPTION == 0:
                    exit(1)
                elif CRC_OPTION == 1:
                    output[-cnt][0] = ERROR_ICON
                    output[-cnt][-1] = hex(int(conv(data[end-4:end])))[2:]+' --> '+hex(crc)[2:]
                elif CRC_OPTION == 2:
                    output[-cnt][0] = ERROR_ICON
                    output[-cnt][-1] = hex(int(conv(data[end-4:end])))[2:]+' --> '+hex(crc)[2:]
                    p_str = 'This process can\'t be undo\nDo you really want to do this? [Y/N]'
                    termcolor.cprint(p_str, 'red')
                    crc_selection = raw_input()
                    while True:
                        if crc_selection.lower() == 'y':
                            tmp = hex(crc)[2:]
                            data = data[:end-4] + binascii.unhexlify('0'*(8-len(tmp))+tmp) + data[end:]
                            CRC_OPTION = 3
                            break
                        if crc_selection.lower() == 'n':
                            CRC_OPTION = 1
                            break
                        crc_selection = raw_input()
                        termcolor.cprint('It\'s invalid option', 'red')
                elif CRC_OPTION == 3:
                    output[-cnt][0] = ERROR_ICON
                    output[-cnt][-1] = hex(int(conv(data[end-4:end])))[2:]+' --> '+hex(crc)[2:]
                    tmp = hex(crc)[2:]
                    data = data[:end-4] + binascii.unhexlify('0'*(8-len(tmp))+tmp) + data[end:]

    return output, data

def printing(data):
    fmt = '%-5s|%-20s|%-33s|%-16s|%-30s'
    termcolor.cprint(fmt %('', '\tType', '\tValue', '\tLength', '\tCRC'), 'green')
    termcolor.cprint(fmt %('', '\t', '\t', '\t', '\t'), 'green')
    termcolor.cprint('-'*100, 'green')
    for value in data:
        crc = (value[4]).upper()
        if '-' not in crc:
            crc = '0'*(8-len(crc))+crc
        if value[0] == CORRECT_ICON:
            termcolor.cprint(fmt %(value[0], '\t'+value[1], '\t'+value[2], '\t'+value[3], '\t'+crc), 'green')
        else:
            termcolor.cprint(fmt %(value[0], '\t'+value[1], '\t'+value[2], '\t'+value[3], '\t'+crc), 'red')

def writing(image, data):
    res = ''
    fmt = '%-5s|%-20s|%-33s|%-16s|%-30s\n'
    res += fmt %('', '\tType', '\tValue', '\tLength', '\tCRC')
    res += fmt %('', '\t', '\t', '\t', '\t')
    res += '-'*100 + '\n'
    for value in data:
        crc = (value[4]).upper()
        res += fmt %(value[0], '\t'+value[1], '\t'+value[2], '\t'+value[3], '\t'+crc)
    image = image.split('/')[-1]
    image = image.split('.')[0]
    with open(image+'.txt', 'w') as f:
        f.write(res)


def examine(image, output=False):
    res = []
    try:
        with open(image, 'rb') as f:
            data = f.read()
        assert data[1:4] == 'PNG'
    except:
        termcolor.cprint("[-] Can't load image file", 'red')
        exit()

    tmp = text_examine(data)
    res += tmp[0]
    data = tmp[1]

    tmp = bin_examine(data)
    res += tmp[0]
    data = tmp[1]
    printing(res)
    if CRC_OPTION == 3:
        with open(image, 'wb') as f:
            f.write(data)
    writing(image, res)

examine(image='/Users/Knight/Desktop/세종 말뭉치/version3.png')
