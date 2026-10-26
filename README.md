# Online Store

Учебный Python-проект с моделями товаров и категорий интернет-магазина. Проект поддерживает ручное создание
объектов, загрузку каталога из JSON, поиск полей по настраиваемым алиасам и журналирование операций чтения данных.

## Возможности

- создание товаров с названием, описанием, ценой и количеством на складе;
- создание категорий со списком товаров;
- хранение списка товаров и цены в приватных атрибутах;
- контролируемое добавление товаров через `Category.add_product()`;
- создание и объединение одноимённых товаров через `Product.new_product()`;
- проверка и подтверждение изменения цены;
- автоматический подсчёт созданных категорий и товаров;
- загрузка категорий и товаров из `data/products.json`;
- настройка названий полей через `configs/field_aliases.json`;
- чтение JSON- и Excel-файлов;
- обработка некорректных входных данных с записью ошибок в журналы;
- тестирование с отчётом о покрытии исходного кода.

## Структура проекта

```text
online_store/
├── configs/
│   └── field_aliases.json
├── data/
│   └── products.json
├── htmlcov/
├── logs/
├── src/
│   ├── category.py
│   ├── fields.py
│   ├── product.py
│   ├── readers.py
│   └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_category.py
│   ├── test_fields.py
│   ├── test_main.py
│   ├── test_package.py
│   ├── test_product.py
│   ├── test_readers.py
│   └── test_utils.py
├── main.py
├── pyproject.toml
└── README.md
```

## Модули и функции

### `src.product`

Модуль содержит класс `Product`, представляющий одну товарную позицию.

Атрибуты объекта:

- `name: str` — название товара;
- `description: str` — описание товара;
- `quantity: int` — количество товара в наличии;
- `__price: float` — приватная цена товара.

Публичный property `price` предоставляет доступ к приватной цене. Геттер возвращает текущее значение, а сеттер
проверяет новую цену и запрашивает подтверждение при её снижении.

Конструктор:

```python
Product(name: str, description: str, price: float, quantity: int)
```

Название, описание и остаток сохраняются в одноимённых атрибутах, а цена — в приватном атрибуте `__price`.

Методы:

- `new_product(product_data, products=None)` — создаёт новый товар из словаря или объединяет его с одноимённым;
- `price` — property для чтения и контролируемого изменения цены.

### `src.category`

Модуль содержит класс `Category`, объединяющий товары в категорию.

Атрибуты объекта:

- `name: str` — название категории;
- `description: str` — описание категории;
- `__products: list[Product]` — приватный список товаров категории.

Публичный property `products` возвращает не сам список, а готовую для вывода строку с товарами.

Атрибуты класса:

- `category_count` — количество созданных объектов `Category`;
- `product_count` — суммарное количество товарных позиций, переданных во все созданные категории.

Конструктор:

```python
Category(
    name: str,
    description: str,
    products: list[Product] | None = None,
)
```

Если список товаров не передан, создаётся пустая категория. При каждом вызове конструктора автоматически
обновляется `category_count`. Переданные товары добавляются через `add_product()`, который также обновляет
`product_count`.

Методы:

- `add_product(product)` — добавляет объект `Product` в приватный список;
- `products` — property, возвращающий строковое представление товаров.

### `src.readers`

Модуль отвечает за безопасное чтение данных из файлов.

#### `get_fields_from_json(file_path)`

Читает JSON-файл по пути `file_path`. Корневым элементом должен быть объект или массив. При успешном чтении функция
возвращает данные без дополнительного преобразования. Если файл отсутствует, недоступен, имеет неверную кодировку,
содержит некорректный JSON или неподдерживаемый корневой тип, возвращается пустой список.

```python
data = get_fields_from_json("data/products.json")
```

#### `get_transactions_from_xls(file_path)`

Читает лист `Отчет по операциям` из Excel-файла и возвращает список словарей. Полностью пустые строки пропускаются.
При ошибке чтения или пустом файле возвращается пустой список.

```python
transactions = get_transactions_from_xls("data/operations.xlsx")
```

### `src.fields`

Модуль загружает справочник алиасов и извлекает значения из словарей по простым или вложенным путям.

#### `get_by_path(item, path)`

Возвращает значение из `item` по указанному пути. Сначала проверяется буквальный ключ, затем вложенная структура.

```python
item = {"currency": {"code": "RUB"}}
code = get_by_path(item, "currency.code")
```

Если путь отсутствует, функция вызывает `KeyError`.

#### `get_field_value(transaction, field_name, field_aliases)`

Получает логическое имя поля и перебирает соответствующие пути из справочника `field_aliases`. Возвращается значение
по первому найденному пути. Если имя поля отсутствует в справочнике или ни один путь не найден, возвращается пустой
список.

#### `load_fields(file_path)`

Загружает справочник полей из JSON с помощью `get_fields_from_json` и возвращает полученную структуру.

#### `_load_field_aliases()`

Внутренняя функция загружает `configs/field_aliases.json` и проверяет его структуру. Ожидается словарь, в котором
каждому строковому имени поля соответствует список строковых путей. При ошибке возвращается пустой словарь.

### `src.utils`

Модуль преобразует исходные JSON-данные в объекты предметной области.

#### `load_categories_from_json(file_path=PRODUCTS_FILE_PATH)`

Загружает список категорий через `get_fields_from_json`, создаёт объекты `Product` для вложенных товаров и объекты
`Category` для категорий. По умолчанию используется `data/products.json`.

```python
categories = load_categories_from_json()
```

Функция возвращает `list[Category]`. Категории с неверной структурой пропускаются и записываются в журнал. Если
корневым элементом JSON не является список, возвращается пустой список.

### `src`

Корневой пакет экспортирует `Product` и `Category`, поэтому модели можно импортировать напрямую:

```python
from src import Category, Product
```

### `main.py`

Демонстрационный модуль создаёт несколько объектов `Product` и `Category`, выводит их свойства и показывает работу
общих счётчиков `Category.category_count` и `Category.product_count`. Исполняемый код защищён условием
`if __name__ == "__main__"`.

### Файлы данных и конфигурации

- `data/products.json` — исходный каталог категорий и товаров;
- `configs/field_aliases.json` — соответствие логических имён полей возможным путям в исходных данных.

## Требования

- Python 3.12 или новее;
- Poetry.

## Установка

Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone <адрес-репозитория>
cd online_store
```

Установите основные зависимости и инструменты разработки:

```bash
poetry install
```

## Запуск

Демонстрационный сценарий создаёт товары и категории и выводит их данные и значения общих счётчиков:

```bash
poetry run python main.py
```

## Использование моделей

```python
from src.category import Category
from src.product import Product

phone = Product(
    name="Iphone 15",
    description="512GB, Gray space",
    price=210000.0,
    quantity=8,
)

smartphones = Category(
    name="Смартфоны",
    description="Смартфоны и аксессуары",
    products=[phone],
)

print(smartphones.name)
print(smartphones.products)
print(Category.category_count)
print(Category.product_count)
```

`Category.category_count` содержит количество созданных категорий, а `Category.product_count` — общее количество
товарных позиций во всех созданных категориях. Значение `quantity` отдельного товара не суммируется в
`product_count`.

## Приватный список товаров категории

Категория хранит товары в приватном атрибуте `__products`. Получить или заменить исходный список напрямую нельзя.
Новый товар добавляется только через метод `add_product()`:

```python
category = Category("Смартфоны", "Смартфоны и аксессуары")
category.add_product(phone)
```

Метод принимает объект `Product`, добавляет его в приватный список и увеличивает `Category.product_count`. Передача
объекта другого типа приводит к `TypeError`.

Property `products` возвращает строку, которую можно вывести в консоль или передать в другой интерфейс:

```python
print(category.products)
```

Формат каждой строки:

```text
Iphone 15, 210000.0 руб. Остаток: 8 шт.
```

Если в категории несколько товаров, строки объединяются через перевод строки. Для пустой категории геттер
возвращает пустую строку.

## Создание и объединение товаров

Класс-метод `Product.new_product()` принимает данные товара в словаре:

```python
product_data = {
    "name": "Iphone 15",
    "description": "512GB, Gray space",
    "price": 210000.0,
    "quantity": 8,
}

product = Product.new_product(product_data)
```

Для поиска одноимённых товаров вторым аргументом можно передать существующий список:

```python
products = [product]

same_product = Product.new_product(
    {
        "name": "Iphone 15",
        "description": "Новая поставка",
        "price": 220000.0,
        "quantity": 2,
    },
    products,
)
```

Если название совпадает, новый объект не создаётся: количество прибавляется к существующему остатку, а из двух цен
выбирается более высокая. Метод возвращает найденный и обновлённый объект. Если совпадений нет, возвращается новый
экземпляр `Product`.

## Управление ценой

Цена хранится в приватном атрибуте `Product.__price` и доступна через property `price`:

```python
print(product.price)
product.price = 230000.0
```

Правила изменения цены:

- положительная цена, равная текущей или превышающая её, устанавливается сразу;
- при попытке установить нулевую или отрицательную цену выводится сообщение
  `Цена не должна быть нулевая или отрицательная`, а значение не меняется;
- при снижении цены программа запрашивает подтверждение;
- ответ `y` подтверждает снижение, любой другой ответ отменяет его.

## Загрузка каталога из JSON

По умолчанию функция использует файл `data/products.json`:

```python
from src.utils import load_categories_from_json

categories = load_categories_from_json()

for category in categories:
    print(category.name)
    print(category.products)
```

Можно передать другой путь:

```python
categories = load_categories_from_json("data/another_products.json")
```

Ожидаемая структура JSON:

```json
[
  {
    "name": "Смартфоны",
    "description": "Смартфоны и аксессуары",
    "products": [
      {
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 210000.0,
        "quantity": 8
      }
    ]
  }
]
```

Названия входных полей задаются в `configs/field_aliases.json`. Некорректные категории пропускаются, а сведения об
ошибках записываются в журнал.

## Тестирование

Запуск всех тестов:

```bash
poetry run pytest
```

Запуск тестов с покрытием модулей из `src`:

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=100
```

Текущий тестовый набор обеспечивает 100% покрытия исходного кода.

## Проверка качества кода

```bash
poetry run black --check src tests main.py
poetry run isort --check-only src tests main.py
poetry run flake8 src tests main.py
poetry run mypy src tests main.py
```

Автоматическое форматирование:

```bash
poetry run black src tests main.py
poetry run isort src tests main.py
```

## Логирование

При работе модулей автоматически создаётся каталог `logs`:

- `readers.log` — чтение JSON и Excel;
- `fields.log` — загрузка алиасов и поиск полей;
- `utils.log` — создание категорий и товаров из JSON.

