import requests
import re
import openpyxl
import pandas as pd
import os
import datetime
import json
import pprint

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from bs4 import BeautifulSoup

# TODO:情報を抽出したいASINをリスト化する
r_items = [
    "https://item.rakuten.co.jp/mrs-chicaco/face-komona-3/",
    "https://item.rakuten.co.jp/dog-kan/9225425/",
    ]

# TODO:
r_items_dic = {}

# TODO:商品URLのループ
for item in r_items:
    # print(item)

    # TODO:ランキング情報を一時的に格納するリスト
    item_lis= []

    # TODO:URL
    url = item

    # URL上の文字列をASINに置換
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    today = datetime.date.today()
    print(url)
    # print(response)

    try:
        # TODO: HTML要素を指定して取得
        ''' APIの情報が取得できたため、不要になったコード
        item_title = soup.find("span", attrs={"class": "normal_reserve_item_name"})
        item_managing_num = soup.find("span", attrs={"class": "normal_reserve_item_number"})
        item_normal_price = soup.find("div", attrs={"id": "priceCalculationConfig"})
        item_dualprice_name = soup.find("div", attrs={"class": "layout-inline-block--1R0y1"})
        item_review = soup.find("div", attrs={"itemtype": "http://schema.org/AggregateRating"})'''

        # item apiのデータをHTML要素から取得
        item_api_data = soup.find("script", attrs={"id" : "item-page-app-data"})

        # デバッグ : 取得できているか
        # print(type(item_api_data))

        # TODO: 取得したい内容を指定(「aタグの後ろ」とか)
        ''' APIの情報が取得できたため、不要になったコード
        # title = item_title.text
        # item_id = item_managing_num.text
        # normal_price = item_normal_price.attrs["data-price"]
        # review_num = item_review.meta.attrs["content"] '''

        # HTMLソース内に記載のあったAPI情報をテキストとして取得
        item_api = item_api_data.text

        # apiのテキストデータをjsonに変換
        json_dict = json.loads(item_api)

        # デバッグ-1 : dictで出力されるか
        # print(json_dict)

        # デバッグ-2 : jsonになっているか
        # print(type(json_dict))

        # デバッグ-3 : pprintで見やすいように整形
        # pprint.pprint(json_dict)

        # デバッグ-4 : jsonのKeyを識別して取得したい項目の選定
        # for key in json_dict:
            # print(key)

        # TODO: 取得項目の選択
        # 取得したい項目の選択 
        mng_num = json_dict["api"]["data"]["itemInfoSku"]["manageNumber"]
        title = json_dict["api"]["data"]["itemInfoSku"]["title"]
        review_num = json_dict["api"]["data"]["itemInfoSku"]["itemReviewInfo"]["summary"]["itemReviewCount"]
        review_score = json_dict["api"]["data"]["itemInfoSku"]["itemReviewInfo"]["summary"]["itemReviewRating"]
        normal_price = json_dict["api"]["data"]["itemInfoSku"]["purchaseInfo"]["purchaseBySellType"]["normalPurchase"]["price"]["minPrice"]
        dual_price_name = json_dict["api"]["data"]["itemInfoSku"]["referencePricePrefix"]
        dual_price = json_dict["api"]["data"]["itemInfoSku"]["taxIncludedReferencePrice"]
        inventory = json_dict["api"]["data"]["itemInfoSku"]["purchaseInfo"]["totalInventory"]
        item_genre = json_dict["rat"]["genericParameter"]["ratItemGenre"]
        item_genre_path = json_dict["rat"]["genericParameter"]["ratItemGenrePath"]
        item_tags = json_dict["rat"]["genericParameter"]["ratItemTag"]

        # Dictの形式でitem_infoに格納
        r_item_info = {
        "mng_num" : mng_num,
        "title" : title,
        "review_num" : review_num,
        "review_score" : review_score,
        "normal_price" : normal_price,
        "dual_price_name" : dual_price_name,
        "dual_price" : dual_price,
        "inventory" : inventory,
        "item_genre" : item_genre,
        "item_genre_path" : item_genre_path,
        "item_tags" : item_tags,
        }

        # デバッグ : ちゃんとDictとして入っているか
        # print(url)
        print(r_item_info)

        # 用意した仮のリストにitem_info(連想配列)をアペンド
        item_lis.append(r_item_info)

    # Keyエラーが発生するのは二重価格表記の部分のため、二重価格がなかったらNAで返す
    except KeyError as _:
        mng_num = json_dict["api"]["data"]["itemInfoSku"]["manageNumber"]
        title = json_dict["api"]["data"]["itemInfoSku"]["title"]
        review_num = json_dict["api"]["data"]["itemInfoSku"]["itemReviewInfo"]["summary"]["itemReviewCount"]
        review_score = json_dict["api"]["data"]["itemInfoSku"]["itemReviewInfo"]["summary"]["itemReviewRating"]
        normal_price = json_dict["api"]["data"]["itemInfoSku"]["purchaseInfo"]["purchaseBySellType"]["normalPurchase"]["price"]["minPrice"]
        # dual_price_name = json_dict["api"]["data"]["itemInfoSku"]["referencePricePrefix"]
        # dual_price = json_dict["api"]["data"]["itemInfoSku"]["taxIncludedReferencePrice"]
        dual_price = "n/a" 
        dual_price_name = "n/a" 
        inventory = "SKU_Type"
        item_genre = json_dict["rat"]["genericParameter"]["ratItemGenre"]
        item_genre_path = json_dict["rat"]["genericParameter"]["ratItemGenrePath"]
        item_tags = json_dict["rat"]["genericParameter"]["ratItemTag"]

        r_item_info = {
        "mng_num" : mng_num,
        "title" : title,
        "review_num" : review_num,
        "review_score" : review_score,
        "normal_price" : normal_price,
        "dual_price_name" : dual_price_name,
        "dual_price" : dual_price,
        "inventory" : inventory,
        "item_genre" : item_genre,
        "item_genre_path" : item_genre_path,
        "item_tags" : item_tags,
        }

        # デバッグ : ちゃんとDictとして入っているか
        # print(url)
        print(r_item_info)

        # 用意した仮のリストにitem_info(連想配列)をアペンド
        item_lis.append(r_item_info)
        # continue

    # TODO: rank_itemsは次のループで消えてしまう為、rank_itemsをcategories_rank_itemsとして保管
    r_items_dic[item] = item_lis
    print(r_items_dic[item])

    # TODO:Create DataFrame
    df = pd.DataFrame(r_items_dic[item])
    print(df)

    # TODO:Excelが存在しているか確認
    if not os.path.exists("Python-SelfDev\R_product.xlsx"):
        # 無ければExcelを作成
        wb = Workbook()
        wb.save("Python-SelfDev\R_product.xlsx")

    # 最終行を取得するための変数: defaltを0にセット
    row_num = 0

    # Excel、sheet(カテゴリID)が存在していれば
    try:
        df2 = pd.read_excel("Python-SelfDev\R_product.xlsx", sheet_name=mng_num)
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
        with pd.ExcelWriter("Python-SelfDev\R_product.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=mng_num, startrow=0, header=True)

    else:
        with pd.ExcelWriter("Python-SelfDev\R_product.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=mng_num, startrow=row_num+1, header=False)


# """
# *******************
# ここからはMySQLにデータを蓄積させる為のコードを書く
# *******************
# """

# # TODO: MySQLにデータとして格納していく

# # TODO: MySQLのデータにアクセスしてExcelに抽出する/Pandas? 

# # TODO: 装飾する/Openpyxl or 関数

