from pymongo import MongoClient
from bson.objectid import ObjectId
import random

MONGO_URI = "mongodb://admin_user:admin123@localhost:27017/library_db?authSource=library_db"
client = MongoClient(MONGO_URI)
db = client['library_db']

db.books.delete_many({})
db.authors.delete_many({})

authors_data = [
    {
        "name": "Александр Пушкин",
        "country": "Россия",
        "birth_year": 1799
    },
    {
        "name": "Лев Толстой",
        "country": "Россия",
        "birth_year": 1828
    },
    {
        "name": "Фёдор Достоевский",
        "country": "Россия",
        "birth_year": 1821
    },
    {
        "name": "Михаил Булгаков",
        "country": "Россия",
        "birth_year": 1891
    },
    {
        "name": "Антон Чехов",
        "country": "Россия",
        "birth_year": 1860
    },
    {
        "name": "Николай Гоголь",
        "country": "Россия",
        "birth_year": 1809
    },
    {
        "name": "Иван Тургенев",
        "country": "Россия",
        "birth_year": 1818
    },
    {
        "name": "Владимир Набоков",
        "country": "Россия",
        "birth_year": 1899
    },
    {
        "name": "Борис Пастернак",
        "country": "Россия",
        "birth_year": 1890
    },
    {
        "name": "Михаил Шолохов",
        "country": "Россия",
        "birth_year": 1905
    },
    {
        "name": "Чарльз Диккенс",
        "country": "Великобритания",
        "birth_year": 1812
    },
    {
        "name": "Джейн Остин",
        "country": "Великобритания",
        "birth_year": 1775
    },
    {
        "name": "Джордж Оруэлл",
        "country": "Великобритания",
        "birth_year": 1903
    },
    {
        "name": "Джон Толкин",
        "country": "Великобритания",
        "birth_year": 1892
    },
    {
        "name": "Артур Конан Дойл",
        "country": "Великобритания",
        "birth_year": 1859
    },
    {
        "name": "Виктор Гюго",
        "country": "Франция",
        "birth_year": 1802
    },
    {
        "name": "Александр Дюма",
        "country": "Франция",
        "birth_year": 1802
    },
    {
        "name": "Жюль Верн",
        "country": "Франция",
        "birth_year": 1828
    },
    {
        "name": "Альбер Камю",
        "country": "Франция",
        "birth_year": 1913
    },
    {
        "name": "Гюстав Флобер",
        "country": "Франция",
        "birth_year": 1821
    },
    {
        "name": "Марк Твен",
        "country": "США",
        "birth_year": 1835
    },
    {
        "name": "Эрнест Хемингуэй",
        "country": "США",
        "birth_year": 1899
    },
    {
        "name": "Фрэнсис Скотт Фицджеральд",
        "country": "США",
        "birth_year": 1896
    },
    {
        "name": "Джек Лондон",
        "country": "США",
        "birth_year": 1876
    },
    {
        "name": "Уильям Фолкнер",
        "country": "США",
        "birth_year": 1897
    },
    {
        "name": "Франц Кафка",
        "country": "Германия",
        "birth_year": 1883
    },
    {
        "name": "Томас Манн",
        "country": "Германия",
        "birth_year": 1875
    },
    {
        "name": "Герман Гессе",
        "country": "Германия",
        "birth_year": 1877
    },
    {
        "name": "Иоганн Вольфганг фон Гёте",
        "country": "Германия",
        "birth_year": 1749
    },
    {
        "name": "Эрих Мария Ремарк",
        "country": "Германия",
        "birth_year": 1898
    }
]

author_ids = []
for author in authors_data:
    result = db.authors.insert_one(author)
    author_ids.append(result.inserted_id)
    print(f"Добавлен автор: {author['name']} ({author['country']})")

books_data = [
    {"title": "Евгений Онегин", "author_index": 0, "year": 1833, "genre": "Роман в стихах"},
    {"title": "Капитанская дочка", "author_index": 0, "year": 1836, "genre": "Исторический роман"},
    {"title": "Повести Белкина", "author_index": 0, "year": 1831, "genre": "Повести"},
    {"title": "Дубровский", "author_index": 0, "year": 1841, "genre": "Роман"},
    {"title": "Пиковая дама", "author_index": 0, "year": 1834, "genre": "Повесть"},
    {"title": "Война и мир", "author_index": 1, "year": 1869, "genre": "Роман-эпопея"},
    {"title": "Анна Каренина", "author_index": 1, "year": 1877, "genre": "Роман"},
    {"title": "Воскресение", "author_index": 1, "year": 1899, "genre": "Роман"},
    {"title": "Смерть Ивана Ильича", "author_index": 1, "year": 1886, "genre": "Повесть"},
    {"title": "Крейцерова соната", "author_index": 1, "year": 1889, "genre": "Повесть"},
    {"title": "Преступление и наказание", "author_index": 2, "year": 1866, "genre": "Роман"},
    {"title": "Идиот", "author_index": 2, "year": 1869, "genre": "Роман"},
    {"title": "Братья Карамазовы", "author_index": 2, "year": 1880, "genre": "Роман"},
    {"title": "Бесы", "author_index": 2, "year": 1872, "genre": "Роман"},
    {"title": "Записки из подполья", "author_index": 2, "year": 1864, "genre": "Повесть"},
    {"title": "Мастер и Маргарита", "author_index": 3, "year": 1967, "genre": "Роман"},
    {"title": "Собачье сердце", "author_index": 3, "year": 1925, "genre": "Повесть"},
    {"title": "Белая гвардия", "author_index": 3, "year": 1925, "genre": "Роман"},
    {"title": "Записки юного врача", "author_index": 3, "year": 1926, "genre": "Рассказы"},
    {"title": "Роковые яйца", "author_index": 3, "year": 1925, "genre": "Повесть"},
    {"title": "Вишнёвый сад", "author_index": 4, "year": 1904, "genre": "Пьеса"},
    {"title": "Чайка", "author_index": 4, "year": 1896, "genre": "Пьеса"},
    {"title": "Три сестры", "author_index": 4, "year": 1901, "genre": "Пьеса"},
    {"title": "Дядя Ваня", "author_index": 4, "year": 1897, "genre": "Пьеса"},
    {"title": "Палата №6", "author_index": 4, "year": 1892, "genre": "Повесть"},
    {"title": "Мёртвые души", "author_index": 5, "year": 1842, "genre": "Поэма"},
    {"title": "Ревизор", "author_index": 5, "year": 1836, "genre": "Комедия"},
    {"title": "Тарас Бульба", "author_index": 5, "year": 1835, "genre": "Повесть"},
    {"title": "Шинель", "author_index": 5, "year": 1842, "genre": "Повесть"},
    {"title": "Вечера на хуторе близ Диканьки", "author_index": 5, "year": 1832, "genre": "Повести"},
    {"title": "Отцы и дети", "author_index": 6, "year": 1862, "genre": "Роман"},
    {"title": "Дворянское гнездо", "author_index": 6, "year": 1859, "genre": "Роман"},
    {"title": "Накануне", "author_index": 6, "year": 1860, "genre": "Роман"},
    {"title": "Записки охотника", "author_index": 6, "year": 1852, "genre": "Рассказы"},
    {"title": "Муму", "author_index": 6, "year": 1854, "genre": "Рассказ"},
    {"title": "Лолита", "author_index": 7, "year": 1955, "genre": "Роман"},
    {"title": "Дар", "author_index": 7, "year": 1938, "genre": "Роман"},
    {"title": "Защита Лужина", "author_index": 7, "year": 1930, "genre": "Роман"},
    {"title": "Приглашение на казнь", "author_index": 7, "year": 1936, "genre": "Роман"},
    {"title": "Машенька", "author_index": 7, "year": 1926, "genre": "Роман"},
    {"title": "Доктор Живаго", "author_index": 8, "year": 1957, "genre": "Роман"},
    {"title": "Детство Люверс", "author_index": 8, "year": 1922, "genre": "Повесть"},
    {"title": "Охранная грамота", "author_index": 8, "year": 1931, "genre": "Автобиография"},
    {"title": "Сестра моя жизнь", "author_index": 8, "year": 1922, "genre": "Поэзия"},
    {"title": "Воздушные пути", "author_index": 8, "year": 1924, "genre": "Рассказы"},
    {"title": "Тихий Дон", "author_index": 9, "year": 1940, "genre": "Роман-эпопея"},
    {"title": "Поднятая целина", "author_index": 9, "year": 1960, "genre": "Роман"},
    {"title": "Судьба человека", "author_index": 9, "year": 1957, "genre": "Рассказ"},
    {"title": "Донские рассказы", "author_index": 9, "year": 1926, "genre": "Рассказы"},
    {"title": "Они сражались за Родину", "author_index": 9, "year": 1959, "genre": "Роман"},
    {"title": "Приключения Оливера Твиста", "author_index": 10, "year": 1838, "genre": "Роман"},
    {"title": "Большие надежды", "author_index": 10, "year": 1861, "genre": "Роман"},
    {"title": "Рождественская песнь", "author_index": 10, "year": 1843, "genre": "Повесть"},
    {"title": "Гордость и предубеждение", "author_index": 11, "year": 1813, "genre": "Роман"},
    {"title": "Разум и чувства", "author_index": 11, "year": 1811, "genre": "Роман"},
    {"title": "Эмма", "author_index": 11, "year": 1815, "genre": "Роман"},
    {"title": "1984", "author_index": 12, "year": 1949, "genre": "Антиутопия"},
    {"title": "Скотный двор", "author_index": 12, "year": 1945, "genre": "Сатира"},
    {"title": "Властелин колец", "author_index": 13, "year": 1954, "genre": "Фэнтези"},
    {"title": "Хоббит", "author_index": 13, "year": 1937, "genre": "Фэнтези"},
    {"title": "Приключения Шерлока Холмса", "author_index": 14, "year": 1892, "genre": "Детектив"},
    {"title": "Собака Баскервилей", "author_index": 14, "year": 1902, "genre": "Детектив"},
    {"title": "Отверженные", "author_index": 15, "year": 1862, "genre": "Роман"},
    {"title": "Собор Парижской Богоматери", "author_index": 15, "year": 1831, "genre": "Роман"},
    {"title": "Три мушкетёра", "author_index": 16, "year": 1844, "genre": "Приключения"},
    {"title": "Граф Монте-Кристо", "author_index": 16, "year": 1846, "genre": "Приключения"},
    {"title": "Двадцать тысяч лье под водой", "author_index": 17, "year": 1870, "genre": "Научная фантастика"},
    {"title": "Вокруг света за 80 дней", "author_index": 17, "year": 1873, "genre": "Приключения"},
    {"title": "Посторонний", "author_index": 18, "year": 1942, "genre": "Роман"},
    {"title": "Чума", "author_index": 18, "year": 1947, "genre": "Роман"},
    {"title": "Госпожа Бовари", "author_index": 19, "year": 1856, "genre": "Роман"},
    {"title": "Приключения Тома Сойера", "author_index": 20, "year": 1876, "genre": "Приключения"},
    {"title": "Приключения Гекльберри Финна", "author_index": 20, "year": 1884, "genre": "Приключения"},
    {"title": "Старик и море", "author_index": 21, "year": 1952, "genre": "Повесть"},
    {"title": "Прощай, оружие!", "author_index": 21, "year": 1929, "genre": "Роман"},
    {"title": "Великий Гэтсби", "author_index": 22, "year": 1925, "genre": "Роман"},
    {"title": "Зов предков", "author_index": 23, "year": 1903, "genre": "Приключения"},
    {"title": "Мартин Иден", "author_index": 23, "year": 1909, "genre": "Роман"},
    {"title": "Шум и ярость", "author_index": 24, "year": 1929, "genre": "Роман"},
    {"title": "Процесс", "author_index": 25, "year": 1925, "genre": "Роман"},
    {"title": "Замок", "author_index": 25, "year": 1926, "genre": "Роман"},
    {"title": "Будденброки", "author_index": 26, "year": 1901, "genre": "Роман"},
    {"title": "Степной волк", "author_index": 27, "year": 1927, "genre": "Роман"},
    {"title": "Фауст", "author_index": 28, "year": 1808, "genre": "Трагедия"},
    {"title": "На Западном фронте без перемен", "author_index": 29, "year": 1929, "genre": "Роман"}
]

for book in books_data:
    book_doc = {
        "title": book["title"],
        "author_id": author_ids[book["author_index"]],
        "year": book["year"],
        "genre": book["genre"],
        "available": random.choice([True, False])
    }
    db.books.insert_one(book_doc)

print(f"\nДобавлено авторов: {len(author_ids)}")
print(f"Добавлено книг: {len(books_data)}")
print("База данных заполнена мировой классической литературой!")

countries = db.authors.distinct('country')
for country in countries:
    count = db.authors.count_documents({'country': country})
    print(f"  {country}: {count} авторов")

client.close()
