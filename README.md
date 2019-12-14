# env_hat_ambient
MicroPython project / ENV HAT &amp; M5StickC / Data storage uses Ambient

<br>

# <概要>

* M5StickCとENV HATを使って、気温・湿度・気圧を表示するプログラムです。
* AmbientというIoTデータ可視化サービスを使って、記録を残すことも可能です。（無料枠で使えます）
* MicroPythonで記述しています。（ファームウェアは UIFlow-v1.4.2 を使用）

この様な環境データグラフを取得出来るようになります。

![Ambient_ENV_1](https://kitto-yakudatsu.com/wp/wp-content/uploads/2019/10/Ambient_env.png)

こちらは2019年10月12日に日本に上陸して猛威を振るった台風19号通過時の気圧記録です。(単位は hPa )

![Ambient_ENV_2](https://kitto-yakudatsu.com/wp/wp-content/uploads/2019/10/Ambient_Press_2.png)

台風の目付近が通過した際の低気圧のピークが記録されています。

![Ambient_ENV_3](https://kitto-yakudatsu.com/wp/wp-content/uploads/2019/10/Ambient_Press_1.png)

<br>

# <実行に必要なファイル>

## Ambientライブラリ「ambient.py」※オプション
Ambientへのデータ送信（記録）を使う場合は、[こちら](https://github.com/AmbientDataInc/ambient-python-lib)のライブラリが必要です。<br>
「ambient.py」をM5StickCのルートに保存して下さい。<br>

<br>

## NTP時刻同期ライブラリ「ntptime.py」**※必須**
NTP時刻同期機能は、[こちら](https://github.com/micropython/micropython/blob/master/ports/esp8266/modules/ntptime.py)のライブラリを使っています。<br>
「ntptime.py」をダウンロードし、下記部分を修正して下さい。（日本時間へ設定を変える為）<br>

```python
NTP_DELTA = 3155673600
```

↓<br>

```python
NTP_DELTA = 3155673600 - (9*60*60)
```

修正したら「ntptime.py」をM5StickCのルートに保存して下さい。<br>

<br>

## 当プログラム本体「test_ENV_Ambient.py」**※必須**
M5StickCのプログラム選択モード「APP.List」から起動させる場合は、「test_ENV_Ambient.py」をM5StickCの「Apps」配下に保存して下さい。<br>

<br>

## Ambientの設定ファイル「am_set.txt」※オプション
Ambientを使う場合は、「am_set.txt」の修正が必要です。<br>
「チャネルID」を「AM_ID:」以降に、「ライトキー」を「AM_WKEY:」以降に追記して下さい。<br>
※空白文字、"などは含まない様にして下さい<br>
<br>
修正後、M5StickCのルートに保存して下さい。<br>
尚、「am_set.txt」が無い場合は、Ambientへのデータ送信は行われません。<br>

<br>

# <使い方>

## 基本動作

- プログラム起動させると、M5StickCの画面に時刻・気温・湿度・気圧が表示されます。
- 300秒毎（5分毎）にAmbientへ気温・湿度・気圧データを送信しています。
- 時刻が赤文字の時はAmbientへの通信が出来ていない事を示します。（**初回通信してない起動直後の5分間は赤文字**）

<br>

## ボタン操作

- M5StickCのAボタン（M5ロゴの有るボタン）を押すと画面消灯します。もう一度押すと画面点灯します。
- M5StickCのBボタン（電源ボタンじゃない方の側面ボタン）を押すと表示が180度回転しますので、設置向きに合わせてお選び下さい。

![M5StickC_1](https://kitto-yakudatsu.com/wp/wp-content/uploads/2019/10/P1180694-800x600.jpg)

![M5StickC_2](https://kitto-yakudatsu.com/wp/wp-content/uploads/2019/10/P1180695-800x600.jpg)

<br>

# <参考ページ>
その他の情報については[ブログ](https://kitto-yakudatsu.com/archives/7143)をご参照下さい。<br>
※当プログラムは、ブログ記載時より若干バージョンアップしています。<br>

<br>

# <アップデート履歴>

## 【2019.12.14】 [test_ENV_Ambient.py] Update!

* UIFlow-v1.4.2ファーム対応コード変更（過去ファームでも動く様に修正）
* AmbientのチャネルID桁数チェックの削除。（5桁縛りだと勘違いしてました）

<br>

## 【2019.11.23】 [test_ENV_Ambient.py] Update!

* UIFlow-v1.4.2 ファームへの対応

<br>

## 【2019.10.28】

* 最初のリリース

