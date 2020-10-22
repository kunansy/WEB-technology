# Script

### Introduction
#### [first slide]
* Hello there and welcome. 
* I am Kolobov Kiril, a student of Moscow Polytechnic University. 
* Today I'm going to tell you about Cython – a Python libraby.
#### [slide 2, example of Cython syntax]
* I guess all Python programmers should know about it, because it let us to speed the code up.
* First of all I will tell you about the basics diferences between Python and C, then I will go on to the syntax of the library and finally I will differ the effectiveness of the Python code and code with Cython.
* It will take about ten minutes to represent some features of the library.
* Let's start.
#### [slide 3, slow Python vs quick C++]
* Python is a very slow language as you can see, but we can fix it.

### Body
#### [slide 4, compile vs interpreter]
* Basicly there are two types of programming languages: compiled such as C, Go, C++, you know, Hascell etc and interpretered, such as Python, JavaScript and things like that.
#### [slide 5, variable definition in C++, `int x; int x = 12;` <This is C++>]
* In compiled languages you should directly tell a compiler: "Hey, I want to create integer variable x with a value or without it". 
#### [slide 6, x = 12.1]
* And you can store there only integer values (in x, in this case of course). 
#### [slide 7, `x = 12, x = 12.1, x = '12'`]
* But in interpreted languages you can store anything, any data type at all.
* This is why interpreted languages is slower than compiled, one of the main reason. 
#### [slide 8, but python...]
* But... In Python you can do anything, including writing a code in C.
#### [slide 9, Python -> Cython, `do_math()`]
* Look at that, we need just change file type to pyx instead of py, define data types explicetly, use a special library and write cimport instead of import.
* This is just an example, it does some mathematics operation repeatedly.
* You know, cycle is one of the thing where Python is slow.
#### [slide 10, setup]
* Then we should compile our programm using setup.py, 
#### [slide 11, bash]
* Because C is a compiled language as I mentioned before.
* Well, let's make a speed test.
#### [slide 12, speed test, Python]
* Python code did the task in ... Let's see Cython results.
#### [slide 13, speed test, Python vs Cython]
* Oh, gosh... And Cython did the same task ... times faster. Not percents, but times.
* And that is amazing.
#### [slide 15, Cython is amazing]

### Conclusion
* So, as I said earlier all Python programmers should know about Cython. It allows us to make the code faster a lot.
#### [slide 16, Thank you for attention]
* Thank you for attention, I am ready to answer your questions now.
