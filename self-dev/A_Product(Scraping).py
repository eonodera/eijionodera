import requests
import re
import openpyxl
import pandas as pd
import os
import datetime

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from bs4 import BeautifulSoup

# TODO:情報を抽出したいASINをリスト化する
asins = ["B089VMCSC2"] #HMB-bulksports "B094J9M6Z5", , EAA-bulksports

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
    today = datetime.date.today()
    print(url)
    print(response)

    try:
        # TODO: 取得したい情報を持っているClassのタグを.find_allメソッドで抽出
        # タグがリストの中に格納される
        asin_title = soup.find_all("span", id="productTitle")
        asin_base_price = soup.find_all("span", id="sns-base-price")
        asin_tiered_price = soup.find_all("span", id="sns-tiered-price")
        asin_store = soup.find_all("a", id="bylineInfo")
        asin_review = soup.find_all("span", id="acrPopover")
        asin_eval = soup.find_all("span", id="acrCustomerReviewText")
        asin_badge_1 = soup.find_all("span", class_="ac-badge-text-primary ac-white")
        asin_badge_2 = soup.find_all("span", class_="ac-badge-text-secondary ac-orange")

        # デバッグ / 使用後コメントアウト
        print(asin_title)
        print(asin_base_price)
        print(asin_tiered_price)
        print(asin_store)
        print(asin_review)
        print(asin_eval)
        print(asin_badge_1)
        print(asin_badge_2)

        # リストの中にdivタグが全て入ってしまう為、一旦リストから取り出す処理
        # bs4.element.ResultSetは.contentsなどのメソッドが使えない
        # indexを活用し、リストの上から〇番目というループを作成している
        unpack_title = asin_title
        unpack_base_price = asin_base_price
        unpack_tiered_price = asin_tiered_price
        unpack_store = asin_store
        unpack_store_link = asin_store
        unpack_asin_review = asin_review
        unpack_asin_eval = asin_eval
        unpack_asin_badge_1 = asin_badge_1
        unpack_asin_badge_2 = asin_badge_2

        # デバッグ / 使用後コメントアウト
        print(unpack_title)
        print(unpack_base_price)
        print(unpack_tiered_price)
        print(unpack_store)
        print(unpack_store_link)
        print(unpack_asin_review)
        print(unpack_asin_eval)
        print(unpack_asin_badge_1)
        print(unpack_asin_badge_2)

        # TODO: 取得したい内容を指定(「aタグの後ろ」とか)
        title = unpack_title.contents
        base_price = unpack_base_price.contents
        tiered_price = unpack_tiered_price.contents
        store = unpack_store.contents
        store_link = unpack_store_link.attrs["href"]
        review = unpack_asin_review.a.span.contents
        evaluation = unpack_asin_eval.contents
        badge_1 = unpack_asin_badge_1.contents
        badge_2 = unpack_asin_badge_2.contents

        # TODO: 取得したデータを加工x,xxx円(str)=>xxxx(int)

        # デバッグ / 使用後コメントアウト
        print(title)
        print(base_price)
        print(tiered_price)
        print(store)
        print(store_link)
        print(review)
        print(evaluation)
        print(badge_1)
        print(badge_2)

        # Dictの形式でitem_infoに格納
        asin_info = {
        "date" : today,
        "product_title" : title,
        "base_price": base_price,
        "tiered_price" : tiered_price,
        "store" : store,
        "store_link" : store_link,
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
        "store_link" : store_link,
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

