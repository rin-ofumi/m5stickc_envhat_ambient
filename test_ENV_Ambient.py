from m5stack import *
import machine
import gc
import utime
import uos
import _thread
import hat
import ntptime


# 変数宣言
Am_err              = 1     # グローバル
Disp_mode           = 0     # グローバル
lcd_mute            = False # グローバル
m5type              = 0     # グローバル [0:M5StickC、1: M5StickCPlus]
am_interval         = 300   # Ambientへデータを送るサイクル（秒）
AM_ID               = None
AM_WKEY             = None
Env_T               = ''
Env_H               = ''
Env_P               = ''


# @cinimlさんのファーム差分吸収ロジック
class AXPCompat(object):
    def __init__(self):
        if( hasattr(axp, 'setLDO2Vol') ):
            self.setLDO2Vol = axp.setLDO2Vol
        else:
            self.setLDO2Vol = axp.setLDO2Volt

axp = AXPCompat()


# 時計表示スレッド関数
def time_count():
    global Disp_mode , m5type
    global Am_err
    
    while True:
        if Am_err == 0 : # Ambient通信不具合発生時は時計の文字が赤くなる
            fc = lcd.WHITE
        else :
            fc = lcd.RED

        if Disp_mode == 1 : # 表示回転処理
            if m5type == 0 :
                lcd.rect(67, 0, 80, 160, lcd.BLACK, lcd.BLACK)
                lcd.font(lcd.FONT_DefaultSmall, rotate = 90)
                lcd.print('{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()[:6]), 78, 40, fc)
            if m5type == 1 :
                lcd.rect(113, 0, 135, 240, lcd.BLACK, lcd.BLACK)
                lcd.font(lcd.FONT_DejaVu18, rotate = 90)
                lcd.print('{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()[:6]), 131, 30, fc)
        else :
            if m5type == 0 :
                lcd.rect(0 , 0, 13, 160, lcd.BLACK, lcd.BLACK)
                lcd.font(lcd.FONT_DefaultSmall, rotate = 270)
                lcd.print('{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()[:6]), 2, 125, fc)
            if m5type == 1 :
                lcd.rect(0 , 0, 20, 240, lcd.BLACK, lcd.BLACK)
                lcd.font(lcd.FONT_DejaVu18, rotate = 270)
                lcd.print('{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*utime.localtime()[:6]), 4, 210, fc)
		
        utime.sleep(0.5)


# 表示OFFボタン処理スレッド関数
def buttonA_wasPressed():
    global lcd_mute

    if lcd_mute :
        lcd_mute = False
    else :
        lcd_mute = True

    if lcd_mute == True :
        axp.setLDO2Vol(0)   #バックライト輝度調整（OFF）
    else :
        axp.setLDO2Vol(2.7) #バックライト輝度調整（中くらい）


# 表示切替ボタン処理スレッド関数
def buttonB_wasPressed():
    global Disp_mode

    if Disp_mode == 1 :
        Disp_mode = 0
    else :
        Disp_mode = 1
    
    draw_lcd()


# 表示モード切替時の枠描画処理関数
def draw_lcd():
    global Disp_mode , m5type

    lcd.clear()

    if Disp_mode == 1 :
        if m5type == 0 :
            lcd.line(66, 0, 66, 160, lcd.LIGHTGREY)
        if m5type == 1 :
            lcd.line(112, 0, 112, 240, lcd.LIGHTGREY)
    else :
        if m5type == 0 :
            lcd.line(14, 0, 14, 160, lcd.LIGHTGREY)
        if m5type == 1 :
            lcd.line(23, 0, 23, 240, lcd.LIGHTGREY)

    draw_env()


# 値表示処理関数
def draw_env():
    global Disp_mode , m5type
    global lcd_mute
    global Env_T
    global Env_H
    global Env_P

    if Env_P == '' : # 初期値の場合は非表示（黒文字）
        fc = lcd.BLACK
    else :
        fc = lcd.WHITE
	
    if Disp_mode == 1 : # 表示回転処理
        if m5type == 0 :
            lcd.rect(0, 0, 65, 160, lcd.BLACK, lcd.BLACK)
            lcd.font(lcd.FONT_Default, rotate = 90)
            lcd.print(Env_T + ' C', 58, 120 - int((len(Env_T + ' C')* 18)/2), fc)
            lcd.print(Env_H + ' %', 38, 120 - int((len(Env_H + ' %')* 18)/2), fc)
            lcd.print(Env_P + ' hPa', 18, 138 - int((len(Env_P + ' hPa')* 18)/2), fc)
        if m5type == 1 :
            lcd.rect(0, 0, 111, 240, lcd.BLACK, lcd.BLACK)
            lcd.font(lcd.FONT_DejaVu18, rotate = 90)
            lcd.print(Env_T + ' C', 95, 160 - int((len(Env_T + ' C')* 18)/2), fc)
            lcd.print(Env_H + ' %', 65, 160 - int((len(Env_H + ' %')* 18)/2), fc)
            lcd.print(Env_P + ' hPa', 35, 160 - int((len(Env_P + ' hPa')* 18)/2), fc)
    else :
        if m5type == 0 :
            lcd.rect(15 , 0, 80, 160, lcd.BLACK, lcd.BLACK)
            lcd.font(lcd.FONT_Default, rotate = 270)
            lcd.print(Env_T + ' C', 22, 40 + int((len(Env_T + ' C')* 18)/2), fc)
            lcd.print(Env_H + ' %', 42, 40 + int((len(Env_H + ' %')* 18)/2), fc)
            lcd.print(Env_P + ' hPa', 62, 22 + int((len(Env_P + ' hPa')* 18)/2), fc)
        if m5type == 1 :
            lcd.rect(24 , 0, 135, 240, lcd.BLACK, lcd.BLACK)
            lcd.font(lcd.FONT_DejaVu18, rotate = 270)
            lcd.print(Env_T + ' C', 40, 80 + int((len(Env_T + ' C')* 18)/2), fc)
            lcd.print(Env_H + ' %', 70, 80 + int((len(Env_H + ' %')* 18)/2), fc)
            lcd.print(Env_P + ' hPa', 100, 80 + int((len(Env_P + ' hPa')* 18)/2), fc)


# am_set.txtの存在/中身チェック関数
def am_set_filechk():
    global AM_ID
    global AM_WKEY

    scanfile_flg = False
    for file_name in uos.listdir('/flash') :
        if file_name == 'am_set.txt' :
            scanfile_flg = True
    
    if scanfile_flg :
        print('>> found [am_set.txt] !')
        with open('/flash/am_set.txt' , 'r') as f :
            for file_line in f :
                filetxt = file_line.strip().split(':')
                if filetxt[0] == 'AM_ID' :
                    AM_ID = str(filetxt[1])
                    print('- AM_ID: ' + str(AM_ID))
                elif filetxt[0] == 'AM_WKEY' :
                    if len(filetxt[1]) == 16 :
                        AM_WKEY = str(filetxt[1])
                        print('- AM_WKEY: ' + str(AM_WKEY))
    else :
        print('>> no [am_set.txt] !')
    return scanfile_flg


# メインプログラムはここから（この上はプログラム内関数）


# WiFi設定
import wifiCfg
wifiCfg.autoConnect(lcdShow=True)


# 画面初期化
axp.setLDO2Vol(2.7) #バックライト輝度調整（中くらい）

if lcd.winsize() == (80,160) :  # M5StickC/Plus機種判定
    m5type = 0
    print('>> M5Type = M5StickC')
if lcd.winsize() == (136,241) :
    m5type = 1
    print('>> M5Type = M5StickCPlus')

draw_lcd()


# ユーザー設定ファイル読み込み
am_set_filechk()


# Ambient設定
if (AM_ID is not None) and (AM_WKEY is not None) : # Ambient設定情報があった場合
    import ambient
    am_env = ambient.Ambient(AM_ID, AM_WKEY)


# RTC設定
ntp = ntptime.client(host='jp.pool.ntp.org', timezone=9)


# 時刻表示スレッド起動
_thread.start_new_thread(time_count, ())


# ボタン検出スレッド起動
btnA.wasPressed(buttonA_wasPressed)
btnB.wasPressed(buttonB_wasPressed)


# タイムカウンタ初期値設定
am_tc = utime.time()


# ENV HAT設定
hat_env0 = hat.get(hat.ENV)
utime.sleep(1)


# メインルーチン
while True:    
    Env_T = str('{:.1f}'.format(hat_env0.temperature))
    Env_H = str('{:.1f}'.format(hat_env0.humidity))
    Env_P = str('{:.1f}'.format(hat_env0.pressure))
    print(str(Env_T) + ' C / ' + str(Env_H) + ' % / ' + str(Env_P) + ' hPa')
    draw_env()

    if (utime.time() - am_tc) >= am_interval :      # インターバル値の間隔でAmbientへsendする
        am_tc = utime.time()
        try :                                       # ネットワーク不通発生などで例外エラー終了されない様に try except しとく
            r = am_env.send({'d1': hat_env0.temperature, 'd2': hat_env0.humidity, 'd3': hat_env0.pressure})
            print('Ambient send OK! / ' + str(r.status_code) + ' / ' + str(Am_err))
            Am_err = 0
            am_tc = utime.time()
            r.close()
        except:
            print('Ambient send ERR! / ' + str(Am_err))
            Am_err = Am_err + 1

    utime.sleep(1)
    gc.collect()    
