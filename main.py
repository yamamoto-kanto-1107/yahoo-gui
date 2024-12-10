# seleniumの必要なライブラリをインポート
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

import time
# pandasライブラリーのインポート
import pandas as pd
import random
import os

def insertDataToYahoo(insertArr,judge,phoneNumber,IdNum,testMode):

    # csvファイルのファイルパスを引数に渡す
  # df = pd.read_csv('../../csv/syupin.csv', encoding='cp932')
  # # 列の行数
  # number_of_cols = df.shape[1]
  # # カラムのラベルが入った配列
  # col_name = df.columns

  judgeTF = judge
  # Chrome Webドライバー の インスタンスを生成
  driver = webdriver.Chrome()

  # WebドライバーでQiitaログインページを起動
  driver.get('https://login.yahoo.co.jp/config/login?.src=auc&lg=jp&.intl=jp&.done=https%3A%2F%2Fauctions.yahoo.co.jp%2F')

  id_input = driver.find_element(By.ID,"login_handle")
  id_input.send_keys(phoneNumber)

  next_btn = driver.find_element(By.CLASS_NAME,"ar-button_button_J2jv2")
  next_btn.click()

  wait = WebDriverWait(driver, 100)
  wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mhdPcLogo')))

  for row in insertArr:
    try:
      wait_range_from = 1.0 # 操作間の待ち時間幅下限値
      wait_range_to = 10.0 # 操作間の待ち時間幅上限値
      title = row[3]
      category = row[1]
      condition = "" #初期化

      match int(row[39]):
        case 1:
            condition = "未使用"
        case 2:
            condition = "未使用に近い"
        case 3:
            condition = "目立った傷や汚れなし"
        case 4:
            condition = "やや傷や汚れあり"
        case 5:
            condition = "傷や汚れあり"
        case 6:
            condition = "全体的に状態が悪い"
      description = row[5]
      location = row[45]
      ship_cost = row[47]

      ship_way = row[58]

      # 配送方法は最初にフラグが立っているものを採用
      for i in range(50,55):
        if(row[i] == 1):
          match i:
            case 51:
              # 宅急便
              # 荷物のサイズが7,8,9または荷物の重さが7の場合は3
              if (row[56]in [7,8,9]) or (row[57] == 7):
                ship_way = 3
              else:
                # 上記以外は2
                ship_way = 2
              break
            case 52:
              # 宅急便コンパクト
              ship_way = 1
              break
            case 53:
              # ネコポス
              ship_way = 0
              break
            case 54:
              # ゆうパック
              ship_way = 7
              break
            case 55:
              # ゆうパケット
              ship_way = 5
              break
            case 56:
              # ゆうパケットポストmini
              ship_way = 4
              break
      match int(row[49]):
        case 1:
            ship_lag = "1〜2日"
        case 2:
            ship_lag = "2〜3日"
        case 3:
            ship_lag = "3〜7日"

      match int(row[31]):
        case 9:
            closing_date = "8"
        case 10:
            closing_date = "9"
        case 11:
            closing_date = "10"
        case 12:
            closing_date = "11"
        case 13:
            closing_date = "12"
        case 14:
            closing_date = "13"
        case 15:
            closing_date = "14"
        case 16:
            closing_date = "15"
        case 17:
            closing_date = "16"
        case 18:
            closing_date = "17"
        case 19:
            closing_date = "18"
        case 20:
            closing_date = "19"
        case 21:
            closing_date = "20"
        case 22:
            closing_date = "21"
        case 23:
            closing_date = "22"
        case 24:
            closing_date = "23"

      driver.get('https://auctions.yahoo.co.jp/jp/show/submit?category=0')
      wait = WebDriverWait(driver, 2)
      try:
        wait.until(EC.element_to_be_clickable((By.ID, 'js-CampaignPRModal_submit')))
        driver.find_element(By.ID,"js-CampaignPRModal_submit").click()
      except:
        print('no campaign')

      # 【画像の設定】
      imagePathString = ""
      for i in range(6,15):
        if (pd.isna(row[i])):
          continue
        if i != 7:
          imagePathString += '\n'
        imagePathString += row[i]
      if(imagePathString == ""):
        print(f"画像データがないため、処理をスキップします{row[0]}行目")
        # csvの次の行へ処理を移る
        continue
      imagePathString = imagePathString.strip() #画像が１つの時余分な空白があるため空白削除

      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      selectFileMultiple = driver.find_element(By.ID,"selectFileMultiple")

      selectFileMultiple.send_keys(imagePathString)

      # 【商品名の設定】
      # ランダムなウェイト
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      fleaTitleForm = driver.find_element(By.ID,"fleaTitleForm")
      fleaTitleForm.send_keys(title)

      # 【カテゴリの設定】
      wait_time = random.uniform(wait_range_from, wait_range_to) # ランダムなウェイト
      time.sleep(wait_time)
      driver.execute_script(f'arguments[0].value = {category}', driver.find_element(By.NAME,'category'))

      # 【商品の状態の設定】
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      select = Select(driver.find_element(By.NAME, 'istatus'))
      select.select_by_visible_text(condition)

      # 【説明の設定】
      # 説明 iframeのrteEditorComposition0に切り替え
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      iframe = driver.find_element(By.ID,'rteEditorComposition0')
      driver.switch_to.frame(iframe)
      driver.find_element(By.ID,'0').send_keys(description)
      driver.switch_to.default_content()


      #説明HTML入力
      html_tag = driver.find_element(By.CLASS_NAME,'descriptionArea__link')
      html_tag.click()

      html_textarea = driver.find_element(By.NAME,'Description_plain_work')
      if category == "2084009286":
        confirmHTML='''
          <table cellspacing="3" cellpadding="4" border="0" width="100%">
          <tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □商品詳細      </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">    
          ・商品は、A4サイズ（210×297mm）のイラストポスターです。<br><br>

          ・当方がAIで作成したオリジナルの美女イラスト（サンプル画像）を高解像度にアップスケールし、<br>
          　厚手の光沢写真用紙に印刷した商品です。<br><br>

          ・最高級品質の高画質でフチなし印刷にてプリントアウトし、<br>
          　丁寧に梱包して発送いたします！<br><br>

          ・お届けする実物のポスターには、「sample」の文字は入りません。<br><br>

          ※当アカウントで販売する商品は、全て作成時に年齢設定を18歳以上にしております。<br>
          全て当方がAIで作成したオリジナル作品（サンプルのため画質を下げてアップロードしています。）ですので、安心してご入札ください。<br><br>

          </font></td></tr></tbody></table>
          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □梱包について      </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">      

          ・おてがる配送ゆうパケット（全国一律230円）にて匿名発送いたします。<br>
          　商品名は「ポスター」と記載いたします。  <br><br>

          ・商品はクリアファイル（またはOPP袋）、板段ボール、防水宅配ビニール袋にて丁寧に梱包し発送いたします。<br>
          ※外側から中身が見えないよう、プライバシーに配慮した梱包で発送いたします。<br><br>


            </font></td></tr></tbody></table>


          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □発送について     </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">      

          ・通常、お支払いから1～3日以内に発送いたします。  <br><br>

          ・万が一、発送が遅れる場合は、事前にご連絡いたしますのでご了承ください。<br><br>

            </font></td></tr></tbody></table>

          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □複数購入について    </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">      

          ・72時間以内に落札した商品は、お支払い前に限りまとめて発送が可能です。<br>
          　落札時に取引メッセージにて、その旨をご連絡ください。  <br><br>

          ・最大で15枚まで同梱発送可能です。<br><br>

          ・落札後に「まとめて取引」のボタンが表示されますので、必ず「落札者様にて操作」をお願いします。<br><br>

          ※操作がない場合、個別配送となりますのでご注意ください。<br>
          ※ヤフオクのシステム上、カテゴリーが異なる場合はまとめて取引ができません。<br>
          カテゴリーごとにまとめて取引申請をお願いいたします。<br>
          <br><br>

            </font></td></tr></tbody></table>

          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □お支払い期限について </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">      

          ・いたずら入札防止のため、72時間以内にお手続きを行っていただけない場合には、<br>
          　大変申し訳ございませんが落札者都合により削除させていただきます。

          <br><br>

            </font></td></tr></tbody></table>

          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □注意事項 </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">    
            
          ※ご使用のPCモニターやスマホによって、色の濃淡や画質が実物と異なる場合があります。<br><br>
          ※プリンターでの印刷の都合上、画像と色味が若干異なることがあります。この点をご理解のうえでご入札をお願いします。<br><br>
          ※フチなし印刷のため、サンプル画像に比べて数ミリ程度外周部分が印刷されません。<br>
          　ご了承ください。<br><br>
          ※若干の傷や擦れ、インク汚れがある場合がありますので、ご了承ください。<br><br>

          その他ご不明な点がございましたら、お気軽にお問い合わせください。
          <br><br>

            </font></td></tr></tbody></table>



          最後までお読みいただき、ありがとうございました。

        '''
      else :
         confirmHTML=f'''
            <table cellspacing="3" cellpadding="4" border="0" width="100%">
          <tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □商品詳細      </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">    
          ・商品は、A4サイズ（210×297mm）のイラストポスターです。<br><br>

          アダルトカテゴリーの作品はブラウザからしか見られないので、下記のリンクからご覧ください↓<br>
          <a href="https://auctions.yahoo.co.jp/seller/{IdNum}?sid={IdNum}&auccat=26146&is_postage_mode=1&dest_pref_code=27&b=1&n=50">アダルト商品を見る</a><br><br>

          ※アダルト画像は陰部にのみボカシが入ります<br><br>

          ・当方がAIで作成したオリジナルの美女イラスト（サンプル画像）を高解像度にアップスケールし、<br>
          　厚手の光沢写真用紙に印刷した商品です。<br><br>

          ・最高級品質の高画質でフチなし印刷にてプリントアウトし、<br>
          　丁寧に梱包して発送いたします！<br><br>

          ・お届けする実物のポスターには、「sample」の文字は入りません。<br><br>

          ※当アカウントで販売する商品は、全て作成時に年齢設定を18歳以上にしております。<br>
          全て当方がAIで作成したオリジナル作品（サンプルのため画質を下げてアップロードしています。）ですので、安心してご入札ください。<br><br>

          </font></td></tr></tbody></table>
          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □梱包について      </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">      

          ・おてがる配送ゆうパケット（全国一律230円）にて匿名発送いたします。<br>
          　商品名は「ポスター」と記載いたします。  <br><br>

          ・商品はクリアファイル（またはOPP袋）、板段ボール、防水宅配ビニール袋にて丁寧に梱包し発送いたします。<br>
          ※外側から中身が見えないよう、プライバシーに配慮した梱包で発送いたします。<br><br>


            </font></td></tr></tbody></table>


          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □発送について     </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">      

          ・通常、お支払いから1～3日以内に発送いたします。  <br><br>

          ・万が一、発送が遅れる場合は、事前にご連絡いたしますのでご了承ください。<br><br>

            </font></td></tr></tbody></table>

          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □複数購入について    </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">      

          ・72時間以内に落札した商品は、お支払い前に限りまとめて発送が可能です。<br>
          　落札時に取引メッセージにて、その旨をご連絡ください。  <br><br>

          ・最大で15枚まで同梱発送可能です。<br><br>

          ・落札後に「まとめて取引」のボタンが表示されますので、必ず「落札者様にて操作」をお願いします。<br><br>

          ※操作がない場合、個別配送となりますのでご注意ください。<br>
          ※ヤフオクのシステム上、カテゴリーが異なる場合はまとめて取引ができません。<br>
          カテゴリーごとにまとめて取引申請をお願いいたします。<br>
          <br><br>

            </font></td></tr></tbody></table>

          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □お支払い期限について </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">      

          ・いたずら入札防止のため、72時間以内にお手続きを行っていただけない場合には、<br>
          　大変申し訳ございませんが落札者都合により削除させていただきます。

          <br><br>

            </font></td></tr></tbody></table>

          <table cellspacing="3" cellpadding="4" border="0" width="100%"><tbody><tr><td bgcolor="#ffc0cb" colspan="2" align="left"><b><font color="#000000" size="3">      □注意事項 </font></b></td></tr><tr><td width="5%"></td><td width="95%" align="left"><font color="#333333" size="3">    
            
          ※ご使用のPCモニターやスマホによって、色の濃淡や画質が実物と異なる場合があります。<br><br>
          ※プリンターでの印刷の都合上、画像と色味が若干異なることがあります。この点をご理解のうえでご入札をお願いします。<br><br>
          ※フチなし印刷のため、サンプル画像に比べて数ミリ程度外周部分が印刷されません。<br>
          　ご了承ください。<br><br>
          ※若干の傷や擦れ、インク汚れがある場合がありますので、ご了承ください。<br><br>

          その他ご不明な点がございましたら、お気軽にお問い合わせください。
          <br><br>

            </font></td></tr></tbody></table>

          最後までお読みいただき、ありがとうございました。
        '''
      html_textarea.send_keys(confirmHTML)

      # 【発送元の地域の設定】
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      Select(driver.find_element(By.NAME,"loc_cd")).select_by_value(f'{location}')

      radios = driver.find_elements(By.CLASS_NAME,"Radio__label")
      if ship_cost == 0:
        radios[1].click()
      elif ship_cost == 1:
        radios[0].click()
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      shipmethod_dummy = driver.find_elements(By.CLASS_NAME,"OfficialDelivery__item")

      # 【配送方法の設定】
      # row[51]お手軽配送
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)

      # shipmethod_dummy[ship_way].click()

      # 【支払いから発送までの日数】
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      Select(driver.find_element(By.NAME,"shipschedule")).select_by_visible_text(ship_lag)

      # 【終了日時-日付】
      # 今日の日付から開催日数分日付をずらしたものを選択
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      today = pd.Timestamp.now().normalize()
      days_later = today + pd.Timedelta(days=int(row[30]))
      Select(driver.find_element(By.ID,"ClosingYMD")).select_by_value(days_later.strftime('%Y-%m-%d'))

      # 【終了日時-時刻】
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      Select(driver.find_element(By.ID,"ClosingTime")).select_by_value(closing_date)

      # 【開始価格の設定】
      # オークションで固定
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      radios[0].click()

      # 【開始価格の設定】
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      driver.find_element(By.NAME, "StartPrice").send_keys(f"{int(row[27])}")

      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      click_overhead = driver.find_elements(By.CLASS_NAME,"Overhead__title--fontNormal")[1]
      # driver.find_element(By.CLASS_NAME,"Overhead js-toggleExpand").click()

      #要素が有効であるか
      if click_overhead.is_enabled():
        print('is enable')

      #要素が存在しているか
      if click_overhead.is_displayed():
        print('click')
        click_overhead.click()
      else:
        print('no such element')

      # 【即決価格の設定】
      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)
      if not pd.isna(int(row[28])):
        driver.find_element(By.ID, "auc_BidOrBuyPrice_auction").send_keys(int(row[28]))

      wait_time = random.uniform(wait_range_from, wait_range_to)
      time.sleep(wait_time)

      if testMode == True or testMode == 'True':
        print('テストモードを終了します')
        time.sleep(200)
        return
      driver.find_element(By.ID,"submit_form_btn").click()

      # print('step11')
      #出品ボタン
      wait_time = random.uniform(wait_range_from, wait_range_to)
      submitBtn = driver.find_element(By.CLASS_NAME,'Button--submit2')
      submitBtn.click()

      wait_time = random.uniform(wait_range_from, wait_range_to)
      continueId = driver.find_element(By.ID, 'modFootLink')
      continueBtn = continueId.find_element(By.TAG_NAME,'a')
      continueBtn.click()

      try:
        wait.until(EC.element_to_be_clickable((By.ID, 'js-CampaignPRModal_submit')))
        driver.find_element(By.ID,"js-CampaignPRModal_submit").click()
      except:
        print('no campaign')

      # time.sleep(200)

    except Exception as e:
      print('error')
      print(f"予期しないエラーが発生しました: {e}")
      time.sleep(200)


