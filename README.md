# votesApi

votesApi - rest api для проведения голосований 

Перед началом использования необходимо создать модели Person и Voting в админ панели django

Перед созданием отчетов необходимо прописать email и пароль 

в admin.py 

    @admin.action(description='create report')
    def create_report(self, request, queryset):
        email_from = ""     # enter your email
        email_from_password = ""    # enter your email password

Отчеты будут автоматически отправлены на почту указаную пользователем админской панели

![image](https://github.com/Dr0n43k/votesApi/assets/72655205/756b7272-60c4-4b46-8a3f-988e409157af)



пользовательские запросы

/votingList пустой get запрос для получения списка всех голосований.

Возвращаемые значения:
список json`ов
[
    {
        "id": 8,
        "title": "Название1",
        "active": false
    },
    {
        "id": 9,
        "title": "Название2",
        "active": false
    }]

/voting?voting_id={id голосования}

Возвращаемые значения: 

voting(str)(наименование голосования)
                       
active(bool)(состояние голосования)

persons(список json`ов)(список участников голосования) 
	[{
            "person": "Вячеслав И.Ф.",
            "votes": 20
        },
        {
            "person": "Марк П.Г.",
            "votes": 0
        }]


/persons?voting_id={id голосования}

Возвращаемые значения: 

id(int)(id участника голосования)

fullname(str)(полное имя участника голосования)

photo(url)(url фотогафии участника)

age(int)(возраст участника)

biography(str)(биография участника)


/winners пустой get запрос

Возвращаемые значения:

[
    {
        "voting": "Название1",
        "winner": [
            "Георгий И.П.",
			"Владимир К.И"
        ],
        "votes": 20
    },
    {
        "voting": "Название2",
        "winner": [
            "1"
        ],
        "votes": 0
    }
]


/send_vote POST {'voting_id': (int)id голосования, 'person_id': (int)id участника}
Возвращаемые значения:

{
    "person": "Георгий И.П.",
    "votes": 1
}


                       
