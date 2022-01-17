import re
from django.shortcuts import render, HttpResponse, redirect 
import random 
from django.views.decorators.csrf import csrf_exempt

# 내용들을 딕셔너리 형태로 담기
nextID = 4 # 다음에 입력하는 데이터를 위한 전역변수 
topics = [
    {'id':1, 'title':'routing', 'body':'Routing is ..'},
    {'id':2, 'title':'View', 'body':'View is ..'},
    {'id':3, 'title':'Model', 'body':'Model is ..'},
]

# a 태그를 걸면 링크를 의미, 결국 get 방식으로 (데이터를 가져올 때 쓰는 방식) 서버에 접속
# delete 버튼을 누르자마자 서버에 있는 데이터를 수정하는 작업 -> get ㄴㄴ post 사용 (form 방식)
# delete 버튼을 클릭했을 때 슬래쉬 delete로 이동하도록 만들 것
# hidden이라는 form은 눈에 보이지 않지만 서버에 데이터를 전송한다.

def HTMLTemplate(articleTag, id=None): # id 값이 없는 경우 기본값을 줌 
    global topics # 전역변수로 사용
    contextUI = ''
    if id != None: # id가 없는 home에서는 delete 버튼 비활성화 
        contextUI = f'''
             <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>' # f를 사용하면 중괄호가 들어갔을 때 변수를 바로 사용할 수 있음
    return f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ol>
            {ol}
        </ol>
        {articleTag}
        <ul>
            <li><a href="/create/">create</a></li> 
            {contextUI}
        </ul>
    </body>
    </html>
    '''
 #read/1이 링크로 들어가고 뒤에있는 title를 누르면 해당 링크로 이동함

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

#사용자가 입력할 수 있는 input tag, placeholer=사용자가 어떤 값을 입력할지 도움을 줌
#사용자가 입력한 데이터를 서버에 title(name)이라는 이름으로 전송함
#p태그 = 단락을 나타내는 태그
#textarea = 여러 줄의 텍스트를 입력할 때 사용
#데이터를 서버에 원하는 경로로 전송하기 위해서 form 태그로 감싸야 함
#query string = 서버에게 어떠한 정보를 질의할 때 사용 (브라우저가 서버로부터 데이터를 가져옴) get하는 방식

@csrf_exempt
def create(request):
    global nextID 
    print('request.method:', request.method)
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type = "text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type = "submit"</p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))

    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        newTopic = {'id':nextID, 'title':title, 'body':body}
        topics.append(newTopic)
        url = '/read/'+str(nextID) # str 작업 안 해주면 에러 발생  
        nextID += 1
        # print(request.POST) # 입력받은 정보 프린트
        return redirect(url)

# update는 기본적으로 ui 안에 데이터가 들어가 있어야 함
# 토픽 조회를 해야 함 (global 선언)
@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        article = 'Update'
        article = '''
            <form action="/update/{id}" method="post">
                <p><input type = "text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type = "submit"</p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))
    elif request.method == 'POST':
        return redirect(f'/read/{id}')


@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        newsTopics = []
        for topic in topics:
            if topic['id'] != int(id): #id가 다를 때 토픽을 리스트에 추가함
                newsTopics.append(topic) # 즉 내가 read한 id와 일치하지 않는 튜플은 newtopic에 append 해버린다. 즉 삭제 안하고 값을 유지한다는 말임
        topics = newsTopics 
        return redirect('/') # 값을 삭제하고 홈으로 이동

        print('id', id)

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic["id"] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'

    return HttpResponse(HTMLTemplate(article, id))

#웹 서버는 정적
# 웹 프레임워크는 동적임 - 접속이 들어올 때마다 랜덤한 정보를 동적으로 만들어주는 웹어플리케이션!
# 
# http://127.0.0.1:8000/create/?title=CRUD&body=CRUD+is+.. 
# (브라우저가 서버에 있는 데이터를 변경하려는 작업) 이 링크를 공유하면 큰일.. 왜냐하면 방문자가 클릭할 때마다 글이 추가돼서
# 따라서 브라우저가 서버에 데이터를 변경할 때는 url에 query string 넣으면 절ㄷㅐ ㄴㄴ 따라서 post를 사용해야 함.
# url이 아닌 Headers라는 것 안에 데이터를 포함해서 눈에 보이지 않게 보낼 수 있다.
# 아무것도 하지 않을 땐 기본적으로 get 방식. 
# request.method를 통해서 사용자가 어떤 방식으로 (get, post) 접속했는지 알 수 있음
