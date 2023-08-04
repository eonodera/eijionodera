import requests
import re
import openpyxl
import pandas as pd
import os
import datetime
import urllib3

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from bs4 import BeautifulSoup
from lxml import html

# TODO:情報を抽出したいASINをリスト化する
asins = ["B094J9M6Z5", "B089VMCSC2"] #HMB-bulksports, EAA-bulksports

# TODO:
asins_rank_items = {}

# TODO:情報を抽出するループ
for asin in asins:
    print(asin)

    # TODO:ランキング情報を一時的に格納するリスト
    item_asins = []

    # TODO:ASINをURLの中に入れ込みDPのURLを完成させる
    pre_url = "https://www.amazon.co.jp/dp/product_asin"
    # URL上の文字列をASINに置換
    url = pre_url.replace("product_asin", asin)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lxml = html.fromstring(str(soup))
    today = datetime.date.today()
    print(url)
    print(response)

    try:
        # TODO: 取得したい情報を持っているClassのタグを.find_allメソッドで抽出
        # タグがリストの中に格納される
        asin_title = soup.find("span", attrs={"id": "productTitle"})
        asin_base_price = lxml.xpath("//*[@id='sns-base-price']/text()") # soup.find("span", attrs={"id": "sns-base-price"})
        asin_tiered_price = lxml.xpath("//*[@id='sns-tiered-price']/text()") # soup.find("span", attrs={"id": "sns-tiered-price"})
        asin_store = soup.find("a", attrs={"id": "bylineInfo"})
        asin_review = soup.find("span", attrs={"id": "acrPopover"})
        asin_eval = soup.find("span", attrs={"id": "acrCustomerReviewText"})
        asin_badge_1 = soup.find("span", attrs={"class": "ac-badge-text-primary"})
        asin_badge_2 = soup.find("span", attrs={"class": "ac-badge-text-secondary"})

        # TODO: 取得したい内容を指定(「aタグの後ろ」とか)
        title = asin_title.text
        base_price = asin_base_price
        tiered_price = asin_tiered_price
        store = asin_store.text
        review = asin_review.a.span.text
        evaluation = asin_eval.text
        badge_1 = asin_badge_1.text
        badge_2 = asin_badge_2.text

        # unpack_title = title[0]
        unpack_base_price = base_price[0]
        unpack_tiered_price = tiered_price[0]

        # TODO: 正規表現で空白の削除
        title_re = re.sub(r'\s+', '', title)
        base_price_re = re.sub(r'\s+', '', unpack_base_price)
        tiered_price_re = re.sub(r'\s+', '', unpack_tiered_price)

        # TODO: 取得したデータを加工x,xxx円(str)=>xxxx(int)        

        # デバッグ / 使用後コメントアウト
        print(title_re)
        print(base_price_re)
        print(tiered_price_re)
        print(store)
        print(review)
        print(evaluation)
        print(badge_1)
        print(badge_2)

        # Dictの形式でitem_infoに格納
        asin_info = {
        "date" : today,
        "product_title" : title_re,
        "base_price": base_price_re,
        "tiered_price" : tiered_price_re,
        "store" : store,
        "review" : review,
        "evaluation" : evaluation,
        "badge_1" : badge_1,
        "badge_2" : badge_2,
        }
        print(url)
        print(asin_info)

        # 用意した仮のリストにitem_info(連想配列)をアペンド
        item_asins.append(asin_info)

        # TODO: 7/20はここまで、デバッグしてないので挙動不明

    except AttributeError as _:
        print("break文に入ります")
        asin_badge_1 = "n/a" 
        asin_badge_2 = "n/a" 

        asin_info = {
        "date" : today,
        "product_title" : title,
        "base_price": base_price,
        "tiered_price" : tiered_price,
        "store" : store,
        # "store_link" : store_link,
        "review" : review,
        "evaluation" : evaluation,
        "badge_1" : badge_1,
        "badge_2" : badge_2,
        }

        item_asins.append(asin_info)
        continue

    # TODO: rank_itemsは次のループで消えてしまう為、rank_itemsをcategories_rank_itemsとして保管
    asins_rank_items[asin] = item_asins
    print(asins_rank_items[asin])

    # TODO:Create DataFrame
    df = pd.DataFrame(asins_rank_items[asin])
    print(df)

    # TODO:Excelが存在しているか確認
    if not os.path.exists("Python-SelfDev\A_product.xlsx"):
        # 無ければExcelを作成
        wb = Workbook()
        wb.save("Python-SelfDev\A_product.xlsx")

    # 最終行を取得するための変数: defaltを0にセット
    row_num = 0

    # Excel、sheet(カテゴリID)が存在していれば
    try:
        df2 = pd.read_excel("Python-SelfDev\A_product.xlsx", sheet_name=asin)
        # 最終行を取得する
        row_num = len(df2)
        # # デバッグ：カテゴリIDのシートと最終行が取得できてるか
        # print(category)
        # print(row_num)
    
    # もしエラーがでたら何もしない処理
    except ValueError as _:
        pass

    # Excelの最終行を取得＆情報の追記＆ヘッダー項目の非表示
    # TODO: もしrow_numが0だったらヘッダーをTrue, startrowを0
    if row_num == 0:
        with pd.ExcelWriter("Python-SelfDev\A_product.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=asin, startrow=0, header=True)

    else:
        with pd.ExcelWriter("Python-SelfDev\A_product.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=asin, startrow=row_num+1, header=False)


# """
# *******************
# ここからはMySQLにデータを蓄積させる為のコードを書く
# *******************
# """

# # TODO: MySQLにデータとして格納していく

# # TODO: MySQLのデータにアクセスしてExcelに抽出する/Pandas? 

# # TODO: 装飾する/Openpyxl or 関数

