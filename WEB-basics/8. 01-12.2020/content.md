# Пара 01-12-2020
## Введение в JS


### Вывод
* Всплывающее окно, останавливает выполнение программы: `alert()`.
* В консоль: `console.log()`.


### Ввод
* Всплывающее окно: `prompt('Enter a number: ')`
* Диалоговое окно, OK и Cancel: `confirm(Истина или ложь)`


### Типы данных
* `string`
    * с обратными кавычками – шаблонный литерал.
* `number`
    * `5e8` – 5 * 10^8
    * `+Infinity`
    * `-Infinity`
    * `NaN`
* `null` – пустой притив, ничего не содержит.
* `boolean` – логика.
* `undefined` – переменная, которой ничего не присвоено.


### Форматирование строк
Только с обратными кавычками.
```javascript
console.log(`10 + 10 = ${10+10}`)
```


### Операторы
* `+` – число + строка = число.
* `-`
* `*`
* `/`
* `%`
* `**`
* `унарный +` – преобразует данные к числу.


### Логические операции
* `&&`
* `||`
* `==` – приводит операнды к одному типу, сравнивает их. Если сраваниваются объекты, то проверяется, что они ссылаются на один участок памяти.
* `===`  – строгое равенство без преобразований.
* `!=`
* `num % 2 == 0 ? 'Чётное': 'Нечётное'`


### Переменные
* `var` – как локальные, так и глобальные переменные.
* `let` – только локальные переменные.
* `const` – константа, только для чтения.


## TODO
* Ещё 6 лабораторных работ