from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment
import random

# Создание двух пользователей
user_jhon = User.objects.create_user(username = 'Jhon', email = '', password = '1111')
user_mike = User.objects.create_user(username = 'Mike', email = '', password = '2222')

# Создание двух объектов Author
author_jhon = Author.objects.create(author = user_jhon)
author_mike = Author.objects.create(author = user_mike)

#Создание категорий новостей(статей)
sport_cat = Category.objects.create(new_category = 'Спорт')
culture_cat = Category.objects.create(new_category = 'Культура')
economic_cat = Category.objects.create(new_category = 'Экономика')
science_cat = Category.objects.create(new_category = 'Наука')
auto_cat = Category.objects.create(new_category = 'Авто')

#Создание первого поста
post1_title = 'Представителей Реала не будет на церемонии вручения наград ФИФА'
post1_text = 'Нападающий Реала не попал в список 26 кандидатов на включение в команду года по версии Международной федерации футбола. В семерку лучших форвардов мира по мнению футболистов вошли Карим Бензема Реал, Криштиану Роналду Аль-Наср, Килиан Мбаппе, Неймар, Лионель Месси все — Пари Сен-Жермен, Эрлинг Холанд Манчестер Сити и Роберт Левандовский Барселона. В испанской команде решение не включать Винисиуса в список кандидатов сочли несправедливым. Сообщается, что претендующие на личные награды Бензема, вратарь Тибо Куртуа и тренер Карло Анчелотти также не будут присутствовать на церемонии. Церемония The Best FIFA Football Awards — 2022 пройдет в понедельник в Париже.'
post1 = Post.objects.create(author = author_jhon, post_type = 'AR', title = post1_title, text = post1_text)

#Создание второго поста
post2_title = 'Maserati показала почти 100 снимков своего нового спорткупе'
post2_text = 'Новое поколение Maserati GranTurismo вышло не менее красивым, чем предыдущее. Теперь новинку можно рассмотреть во всех деталях и в разных вариантах окраски в огромной фирменной фотогалерее'
post2 = Post.objects.create(author = author_mike, post_type = 'AR', title = post2_title, text = post2_text)

# Создание новости
news1_title = 'Минтранс заявил о планах кратно увеличить число авиарейсов в Китай'
news1_text = 'В 2023 году Минтранс ожидает, что число авиарейсов в Китай и количество перевезенных пассажиров между Россией и КНР кратно увеличатся, говорится в сообщении ведомства, поступившем в РБК. В ведомстве пояснили, что этому должно способствовать снятие карантинных ограничений китайской стороной и разрешение на безвизовых поездок тургрупп из двух стран.'
news1 = Post.objects.create(author = author_jhon, post_type = 'NW', title = news1_title, text = news1_text)

# Назначение категории новостей для созданных постов
PostCategory.objects.create(post = post1, category = sport_cat)
PostCategory.objects.create(post = post2, category = auto_cat)
PostCategory.objects.create(post = news1, category = economic_cat)
PostCategory.objects.create(post = news1, category = culture_cat)

#Пишем комментарии к постам
comment_1 = Comment.objects.create(text = 'Новость - бомба!', post = post1, user = user_mike)
comment_2 = Comment.objects.create(text = 'Обожаю Tesla! Мазерати отстой!', post = post2, user = user_jhon)
comment_3 = Comment.objects.create(text = 'Кому это надо?', post = news1, user = user_jhon)
comment_4 = Comment.objects.create(text = 'Минтранс ошибся с анализом', post = news1, user = user_mike)
comment_5 = Comment.objects.create(text = 'Ерунда какая-то. Хм.', post = post1, user = user_jhon)

#Лайкаем, дизим посты и комментарии
obj_for_like = [post1, post2, news1, comment_1, comment_2, comment_3, comment_4]
for i in range(100):
	rnd_obj = random.choice(obj_for_like)
	if i % 2:
		rnd_obj.like()
	else:
		rnd_obj.dislike()
		
#Считаем суммарный рейтинг Jhony 
jhony_rating = sum([post.rating*3 for post in Post.objects.filter(author = author_jhon)]) + sum([comment.rating for comment in Comment.objects.filter(user = author_jhon.author)]) + sum([comment.rating for comment in Comment.objects.filter(post__author = author_jhon)])
author_jhon.update_rating(jhony_rating)

#Считаем суммарный рейтинг Mikla
miky_rating = sum([post.rating*3 for post in Post.objects.filter(author = author_mike)]) + sum([comment.rating for comment in Comment.objects.filter(user = author_mike.author)]) + sum([comment.rating for comment in Comment.objects.filter(post__author = author_mike)])
author_mike.update_rating(miky_rating)

# Находим и выводим лучшего автора
best_user = Author.objects.all().order_by('-user_rating')
print('The best user is ' + best_user[0].author.username)
print('Rating: ' + str(best_user[0].user_rating))

#Ищем и выводим информацию лучшего поста
best_article = Post.objects.all().order_by('-rating')[0]
print("Best article information: ")
print("create time: " + best_article.time_create.strftime("%Y-%m-%d %H:%M:%S"))
print("author: " + best_article.author.author.username)
print("rating: " + str(best_article.rating))
print("title: " + best_article.title)
print("preview: " + best_article.preview())

#Выводим комментарии к лучшему посту
best_article_comments = Comment.objects.filter(post = best_article)
print("Комментарии к лучшей статье...")
for best_article_comment in best_article_comments:
	print("Дата комментария: " + best_article_comment.created.strftime("%Y-%m-%d %H:%M:%S"))
	print("Пользователь: " + best_article_comment.user.username)
	print("Рейтинг комментария: " + str(best_article_comment.rating))
	print("Текст комментария: " + best_article_comment.text + "\n")
