from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

# add_argumentメソッド
# Chrome起動オプションの指定
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# インスタンスを作成し、変数chrome_driverに格納
chrome_driver = webdriver.Chrome(options=chrome_options)

# URLにアクセスする - リダイレクトされてる
chrome_driver.get("https://glogin.rms.rakuten.co.jp/?sp_id=1")

# ページ要素が表示されるまでWait
# ログインボタンのCSSセレクタをelemに格納
WebDriverWait(chrome_driver, 5).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.rf-form-login.rf-red > main > div > section.rf-form-login--step-1 > form > p:nth-child(7)"))
)

# TODO:最初のログインプロセスを定義する
def get_inp_area_1st():
    # rid_pwの入力 / hanatsubaki
    rid = input("R-Login ID を入力してください：")
    pw = input("R-Login PW を入力してください：")

    # emailアドレスとパスワードの入力欄の特定
    rid_input_area = chrome_driver.find_element(By.CSS_SELECTOR, "#rlogin-username-ja")
    pw_input_area = chrome_driver.find_element(By.CSS_SELECTOR, "#rlogin-password-ja")

    # 入力ボックスの初期化
    rid_input_area.clear()
    pw_input_area.clear()

    rid_input_area.send_keys(rid)
    pw_input_area.send_keys(pw)

def login_click_1st():
    # 「次へ」要素を取得
    elem_login_1st = chrome_driver.find_element(By.CSS_SELECTOR, "body > div.rf-form-login.rf-red > main > div > section.rf-form-login--step-1 > form > p:nth-child(9) > button")
    
    # 「次へ」をクリック
    elem_login_1st.click()

def login_click_err_1st():
    # エラーの場合、CSSセレクタが変動するため再度要素の取得
    elem_login_1st_err = chrome_driver.find_element(By.CSS_SELECTOR, "body > div.rf-form-login.rf-red > main > div > section.rf-form-login--step-1 > form > p:nth-child(11) > button")
    
    # クリック
    elem_login_1st_err.click()


# 1st プロセスの実行
get_inp_area_1st()
login_click_1st()


# TODO:正誤ループ-その1
# find_elementsはリストで返してくるので、条件分岐では1だったら、など数で指定する
for i in range(1,4,1):
    er_messe_1st = chrome_driver.find_elements(By.CSS_SELECTOR, "body > div.rf-form-login.rf-red > main > div > section.rf-form-login--step-1 > form > p.rf-form-message.rf-form-error")
    print(er_messe_1st)

    if len(er_messe_1st) == 1 and i == 3:
        print(f"{i}回以上間違えたため終了します")
        sys.exit()

    elif len(er_messe_1st) == 1:
        print("入力情報に誤りがあります")
        print(f"入力に{i}回失敗しました")
        print("もう一度入力してください")
        get_inp_area_1st()
        login_click_err_1st()

    else:
        print("正しい情報が入力されました")
        break


# TODO:二段階認証のログインプロセスを定義する
def get_inp_area_2nd():
    # useridの入力 / hanatsubaki@clock.ocn.ne.jp
    userid = input("ユーザーIDを入力してください：")
    pipw = input("パスワードを入力してください：")

    # emailアドレスとパスワードの入力欄の特定
    userid_input_area = chrome_driver.find_element(By.CSS_SELECTOR, "#rlogin-username-2-ja")
    pipw_input_area = chrome_driver.find_element(By.CSS_SELECTOR, "#rlogin-password-2-ja")

    # 入力ボックスの初期化
    userid_input_area.clear()
    pipw_input_area.clear()

    # 入力したメアドとパスワードを代入
    userid_input_area.send_keys(userid)
    pipw_input_area.send_keys(pipw)

def login_click_2nd():
    # 「次へ」要素を取得
    elem_login_2nd = chrome_driver.find_element(By.CSS_SELECTOR, "#loginForm > p:nth-child(11) > button")

    # 「次へ」をクリック
    elem_login_2nd.click()

def login_click_err_2nd():
    # エラーの場合のCSSセレクタの取得
    elem_login_2nd_err = chrome_driver.find_element(By.CSS_SELECTOR, "#loginForm > p:nth-child(13) > button")
    elem_login_2nd_err.click()

# 2nd プロセスの実行
get_inp_area_2nd()
login_click_2nd()

# TODO:正誤ループ-その2
for j in range(1,4,1):
    er_messe_2nd = chrome_driver.find_elements(By.CSS_SELECTOR, "#loginForm > p.rf-form-login--input-error.rf-form-message.rf-form-error")
    print(er_messe_2nd)

    if len(er_messe_2nd) == 1 and j == 3:
        print("3回以上間違えたため終了します")
        sys.exit()

    elif len(er_messe_2nd) == 1:
        print("入力情報に誤りがあります")
        print(f"入力に{j}回失敗しました")
        print("もう一度入力してください")
        get_inp_area_2nd()
        login_click_err_2nd()
            
    else:
        print("正しい情報が入力されました")
        break


# TODO:常に出てこない確認画面の例外処理の作成
def final_conf():
    # 最後の次へボタン
    WebDriverWait(chrome_driver, 2).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#message-ja > section > div > div > div > div > button"))
    )
    final_conf = chrome_driver.find_element(By.CSS_SELECTOR, "#message-ja > section > div > div > div > div > button")
    final_conf.click()

def info_conf():
    # お知らせの確認ボタン
    WebDriverWait(chrome_driver, 2).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#confirm > p > button"))
    )
    info_conf = chrome_driver.find_element(By.CSS_SELECTOR, "#confirm > p > button")
    info_conf.click()

def consultant_info():
    # コンサルからのお知らせポップアップ
    WebDriverWait(chrome_driver, 2).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#overContainer1 > div.eccMessagePopTitle > span"))
    )
    consul_pop = chrome_driver.find_element(By.CSS_SELECTOR, "#overContainer1 > div.eccMessagePopTitle > span")
    consul_pop.click()

# 出る時と出ない時があるため、エラーにならないように例外処理
try:
    final_conf()
except:
    pass

try:
    info_conf()
except:
    pass

try:
    consultant_info()
except:
    pass


# TODO:ログイン後の分岐処理
options_select = input("次の中から実行したい処理を選んで下さい: >> 1. CSV(最低限), 2. CSV(全データ), 3. クーポン発行(20%OFF)")

# # TODO:もしオプションが1の場合、CSVのダウンロード処理（最低限の項目）
# if options_select == 1:
    

#     # TODO:もしオプションが2の場合、CSVのダウンロード処理（全項目）
#     if options_select == 2:
        

#         # TODO:もしオプションが3の場合、CSVのダウンロード処理（全項目）
#         if options_select == 3:
    
# else:
#     pass