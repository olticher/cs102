import config
import gensim
import pymorphy2
import pyLDAvis
import pyLDAvis.gensim
import re
import requests

from stop_words import get_stop_words
from string import punctuation


stop_words = get_stop_words('russian')


def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
):
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """

    code = ("return API.wall.get({" +
        f"'owner_id': '{owner_id}'," +
        f"'domain': '{domain}'," +
        f"'offset': {offset}," +
        f"'count': {count}," +
        f"'filter': '{filter}'," +
        f"'extended': {extended}," +
        f"'fields': '{fields}'," +
        f"'v': {v}," +
    "});")

    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG['access_token'],
            "v": v
            }
    )

    walls = []
    for i in range(count):
        try:
            walls.append(response.json()['response']['items'][i]['text'])
        except:
            break

    return walls


def del_stopwords(text): #удаление стоп-слов
    text = [[j for j in text[k] if j not in stop_words] for k in range(len(text))]
    return text


def del_symbols(text):
    upd_text = []
    new_text = []
    for j in text:
        for word in j:
            word = ''.join(ch for ch in word if ch not in punctuation and ch != '«' and ch != '»') # удаление знаков препинания
            emoji_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F"  # emoticons
                                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       "]+", flags=re.UNICODE)
            if not word.isalpha():  # удаляем цифры
                continue
            if len(word) > 15:  # удаляем длинные слова
                continue
            upd_text.append(emoji_pattern.sub(r'', word))  # удаляем эмодзи
        new_text.append(upd_text)
        upd_text = []
    return new_text


def del_links(text): #удаление ссылок
    upd_text = []
    new_text = []
    for j in text:
        for word in j:
            if word.find('http') == -1 and word.find('.ru') == -1 and word.find('.com') == -1:
                upd_text.append(word)
        new_text.append(upd_text)
        upd_text = []
    return new_text


def start(text): #начальная форма слова
    upd_text = []
    new_text = []
    p = pymorphy2.MorphAnalyzer()
    for j in text:
        for word in j:
            if p.parse(word)[0].tag.POS in ['PREP', 'CONJ', 'PRCL', 'INTJ', 'NPRO']:
                continue
            word = p.parse(word)[0].normal_form
            upd_text.append(word)
        new_text.append(upd_text)
        upd_text = []
    return new_text


wall = []
for i in range(2):
	for group in ['summertimesadnesseva','psyhologiaa']:
		wall.extend(get_wall(domain=group, count=150, offset=100*i))

texts = [[text.lower() for text in lst.split()] for lst in wall]
print(texts)
texts = del_stopwords(texts)
print(texts)
texts = del_links(texts)
print(texts)
texts = del_symbols(texts)
print(texts)
texts = inf(texts)
print(texts)

dictionary = gensim.corpora.Dictionary(texts)
full_text = []
for i in range(len(texts)):
    full_text.extend(texts[i])
corpus = [dictionary.doc2bow(full_text)]

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=10,
                                           alpha='auto',
                                           per_word_topics=False)

vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
pyLDAvis.save_html(vis, 'LDA.html')
pyLDAvis.show(data = vis, open_browser = True)
