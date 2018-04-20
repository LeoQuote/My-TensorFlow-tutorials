# 导入模块
from wxpy import *
import random
import math
from identify import evaluate_image, get_image
import os
import uuid
# 初始化机器人，扫码登陆
WHATS_THE_JOKE='whatsthejoke.jpg'
def miaomiaomiao():
    emoji_list = ['(゜-゜)','(=`ｪ´=；)ゞ','(;´༎ຶД༎ຶ`)','⁄(⁄⁄•⁄ω⁄•⁄⁄)⁄','(´･_･`)','(｀∀´)','(:3[▓▓▓]','（╯‵□′）╯︵┴─┴','₍•͈˽•͈₎','∠( ᐛ 」∠)＿','(*ﾉωﾉ)','ヾ(*>∀＜*) ','(ฅωฅ*)','<(￣︶￣)/ ','(´⊙ω⊙`)','(๑•̀ω•́๑)','(≧∀≦)♪','(*/∇＼*)','(｡･ω･｡)ﾉ♡','( • ̀ω•́ )✧','(☆ω☆)','╮(￣⊿￣")╭','(′へ`、)','(ﾟﾛ ﾟﾉ)ﾉ','(*｀▽´*)','Ծ‸Ծ']
    sig_choices = ['？','！','~','~~~','？？？','？！','！！！']
    miao_count = random.randrange(1,15)
    reply_list = ['喵'] * miao_count
    sig_count = random.randrange(0,math.ceil(miao_count/2))
    emoji_count = random.randrange(0,2)
    if emoji_count == 0:
        emoji = ''
    else:
        emoji = random.choice(emoji_list)
    reply_list += [emoji]
    for i in range(sig_count+1):
        reply_list += [random.choice(sig_choices)]
    random.shuffle(reply_list)
    return ''.join(reply_list)
    
def is_cat(msg):
    if msg.type == PICTURE:
        print(msg)
        uuid_str = uuid.uuid4().hex
        tmp_file_name = 'tmpfile_{}.txt'.format(uuid_str)
        tmp_file_name = os.path.join(temp_dir, tmp_file_name)
        print(tmp_file_name)
        msg.get_file(save_path = tmp_file_name )
        return evaluate_image(get_image(tmp_file_name))


def is_hahaha(content):
    if '哈哈' in content:
        return True
    if 'hhh'  in content:
        return True
    if 'hah' in content:
        return True
 
if __name__ == '__main__':
    bot = Bot(console_qr=True, cache_path = True)
    bot.file_helper.send('微信机器人已成功登录')
    test_group = ensure_one(bot.groups().search('test_group'))
    fans_group = ensure_one(bot.groups().search('叛逆'))
    listening_group = [test_group] + [fans_group] + bot.friends()
    my_self = ensure_one(bot.friends().search('很久很久以前'))
    temp_dir = 'temp'
    @bot.register(chats=[test_group] + [fans_group] + bot.friends())
    def test_group_auto(msg):
        if msg.type == TEXT:
            if '喵喵' in msg.text or '猫猫' in msg.text:
                return miaomiaomiao()
        if msg.type == PICTURE:
            return is_cat(msg)
            
                    
    @bot.register(chats=my_self,except_self=False)
    def turn_it_on_and_off(msg):
        if msg.type == PICTURE:
            return is_cat(msg)
        if msg.text == 'off':
            bot.registered.disable()
            bot.registered.enable(turn_it_on_and_off)
            return '机器人已成功暂停'
        if msg.text == 'on':
            bot.registered.enable()
            return '机器人已成功重启'
    bot.join()
