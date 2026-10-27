# Online Store

Учебный Python-проект с моделями товаров и категорий интернет-магазина. Проект поддерживает ручное создание
объектов, загрузку каталога из JSON, поиск полей по настраиваемым алиасам и журналирование операций чтения данных.

## Возможности

- создание товаров с названием, описанием, ценой и количеством на складе;
- общий абстрактный класс `BaseProduct` для всех товаров;
- журналирование создания товаров через миксин `MixinLog`;
- специализированные товары `Smartphone` и `LawnGrass`, унаследованные от `Product`;
- оформление заказа одного товара через класс `Order`;
- общий абстрактный контейнер для категорий и заказов;
- создание категорий со списком товаров;
- хранение списка товаров и цены в приватных атрибутах;
- контролируемое добавление товаров через `Category.add_product()`;
- создание и объединение одноимённых товаров через `Product.new_product()`;
- проверка и подтверждение изменения цены;
- строковое представление товаров и категорий через `__str__`;
- вычисление стоимости складских остатков через сложение товаров;
- последовательный перебор товаров категории с помощью `CategoryIterator`;
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
│   ├── base_product.py
│   ├── category.py
│   ├── category_iterator.py
│   ├── fields.py
│   ├── lawn_grass.py
│   ├── mixin_log.py
│   ├── order.py
│   ├── product.py
│   ├── product_container.py
│   ├── readers.py
│   ├── smartphone.py
│   └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_base_product.py
│   ├── test_category.py
│   ├── test_category_iterator.py
│   ├── test_fields.py
│   ├── test_lawn_grass.py
│   ├── test_order.py
│   ├── test_package.py
│   ├── test_product.py
│   ├── test_readers.py
│   ├── test_smartphone.py
│   └── test_utils.py
├── main.py
├── pyproject.toml
└── README.md
```

## Модули и функции

### `src.base_product`

Модуль содержит абстрактный класс `BaseProduct`, унаследованный от `ABC`. Он определяет общие свойства любого
товара: `name`, `description`, приватную цену и `quantity`.

Конструктор отмечен декоратором `@abstractmethod`, поэтому напрямую создать `BaseProduct` нельзя. При этом
конструктор содержит общую реализацию, которую `Product` вызывает через цепочку `super()`.

В базовый класс вынесены:

- property `price` с проверкой и подтверждением снижения цены;
- общее строковое представление `__str__()`;
- общая инициализация товарных характеристик.

### `src.mixin_log`

Модуль содержит `MixinLog` — миксин журналирования создания объектов. Его конструктор передаёт аргументы следующему
классу в MRO через `super()`, а после завершения инициализации печатает `repr(self)`.

Метод `__repr__()` анализирует сигнатуру конструктора фактического класса и формирует строку с именем класса и всеми
параметрами создания.

### `src.product`

Модуль содержит класс `Product`, представляющий одну товарную позицию. Он использует множественное наследование:

```python
class Product(MixinLog, BaseProduct):
    ...
```

Атрибуты объекта:

- `name: str` — название товара;
- `description: str` — описание товара;
- `quantity: int` — количество товара в наличии.

Приватная цена, property `price` и `__str__()` наследуются от `BaseProduct`.

Конструктор:

```python
Product(name: str, description: str, price: float, quantity: int)
```

Конструктор передаёт параметры дальше по MRO: сначала в `MixinLog`, затем в `BaseProduct`. После общей инициализации
миксин выводит созданный объект.

Методы:

- `new_product(product_data, products=None)` — создаёт новый товар из словаря или объединяет его с одноимённым;
- `price` — property для чтения и контролируемого изменения цены;
- `__str__()` — возвращает сведения о товаре в удобном для вывода формате;
- `__add__(other)` — возвращает полную стоимость остатков двух товаров.

### `src.smartphone`

Модуль содержит класс `Smartphone`, унаследованный от `Product`. Он получает все общие свойства и методы товара и
добавляет характеристики смартфона:

- `efficiency: float` — производительность;
- `model: str` — модель;
- `memory: int` — объём встроенной памяти;
- `color: str` — цвет.

Конструктор сначала сохраняет специальные свойства смартфона, а затем передаёт общие параметры в
`Product.__init__()` через `super()`. Благодаря этому `MixinLog` видит все параметры готового объекта.

### `src.lawn_grass`

Модуль содержит класс `LawnGrass`, также унаследованный от `Product`. Дополнительные свойства:

- `country: str` — страна-производитель;
- `germination_period: str` — срок прорастания;
- `color: str` — цвет.

Общие поля `name`, `description`, `price` и `quantity`, а также методы управления ценой, строкового отображения и
сложения наследуются от `Product`.

### `src.product_container`

Модуль содержит общий абстрактный класс `ProductContainer` для объектов, которые содержат товарные позиции.
Абстрактный метод `_stock_items()` задаёт контракт получения пар «цена — количество».

На основе этих данных базовый класс реализует два общих property:

- `total_quantity` — суммарное количество товаров;
- `total_cost` — суммарная стоимость товаров.

Класс нельзя создать напрямую. Его наследниками являются `Category` и `Order`.

### `src.category`

Модуль содержит класс `Category`, объединяющий товары в категорию и наследующий `ProductContainer`.

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
- `products` — property, возвращающий строковое представление товаров;
- `__str__()` — возвращает название категории и общий остаток всех её товаров;
- `_stock_items()` — передаёт базовому контейнеру цены и остатки товаров.

Через `ProductContainer` категория также предоставляет `total_quantity` и `total_cost`.

### `src.order`

Модуль содержит класс `Order`, представляющий заказ ровно одного товара. Класс наследует `ProductContainer` и
содержит:

- `product` — ссылку на купленный `Product` или его наследника;
- `quantity` — приобретённое количество;
- `total_cost` — итоговую стоимость заказа;
- `total_quantity` — количество товара в заказе.

Цена фиксируется в момент создания заказа. Последующее изменение цены исходного товара не изменяет уже рассчитанную
стоимость заказа. Передача объекта, не являющегося `Product`, вызывает `TypeError`.

### `src.category_iterator`

Модуль содержит вспомогательный класс `CategoryIterator`, предназначенный для последовательного перебора приватного
списка товаров категории.

Конструктор:

```python
CategoryIterator(category: Category)
```

Методы:

- `__iter__()` — сбрасывает текущую позицию и возвращает сам итератор;
- `__next__()` — возвращает очередной объект `Product`, а после последнего товара вызывает `StopIteration`.

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

Корневой пакет экспортирует основные модели, абстракции и миксин, поэтому их можно импортировать напрямую:

```python
from src import (
    BaseProduct,
    Category,
    CategoryIterator,
    LawnGrass,
    MixinLog,
    Order,
    Product,
    ProductContainer,
    Smartphone,
)
```

### `main.py`

Демонстрационный модуль создаёт смартфоны и газонную траву, проверяет сложение одинаковых и разных классов, добавляет
товары в категории и демонстрирует обработку `TypeError`. Исполняемый код защищён условием
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

## Иерархия товарных классов

`Product` остаётся базовым классом для обычных товаров. `Smartphone` и `LawnGrass` расширяют его специальными
характеристиками и наследуют общую работу с названием, описанием, ценой, остатком и операторами.

Создание смартфона:

```python
from src.smartphone import Smartphone

smartphone = Smartphone(
    name="Samsung Galaxy S23 Ultra",
    description="256GB, Серый цвет, 200MP камера",
    price=180000.0,
    quantity=5,
    efficiency=95.5,
    model="S23 Ultra",
    memory=256,
    color="Серый",
)
```

Создание газонной травы:

```python
from src.lawn_grass import LawnGrass

grass = LawnGrass(
    name="Газонная трава",
    description="Элитная трава для газона",
    price=500.0,
    quantity=20,
    country="Россия",
    germination_period="7 дней",
    color="Зелёный",
)
```

Оба объекта являются экземплярами `Product`, поэтому их можно добавлять в категории и использовать с унаследованной
функциональностью:

```python
isinstance(smartphone, Product)  # True
isinstance(grass, Product)       # True
```

## Абстрактный класс товара

`BaseProduct` задаёт обязательный интерфейс и общую реализацию для всех товаров. Он использует `ABC` и
`@abstractmethod`:

```python
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        ...
```

Напрямую создать `BaseProduct` нельзя — Python вызовет `TypeError`. Цепочка наследования товарных классов выглядит
так:

```text
BaseProduct
└── Product
    ├── Smartphone
    └── LawnGrass
```

Общая инициализация, приватная цена, её геттер и сеттер, а также строковое представление описаны один раз в
`BaseProduct` и доступны всем наследникам.

## Миксин журналирования

`MixinLog` добавлен первым в цепочку множественного наследования `Product`:

```python
class Product(MixinLog, BaseProduct):
    ...
```

Порядок важен: вызов `Product.__init__()` переходит в `MixinLog.__init__()`, тот через `super()` вызывает
`BaseProduct.__init__()`, а затем печатает `repr` полностью созданного объекта.

```python
product = Product("Продукт1", "Описание продукта", 1200, 10)
```

Результат в консоли:

```text
Product('Продукт1', 'Описание продукта', 1200, 10)
```

Для наследников используется имя фактического класса и все параметры их конструкторов, например `Smartphone(...)`
или `LawnGrass(...)`.

## Заказы и общий товарный контейнер

`Category` и `Order` наследуют общий абстрактный класс `ProductContainer`. Оба класса предоставляют свойства
`total_quantity` и `total_cost`, но формируют товарные позиции по-разному:

- категория содержит произвольный список товаров;
- заказ содержит ровно один товар и приобретённое количество.

Пример заказа:

```python
from src.order import Order

product = Product("Кофе", "Зерновой кофе", 500.0, 10)
order = Order(product, 3)

print(order.product.name)    # Кофе
print(order.total_quantity)  # 3
print(order.total_cost)      # 1500.0
```

Стоимость сохраняется по цене на момент создания заказа:

```python
product.price = 600.0
print(order.total_cost)  # по-прежнему 1500.0
```

Для категории общие свойства рассчитываются по всем товарам:

```python
print(category.total_quantity)
print(category.total_cost)
```

## Приватный список товаров категории

Категория хранит товары в приватном атрибуте `__products`. Получить или заменить исходный список напрямую нельзя.
Новый товар добавляется только через метод `add_product()`:

```python
category = Category("Смартфоны", "Смартфоны и аксессуары")
category.add_product(phone)
```

Метод принимает произвольный объект на границе API, проверяет его через `isinstance()` и `issubclass()`, а затем
добавляет в приватный список и увеличивает `Category.product_count`. Разрешены обычные `Product`, `Smartphone`,
`LawnGrass` и другие наследники `Product`. Передача объекта другого типа приводит к `TypeError`.

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

Метод использует `cls(**product_data)` и возвращаемый тип `Self`, поэтому фабрика работает полиморфно. При вызове
`Smartphone.new_product()` создаётся объект `Smartphone`, если словарь содержит все специальные поля смартфона.

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

## Строковое представление объектов

Метод `Product.__str__()` возвращает данные товара в формате:

```text
Название продукта, 80 руб. Остаток: 15 шт.
```

Пример:

```python
product = Product("Кофе", "Зерновой кофе", 80, 15)
print(product)
```

Геттер `Category.products` использует строковое представление каждого товара и объединяет результаты:

```python
print(category.products)
```

Метод `Category.__str__()` суммирует значения `quantity` всех товаров категории:

```python
print(category)
```

Формат результата:

```text
Название категории, количество продуктов: 200 шт.
```

Здесь учитывается фактическое количество единиц на складе, а не количество товарных позиций.

## Сложение товаров

Оператор `+` для двух объектов одного товарного класса возвращает полную стоимость обоих складских остатков:

```python
product_a = Product("Товар A", "Описание", 100, 10)
product_b = Product("Товар B", "Описание", 200, 2)

total_cost = product_a + product_b
print(total_cost)  # 1400
```

Расчёт выполняется по формуле:

```text
цена A × количество A + цена B × количество B
```

Перед вычислением `Product.__add__()` сравнивает точные классы операндов через `type()`. Поэтому разрешены операции
`Product + Product`, `Smartphone + Smartphone` и `LawnGrass + LawnGrass`. Смешивать классы нельзя:

```python
smartphone + grass  # TypeError
product_a + smartphone  # TypeError
```

Это ограничение действует и для базового класса: `Product` нельзя складывать с его наследником, несмотря на
`isinstance(smartphone, Product) == True`.

## Безопасное добавление товаров в категорию

`Category.add_product()` принимает значение типа `object`, чтобы проверочный код мог передать произвольный объект и
получить контролируемый `TypeError` во время выполнения. Внутри метода выполняются обе проверки:

```python
if not isinstance(product, Product) or not issubclass(type(product), Product):
    raise TypeError("Добавлять можно только объекты класса Product")
```

Пример обработки неверного значения:

```python
try:
    category.add_product("Not a product")
except TypeError:
    print("В категорию можно добавлять только товары")
```

Аннотация `object` также позволяет этому проверочному сценарию проходить `mypy`: метод принимает объект любого типа,
но самостоятельно проверяет его перед записью в приватный список.

## Перебор товаров категории

`CategoryIterator` позволяет перебирать товары категории в цикле `for`, не предоставляя пользователю прямой доступ
к приватному списку `Category.__products`:

```python
from src.category_iterator import CategoryIterator

iterator = CategoryIterator(category)

for product in iterator:
    print(product)
```

Итератор сохраняет категорию и текущий индекс. `__iter__()` сбрасывает индекс в начало, а `__next__()` возвращает
очередной `Product`. После завершения списка вызывается `StopIteration`, и цикл `for` останавливается автоматически.

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

