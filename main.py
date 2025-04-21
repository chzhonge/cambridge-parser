import requests
import csv
import sys
import os
from bs4 import BeautifulSoup

def main():
    if 1 > len(sys.argv):
        print("path is empty.", sys.argv)
        return

    path = sys.argv[1]
    words = []
    word_info_list =  []

    if not os.path.exists(path):
        print(f"Error: File '{path}' not found.")
        return

    with open(path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row[0])

    for d in words:
        word_data = get_cambridge_word_info(d)
        word_info_list.append(word_data)

    with open('word_info.csv', mode='w', newline='', encoding='utf-8') as file:
        # 定義 CSV 欄位標題（即字典中的鍵）
        fieldnames = [
            "單字", 
            "單字說明", 
            "拼音", 
            "詞性", 
            "翻譯", 
            "例句1",
            "例句1(翻譯)",
            "例句2",
            "例句2(翻譯)",
            ]
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for word_info in word_info_list:
            writer.writerow(word_info)

    print("words downloaded successfully.", sys.argv)


def get_cambridge_word_info(word):
    
    # 劍橋字典的網址
    url = f"https://dictionary.cambridge.org/dictionary/english-chinese-traditional/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # 發送 HTTP 請求
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}
    
    # 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 取得單字
    word_element = soup.find("span", class_="hw dhw")
    word_text = word_element.text if word_element else word

    word_description_ele = soup.find("div", class_="def ddef_d db")
    word_description_text = word_description_ele.text.strip() if word_description_ele else "N/A"
    
    # 取得拼音 (IPA 發音)
    pronunciation_element = soup.find("span", class_="ipa")
    pronunciation = pronunciation_element.text if pronunciation_element else "N/A"
    
    # 取得詞性 (形容詞、名詞等)
    pos_element = soup.find("span", class_="pos dpos")
    pos = pos_element.text if pos_element else "N/A"
    
    # 取得所有中文翻譯
    translation_element = soup.find("span", class_="trans dtrans dtrans-se break-cj")
    translation = translation_element.text.strip() if translation_element else "N/A"
    
    examples = []
    example_elements = soup.find_all("div", class_="examp dexamp")
    
    for example in example_elements[:2]:  # 只取前 2 句
        eng_sentence_element = example.find("span", class_="eg")
        eng_sentence = eng_sentence_element.text.strip() if eng_sentence_element else "N/A"
        
        zh_sentence_element = example.find("span", class_="trans dtrans dtrans-se hdb break-cj")
        zh_sentence = zh_sentence_element.text.strip() if zh_sentence_element else "N/A"

        examples.append({
            "例句": eng_sentence,
            "例句翻譯": zh_sentence
        })
    
    example_data = {
        "例句1": examples[0]["例句"] if len(examples) > 0 else "N/A",
        "例句1(翻譯)": examples[0]["例句翻譯"] if len(examples) > 0 else "N/A",
        "例句2": examples[1]["例句"] if len(examples) > 1 else "N/A",
        "例句2(翻譯)": examples[1]["例句翻譯"] if len(examples) > 1 else "N/A",
    }

    word_info = {
        "單字": word_text,
        "單字說明": word_description_text,
        "拼音": pronunciation,
        "詞性": pos,
        "翻譯": translation,
    }

    word_info.update(example_data)
    
    return word_info


if __name__ == "__main__":
    main()