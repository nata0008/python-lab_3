from googletrans import Translator, LANGUAGES
import asyncio
import time

translator = Translator()

# 3.1 переклад
async def TransLate(text, lang):
    try:
        code = CodeLang(lang)
        result = await translator.translate(text, dest=code)
        return result.text
    except:
        return "Помилка перекладу"

# 3.2 визначення мови
async def LangDetect(txt):
    try:
        res = await translator.detect(txt)
        return res.lang, res.confidence
    except:
        return "unknown", 0

# 3.3 код мови
def CodeLang(lang):

    lang = lang.lower()

    if lang in LANGUAGES:
        return lang

    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code

    return None

# асинхронна обробка речення
async def async_translate(sentence, lang):
    return await TransLate(sentence, lang)

#ОСНОВНА ПРОГРАМА
async def main():

    file_name = "v-18.txt"
    target_lang = "spanish"

    # читання файлу
    try:
        f = open(file_name, "r", encoding="utf-8")
        text = f.read()
        f.close()
        print("Файл:", file_name)
    except:
        print("Помилка читання файлу")
        return

    # список речень
    TxtList = [s.strip() for s in text.split(".") if s.strip()]

    print("Кількість символів:", len(text))
    print("Кількість речень:", len(TxtList))

    # визначення мови тексту
    lang, conf = await LangDetect(text)

    print("Мова тексту:", LANGUAGES.get(lang))
    print("Код мови:", lang)
    print("Confidence:", conf)

    print("\nОригінальний текст:")
    print(text)

    code = CodeLang(target_lang)

    print("\nМова перекладу:", LANGUAGES.get(code))
    print("Код мови перекладу:", code)

    # 3.4.1 ПОСЛІДОВНИЙ ПЕРЕКЛАД
    start = time.time()

    translations = []

    for s in TxtList:
        tr = await TransLate(s, target_lang)
        translations.append(tr)

    end = time.time()

    print("\nПереклад тексту:")
    print(". ".join(translations))

    print("\nЧас (без асинхронності):", end - start)

    #3.4.2 АСИНХРОННИЙ ПЕРЕКЛАД
    start = time.time()

    tasks = []

    for s in TxtList:
        tasks.append(async_translate(s, target_lang))

    result = await asyncio.gather(*tasks)

    end = time.time()

    print("\nАсинхронний переклад:")
    print(". ".join(result))

    print("\nЧас (асинхронний):", end - start)


asyncio.run(main())