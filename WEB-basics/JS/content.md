# JavaScript

## Всплывающее окно
Не делать так
```javascript
alert("text");
```

## Отладочная инфа
```javascript
console.log("info");
```

## Сложение строк
Если число складывается со строкой, то получается строка.

## Переменные
```javascript
let value = 219;
```

## Массивы
Однотипные, индексация с 0.
```javascript
let arr = [1, 2, 3];
```

## Свойства
* `<str>.length` – количество символов

## Math
* `random()` – [0; 1)
* `floor()` – округлить число

## Функции
```javascript
function hello() {}
```

## Работа с веб-страницей
Всё находится в `document`.
* `querySelector('.classname')` – выбрать элемент страницы <br/>
Изменить текст элемента
```javascript
let txt = querySelector('.classname');
txt.textContent = ...
```
* поменять стиль
```javascript
elem.style.fontSize = '12px';
```

## Слушатель
Позволяет добавить реакцию на некоторое действие
```javascript
elem.addEventListener('click', f1);
elem.addEventListener('click', function () {
    return -1;
});
```

## Объекты
Что-то вроде словарей
```javascript
let user = {
    name: 'Anna',
    age: 19,
    married: true
};

console.log(user.name)
```

## Внешние библиотеки
Подключаются через `script src=...` <br/>

### Smoothly
[Анимация](https://code.s3.yandex.net/web-code/smoothly/index.html)

## Цикл
```javascript
for (let i = 0; i <= 10; i++) {}
```
