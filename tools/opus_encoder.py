# Tool to help converting .wav to telegram's .ogg

import os

def convert(sound):
    cmd = 'opusenc --downmix-mono ' + str(sound) + '.wav ' + str(sound) + '.ogg'
    os.system(cmd)

print('============================')
print('    OPUS .WAV to .OGG\n\n')
print('* File can not countain spaces.')
print('* There\'s no need to write .wav\n')
print('============================')

running = True

while running:
    sound = input('File name: ')
    if sound == '':
        running = False
        exit()
        
    elif ' ' in sound:
        print('Please remove the spaces from that file!')
    
    else:
        convert(sound)
