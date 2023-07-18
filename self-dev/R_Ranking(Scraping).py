import requests
import re
import openpyxl
import pandas as pd
import os
import datetime

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from bs4 import BeautifulSoup

# TODO:ランキングを抽出したいカテゴリ番号をリスト化する
categories = ["215783", "100554"] # 215783日用品雑貨 100554生活雑貨

# TODO:
categories_rank_items = {}

# TODO:カテゴリごとの抽出が終わったら次のカテゴリへというループを作る
for category in categories:
    #print(category)

    # TODO:ランキング情報を一時的に格納するリスト
    rank_items = []
    index = 0

    # TODO:(ループ) Daily Ranking 上位5件まで
    while index < 3:

        # TODO:配列からカテゴリ番号を取り出してURLに格納
        pre_url = "https://ranking.rakuten.co.jp/daily/category/"
        # URL上の文字列をカテゴリIDに置換
        url = pre_url.replace("category", category)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        #print(url)

        try:
            # 取得したい情報を持っているClassのタグを.find_allメソッドで抽出
            # タグがリストの中に格納される
            # find_allすると全件取得してしまう為、limitで制限をかける
            elem = soup.find_all("div", class_="rnkRanking_itemName", limit=3)
            elem_img = soup.find_all("div", class_="rnkRanking_imageBox", limit=3)
            elem_review = soup.find_all("div", class_="rnkRanking_starBox", limit=3)
            elem_shop = soup.find_all("div", class_="rnkRanking_shop", limit=3)
            elem_price = soup.find_all("div", class_="rnkRanking_price", limit=3)
            #print(elem_shop)
            #print(type(elem))

            # リストの中にdivタグが全て入ってしまう為、一旦リストから取り出す処理
            # bs4.element.ResultSetは.contentsなどのメソッドが使えない
            # indexを活用し、リストの上から〇番目というループを作成している
            unpack_title = elem[index]
            unpack_item_link = elem[index]
            unpack_item_img = elem_img[index]
            unpack_review = elem_review[index]
            unpack_shop = elem_shop[index]
            unpack_price = elem_price[index]
            #print(unpack_title)

            # 取得したい内容を指定(「aタグの後ろ」とか)
            title = unpack_title.a.contents
            item_link = unpack_item_link.a.attrs["href"]
            item_img = unpack_item_img.img.attrs["src"]
            item_review = unpack_review.a.contents
            item_review_link = unpack_review.a.attrs["href"]
            shop = unpack_shop.a.contents
            shop_link = unpack_shop.a.attrs["href"]
            item_price = unpack_price.contents

            # # デバッグ
            # print(title)
            # print(item_link)
            # print(item_img)
            # print(item_review)
            # print(item_review_link)
            # print(shop)
            # print(shop_link)
            # print(item_price)

            # Dictの形式でitem_infoに格納
            item_info = {
                "title" : title,
                "item_link": item_link,
                "item_img" : item_img,
                "item_review" : item_review,
                "item_review_link" : item_review_link,
                "shop" : shop,
                "shop_link" : shop_link,
                "item_price" : item_price,
            }
            #print(url)
            #print(item_info)

            # 用意した仮のリストにitem_info(連想配列)をアペンド
            rank_items.append(item_info)

            # HTML要素の番号に1足す
            index += 1

        except AttributeError as _:
            break

    # rank_itemsは次のループで消えてしまう為、rank_itemsをcategories_rank_itemsとして保管
    categories_rank_items[category] = rank_items
    # print(categories_rank_items[category])

    # TODO:Create DataFrame
    df = pd.DataFrame(categories_rank_items[category])
    #print(df)

    # TODO:Excelが存在しているか確認
    if not os.path.exists("venv\Python-SelfDev\R_Ranking_Daily.xlsx"):
        # 無ければExcelを作成
        wb = Workbook()
        wb.save("venv\Python-SelfDev\R_Ranking_Daily.xlsx")

    # 最終行を取得するための変数: defaltを0にセット
    row_num = 0

    # Excel、sheet(カテゴリID)が存在していれば
    try:
        df2 = pd.read_excel("venv\Python-SelfDev\R_Ranking_Daily.xlsx", sheet_name=category)
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
        with pd.ExcelWriter("venv\Python-SelfDev\R_Ranking_Daily.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=category, startrow=0, header=True)

    else:
        with pd.ExcelWriter("venv\Python-SelfDev\R_Ranking_Daily.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=category, startrow=row_num+1, header=False)


# TODO:データ取得日をcolumn:Bに追記する

"""
*******************
ここからはMySQLにデータを蓄積させる為のコードを書く
*******************
"""

# TODO: MySQLにデータとして格納していく

# TODO: MySQLのデータにアクセスしてExcelに抽出する/Pandas? 

# TODO: 装飾する/Openpyxl or 関数

