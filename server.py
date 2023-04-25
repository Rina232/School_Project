from flask import Flask, render_template, request
import xlrd3

app = Flask(__name__)

with open('static/documents/inf.txt', encoding='utf8') as f:
    data = f.readlines()

inf = {'school_name': data[0].strip(),
       'full_school_name': data[1].strip(),
       'address': data[2].strip(),
       'phone_number': data[3].strip(),
       'email': data[4].strip()}

at = ''
try:
    with open("static/documents/attention.txt", encoding='utf8') as f:
        data = f.readlines()
    for i in data:
        at += i.strip() + ' '
except Exception as e:
    print(e)

schedule = []
try:
    workbook = xlrd3.open_workbook("static/documents/schedule.xlsx")
    worksheet = workbook.sheet_by_index(0)
    for i in range(0, 230):
        lst = []
        for j in range(0, 11):
            if type(worksheet.cell_value(i, j)) is float:
                lst.append(int(worksheet.cell_value(i, j)))
            else:
                lst.append(worksheet.cell_value(i, j))
        schedule.append(lst)
except Exception as e:
    print(e)

polls = []
try:
    with open("static/documents/polls/polls.txt", encoding='utf8') as f:
        data = f.readlines()
    k = 0
    date = ''
    name = ''
    description = ''
    for i in data:
        if k == 0:
            date = i.strip()
        elif k == 1:
            name = i.strip()
        elif k == 2:
            description = i.strip()
        elif k == 3:
            polls.append({'date': date,
                          'name': name,
                          'description': description,
                          'doc': i.strip()})
            k = -2
        k += 1
except Exception as e:
    print(e)

actual = []
try:
    with open("static/documents/actual/actual.txt", encoding='utf8') as f:
        data = f.readlines()
    k = 0
    name = ''
    doc = ''
    for i in data:
        if k == 0:
            name = i.strip()
        elif k == 1:
            doc = i.strip()
        elif k == 2:
            actual.append({'name': name,
                           'doc': doc,
                           'pic': i.strip()})
        elif k == 3:
            k = -1
        k += 1
except Exception as e:
    print(e)

news = []
try:
    with open("static/documents/news/news.txt", encoding='utf8') as f:
        data = f.readlines()
    k = 0
    name = ''
    date = ''
    pic = ''
    text = ''
    for i in data:
        if k == 0:
            name = i.strip()
        elif k == 1:
            date = i.strip()
        elif k == 2:
            text = i.strip()
        elif k == 3:
            pic = i.strip()
        elif k == 4:
            news.append({'name': name,
                         'date': date,
                         'text': text,
                         'pic': pic,
                         'doc': i.strip()})
        elif k == 5:
            k = -1
        k += 1
except Exception as e:
    print(e)

information = []
try:
    with open("static/documents/information.txt", encoding='utf8') as f:
        data = f.readlines()
    for i in data:
        information.append(i.strip())
except Exception as e:
    print(e)


@app.route('/')
def main_page():
    return render_template('main.html', inf=inf, attention=at, actual=actual, news=news[:5])


@app.route('/schedule')
def schedule_page():
    return render_template('schedule.html', inf=inf, attention=at, schdl=schedule)


@app.route('/polls')
def polls_page():
    return render_template('polls.html', inf=inf, attention=at, polls=polls)


@app.route('/poll/<name>', methods=['POST', 'GET'])
def poll_page(name):
    doc = [i['doc'] for i in polls if i['name'] == name][0]
    questions = []
    keys = []
    try:
        with open(f'static/documents/polls/{doc}', encoding='utf8') as f:
            data = f.readlines()
            for i in data:
                questions.append(i.strip())
        if len(questions) == 0:
            raise Exception('Файл пустой')
        k = 0
        temp = []
        for i in questions:
            if k == 1 and i[:3] == 'кон':
                k = 0
                keys.append(temp)
                temp = []
            elif k == 1:
                temp.append(i)
            elif i[:6] == 'список':
                keys.append(i[7:])
            elif i[:6] == 'строка':
                keys.append(i[7:])
            elif i[:5] == 'текст':
                keys.append(i[6:])
            elif i[:5] == 'выбор':
                keys.append(i[6:])
            elif i[:10] == 'множ выбор':
                k = 1
                temp.append(i[11:])
        if request.method == 'GET':
            return render_template('poll.html', inf=inf, attention=at, quest=questions, name=name)
        elif request.method == 'POST':
            with open(f"static/documents/polls_answers/{doc[:-4]}_answers.txt", mode="a", encoding='utf8') as f:
                for i in keys:
                    if type(i) == list:
                        f.write(i[0] + '\n')
                        for j in i[1:]:
                            try:
                                f.write(request.form[j] + '\n')
                            except Exception as e:
                                pass
                    else:
                        f.write(i + '\n' + request.form[i] + '\n')
                f.write('\n')
            return render_template('conclusion_poll.html', inf=inf,
                                   attention=at, con='Спасибо за прохождение опроса!')
    except Exception as e:
        return render_template('conclusion_poll.html', inf=inf,
                               attention=at, con='Произошли технические неполадки')


@app.route('/actual/<name>')
def actual_page(name):
    doc = [i['doc'] for i in actual if i['name'] == name][0]
    try:
        with open(f'static/documents/actual/{doc}', encoding='utf8') as f:
            data = f.readlines()
        if data:
            return render_template('actual.html', inf=inf, attention=at, name=name, text=data)
        else:
            raise Exception
    except Exception as e:
        return render_template('conclusion_main.html', inf=inf, attention=at)


@app.route('/news/<value>')
def news1_page(value):
    if value.isnumeric() and len(news) >= int(value) * 5:
        data = news[(int(value) - 1) * 5: int(value) * 5]
        return render_template('news.html', inf=inf, attention=at, news=data, num=len(news) // 5,
                               now_num=int(value), real_len=len(news))
    elif value.isnumeric() and int(value) * 5 - len(news) <= 5:
        data = news[(int(value) - 1) * 5:]
        return render_template('news.html', inf=inf, attention=at, news=data, num=len(news) // 5,
                               now_num=int(value), real_len=len(news))
    doc, date = [(i['doc'], i['date']) for i in news if i['name'] == value][0]
    try:
        with open(f'static/documents/news/{doc}', encoding='utf8') as f:
            data = f.readlines()
        if data:
            return render_template('news1.html', inf=inf, attention=at, name=value, date=date, text=data)
        else:
            raise Exception('Файл пустой')
    except Exception as e:
        return render_template('conclusion_news.html', inf=inf, attention=at)


@app.route('/information')
def information_page():
    return render_template('information.html', inf=inf, attention=at, information=information)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
