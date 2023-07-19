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
asins = ["B094J9M6Z5", "B089VMCSC2"] #HMB-bulksports, EAA-bulksports

# TODO:
asins_rank_items = {}

# TODO:情報を抽出するループ
for asin in asins:
    #print(category)

    # TODO:ランキング情報を一時的に格納するリスト
    item_asins = []
    index = 0

    # TODO:(ループ) 
    while index < 10:

        # TODO:ASINをURLの中に入れ込みDPのURLを完成させる
        pre_url = "https://www.amazon.co.jp/dp/product_asin"
        # URL上の文字列をASINに置換
        url = pre_url.replace("product_asin", asin)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        today = datetime.date.today()
        #print(url)

        try:
            # TODO: 取得したい情報を持っているClassのタグを.find_allメソッドで抽出
            # タグがリストの中に格納される
            asin_title = soup.find_all("span", id="productTitle")
            asin_base_price = soup.find_all("span", id="sns-base-price")
            asin_tiered_price = soup.find_all("span", id="sns-tiered-price")
            store = soup.find_all("a", id="bylineInfo")
            # store_link = soup.find_all("div", class_="rnkRanking_shop", limit=10)
            # elem_price = soup.find_all("div", class_="rnkRanking_price", limit=10)
            print(asin_title)
            print(asin_base_price)
            print(asin_tiered_price)

            # リストの中にdivタグが全て入ってしまう為、一旦リストから取り出す処理
            # bs4.element.ResultSetは.contentsなどのメソッドが使えない
            # indexを活用し、リストの上から〇番目というループを作成している
            unpack_title = asin_title[index]
            unpack_base_price = asin_base_price[index]
            unpack_tiered_price = asin_tiered_price[index]
            # unpack_review = elem_review[index]
            # unpack_shop = elem_shop[index]
            # unpack_price = elem_price[index]
            print(index)
            print(asin)
            print(unpack_title)
            print(unpack_base_price)
            print(unpack_tiered_price)

            # TODO: 取得したい内容を指定(「aタグの後ろ」とか)
            title = unpack_title.contents
            base_price = unpack_base_price.contents
            tiered_price = unpack_tiered_price.contents
            # item_review = unpack_review.a.contents
            # item_review_link = unpack_review.a.attrs["href"]
            # shop = unpack_shop.a.contents
            # shop_link = unpack_shop.a.attrs["href"]
            # item_price = unpack_price.contents

            # TODO: 取得したデータを加工x,xxx円(str)=>xxxx(int)

            # デバッグ
            print(title)
            print(base_price)
            print(tiered_price)
            # print(item_img)
            # print(item_review)
            # print(item_review_link)
            # print(shop)
            # print(shop_link)
            # print(item_price)

            # Dictの形式でitem_infoに格納
            asin_info = {
                "date" : today,
                "product_title" : title,
                "base_price": base_price,
                "tiered_price" : tiered_price,
                # "item_review" : item_review,
                # "item_review_link" : item_review_link,
                # "shop" : shop,
                # "shop_link" : shop_link,
                # "item_price" : item_price,
            }
            print(url)
            print(asin_info)

            # 用意した仮のリストにitem_info(連想配列)をアペンド
            item_asins.append(asin_info)

            # HTML要素の番号に1足す
            index += 1

        # TODO: 7/20はここまで、デバッグしてないので挙動不明

        except AttributeError as _:
            item_review = "n/a" 
            item_review_link = "n/a" 

            item_info = {
                "date" : today,
                "title" : title,
                "item_link": item_link,
                "item_img" : item_img,
                "item_review" : item_review,
                "item_review_link" : item_review_link,
                "shop" : shop,
                "shop_link" : shop_link,
                "item_price" : item_price,
            }

            rank_items.append(item_info)

            index += 1
            continue

    # TODO: rank_itemsは次のループで消えてしまう為、rank_itemsをcategories_rank_itemsとして保管
    categories_rank_items[category] = rank_items
    # print(categories_rank_items[category])

    # TODO:Create DataFrame
    df = pd.DataFrame(categories_rank_items[category])
    #print(df)

    # TODO:Excelが存在しているか確認
    if not os.path.exists("Python-SelfDev\R_Ranking_Daily.xlsx"):
        # 無ければExcelを作成
        wb = Workbook()
        wb.save("Python-SelfDev\R_Ranking_Daily.xlsx")

    # 最終行を取得するための変数: defaltを0にセット
    row_num = 0

    # Excel、sheet(カテゴリID)が存在していれば
    try:
        df2 = pd.read_excel("Python-SelfDev\R_Ranking_Daily.xlsx", sheet_name=category)
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
        with pd.ExcelWriter("Python-SelfDev\R_Ranking_Daily.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=category, startrow=0, header=True)

    else:
        with pd.ExcelWriter("Python-SelfDev\R_Ranking_Daily.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=category, startrow=row_num+1, header=False)


"""
*******************
ここからはMySQLにデータを蓄積させる為のコードを書く
*******************
"""

# TODO: MySQLにデータとして格納していく

# TODO: MySQLのデータにアクセスしてExcelに抽出する/Pandas? 

# TODO: 装飾する/Openpyxl or 関数

