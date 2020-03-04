"""
HackerNews Table
"""
from bottle import (
    route, run, template, request, redirect
)
from sqlalchemy import exists
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/")
@route("/news")
def news_list():
    """ Вывести таблицу с неразмеченными новостями """
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    """
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    """
    try:
        s = session()
        news_record = s.query(News).get(request.query.id)
        news_record.label = request.query.label
        s.commit()
    except BaseException:
        pass
    redirect("/news")


@route("/update")
def update_news():
    """
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    """
    news = get_news("https://news.ycombinator.com/newest", 1)
    s = session()
    for new in news:
        (record_exists, ), = s.query(exists().where(
            News.title == new['title'] and News.author == new['author']))
        if record_exists:
            break
        print('Adding record...')
        record = News(title=new['title'],
                      author=new['author'],
                      url=new['url'],
                      comments=new['comments'],
                      points=new['points'],
                      cleaned=new['cleaned'])
        s.add(record)
    s.commit()
    redirect("/news")


@route('/recommendations')
def recommendations():
    """
    # 1. Получить список неразмеченных новостей из БД
    # 2. Получить прогнозы для каждой новости
    # 3. Вывести ранжированную таблицу с новостями
    """

    s = session()
    rows = s.query(News).filter(News.label != None).all()
    labels = [row.label for row in rows]
    titles = [row.cleaned for row in rows]
    model = NaiveBayesClassifier()
    model.fit(titles, labels)
    rows = s.query(News).filter(News.label == None).all()
    titles = [row.cleaned for row in rows]
    classification = sorted(zip(rows, model.predict(titles)),
                            key=lambda x: (x[1][0], abs(x[1][1])))
    classified_news = []
    for record in classification:
        classified_news.append(record[0])
    return template('news_recommendations', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
