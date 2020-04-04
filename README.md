# Wrapper for the CoCoCo: Collocations, Collligations, and Corpora tool

This is a python CLI for the CoCoCo API. It allows for finding the
significant values of an unknown element in a sequence of 2 or 3 words.

## Contents
1. [CoCoCoDriver.py](#CoCoCoDriver.py)
1. [get_valency.py](#get_valency.py)
1. [utility.py](#utility.py)

The CoCoCo website GUI is located at [http://cococo.cosyco.ru/](http://cococo.cosyco.ru/).

Read more about the CoCoCo project [here](http://cococo.cosyco.ru/about.html).

<hr/>

## CoCoCoDriver.py
This module is the core wrapper for the CoCoCo API. 

To see the usage, enter the following command in a cmd or bash terminal in the same directory as the *CoCoCoDriver.py* file:
```
python3 CoCoCoDriver.py -h
```

### Poses / Parts of Speech
The *-pos1*, *-pos2*, and *-pos3* options allow for specifying the part-of-speech tag for words in the word sequence:

Pose | Part-of-Speech | Часть речи
--- | --- | --- 
S | Noun | Существительное
A | Adjective | Прилагательное
V | Verb | Глагол
ADV | Adverb | Наречие
PARTCP | Participle | Причастие
GER | gerund | Деепричастие
SPRO | Pronoun | Местоим. существ.
APRO | Adjective pronoun | Местоим. прилаг.
PR | Preposition | Предлог
CONJ | Conjugation | Союз
ADVPRO | Pronoun adverb | Местоим. наречие
NUM | Numeral | Колич. числит.
ANUM | Ordinal numeral | Порядк. числит.
PART | Participle | Частица
INTJ | Interjection | Междометие
PRAEDIC | Predicate | Предикатив
PARENTH | Parenthesis | Вводное слово
SYM | ??? | SYM
X | ??? | X

### Word Features
Depending on the corpus, there are different possible word feature parameters available:

#### RNC & IRU Word Features
Feature | Options | Разметка | Выборы
--- | --- | --- | ---
transitivity | ['tran', 'intr'] | переходность | ['переходный', 'непереходный']
gender | ['n', 'm', 'f', 'mf'] | род | ['средний', 'мужской', 'женский', 'общий']
number | ['sg', 'pl'] | число | ['единственное', 'множественное']
case | ['nom', 'gen', 'gen2', 'dat', 'acc', 'acc2', 'ins', 'loc', 'loc2', 'voc', 'adnum'] | падеж | ['именительный', 'родительный', 'родительный2', 'дательный', 'винительный', 'винительный2', 'творительный', 'предложный', 'предложный2', 'звательный', 'счётная форма']
animacy | ['inan', 'anim'] | одушевленность |['неодушевленный', 'одушевленный']
degree | ['comp', 'supr', 'comp2', 'p'] | степень |['сравнительная', 'превосходная', 'сравнительная2', 'положительная']
mood | ['indic', 'inf', 'imper', 'imper2'] | наклонение | ['изъявительное', 'инфинитив', 'повелительное', 'повелительное2']
tense | ['praes', 'praet', 'fut'] | время | ['настоящее', 'прошедшее', 'будущее']
person | ['1p', '2p', '3p'] | лицо | ['первое', 'второе', 'третье']
voice | ['act', 'pass', 'med'] | залог | ['активный', 'пассивный', 'медиальный']
form | ['brev', 'plen'] | форма | ['краткая', 'полная']
aspect | ['pf', 'ipf'] | вид | ['совершенный', 'несовершенный']
name | ['persn', 'nonname'] | имя собств. | ['имя', 'не имя']
abbr | ['abbr', 'nonabbr'] | аббревиатура | ['аббревиатура', 'не аббревиатура']

#### Taiga Word Features
Feature | Options | Разметка | Выборы
--- | --- | --- | ---
gender | ['n', 'm', 'f'] | род | ['средний', 'мужской', 'женский']
animacy | ['inan', 'anim'] | одушевленность | ['неодушевленный', 'одушевленный']
number | ['sg', 'pl'] | число | ['единственное', 'множественное']
case | ['nom', 'gen', 'gen2', 'dat', 'acc', 'ins', 'loc', 'voc'] | падеж | ['именительный', 'родительный', 'родительный2', 'дательный', 'винительный', 'творительный', 'предложный', 'звательный']
variant | ['short','long'] | форма | ['краткая','полная']
degree | ['comp', 'supr', 'p'] | степень | ['сравнительная', 'превосходная', 'положительная']
aspect | ['pf', 'ipf'] | вид | ['совершенный', 'несовершенный']
voice | ['act', 'pass', 'med'] | залог | ['активный', 'пассивный', 'медиальный']
mood | ['indic', 'imper','cnd'] | наклонение | ['изъявительное', 'повелительное', 'условное']
tense | ['praes', 'praet', 'fut'] | время | ['настоящее', 'прошедшее', 'будущее']
person | ['1p', '2p', '3p'] | лицо | ['первое', 'второе', 'третье']
foreign | ['Yes'] | иностранное | ['да']
polarity | ['neg','pos'] | полярность | ['отрицательная','положительная']
proper | ['yes', 'no'] | имя собственное | ['да', 'нет']
verbform | ['fin', 'inf'] | форма глагола | ['личная', 'неличная']

### Examples:
[**python3 CoCoCoDriver.py -w1 читать RNC**](Example/driver1.txt)
*Print the server's .json response from searching "читать", "" from ruscorpora*

[**python3 CoCoCoDriver.py -v -n 3 -w1 быть -pos2 A -w3 человек RNC**](Example/driver2.txt)
*Print the GET request url & headers and response code*
*Then, print out the server's .json response from searching "быть", "", "человек" from ruscorpora*
*The second word is an adjective*

[**python3 CoCoCoDriver.py -v -n 3 -flem -w1 любить -pos2 A -w3 человек RNC**](Example/driver3.txt)
*Print the GET request url & headers and response code*
*Then, print out the server's .json response from searching "любить", "", "человек" from ruscorpora*
*The second word is an adjective and each word is a lemma*

[**python3 CoCoCoDriver.py -vv -w1 любовь -pos1 S -pos2 A -f2 "form=brev|" IRU**](Example/driver4.txt)
*Print the GET request url & headers and response code*
*Then, pretty print the server's .json response from searching "любовь", "", from I-RU*
*The first word is a noun and the second word is an adjective in short form*

<hr />

*The following code saves the CoCoCoDriver output to files*
*Print the GET request url & headers and response code*
*Then, pretty print the server's .json response from searching "жизнь", ""*
*The first word is a noun and the second word is an adjective in short form*
*Each command queries a subcorpus of the Taiga database:*
1. All subcorpora:  [**python3 CoCoCoDriver.py -vv -w1 жизнь -pos1 S -f1 "case=nom|" -pos2 A -f2 "variant=short|" Taiga > Example/All.txt**](Example/All.txt)
1. Social subcorpus: [**python3 CoCoCoDriver.py -vv -w1 жизнь -pos1 S -f1 "case=nom|" -pos2 A -f2 "variant=short|" Taiga -s Social > Example/Social.txt**](Example/Social.txt)
1. News subcorpus: [**python3 CoCoCoDriver.py -vv -w1 жизнь -pos1 S -f1 "case=nom|" -pos2 A -f2 "variant=short|" Taiga -s News > Example/News.txt**](Example/News.txt)
1. Poetry subcorpus: [**python3 CoCoCoDriver.py -vv -w1 жизнь -pos1 S -f1 "case=nom|" -pos2 A -f2 "variant=short|" Taiga -s Poetry > Example/Poetry.txt**](Example/Poetry.txt)

## get_valency.py
This module is a wrapper for the CoCoCoDriver module. It prints a tabularly formatted response of an 'advanced search' from the CoCoCo website.

Because this file imports the CoCoCoDriver module, it must be located in the same directory as the *CoCoCoDriver.py* file. The get_valency module accepts two sets of arguments:
1. First, the get_valency module arguments.
1. Next, the CoCoCoDriver module arguments.

To see the usage of the get_valency and CoCoCoDriver modules, enter the following command in a cmd or bash terminal in the same directory as the *get_valency.py* and *CoCoCoDriver.py* file:

```
python3 get_valency.py -h
python3 CoCoCoDriver.py -h
```

### Threshold
Threshold determines the amount of fvals to display for each feature:

Threshold | Approach | Подход 
--- | --- | ---
0 | Simple approach - first 3 ranks in the 'Rank' column | Простой подход - Первые 3 ранга в колонке Ranks
1 | Conservative approach - print out ranks that are above the median frequency ratio | Консерванитвный подход - Freq. ratio высше медианы
2 | Liberal approach - print out all ranks that are above the largest rank difference | Либеральный подход - Искать самую большую дистанцию между Ranks
3 | Diffiule approach - TODO | Сложный подход - TODO
4 | Everything - print out all ranks | Всё

### Examples
[**python3 get_valency.py -w1 читать RNC**](Example/valency1.txt)
*Print the valency for searching "читать", "" from ruscorpora*
*The default is threshold 0: Simple approach - first 3 ranks in the 'Rank' column*

[**python3 get_valency.py -t 4 -w1 читать RNC**](Example/valency2.txt)
*Print the valency for searching "читать", "" from ruscorpora*
*Use threshold 4: Everything - print out all ranks*

[**python3 get_valency.py -vv -t 1 -w1 читать RNC**](Example/valency3.txt)
*Verbosity 2 - print request header and url, and raw server's .json response*
*Print the valency for searching "читать", "" from ruscorpora*
*Use threshold 1: Conservative approach - print out ranks that are above the median frequency ratio*

[**python3 get_valency.py -vvv -t 2 -w1 читать RNC**](Example/valency4.txt)
*Verbosity 3 - print request header and url, and pretty print the server's .json response*
*Print the valency for searching "читать", "" from ruscorpora*
*Use threshold 2: Liberal approach - print out all ranks that are above the largest rank difference*

## utility.py
This module contains utility functions, such as printing a formatted debug message.
