---
title: Variables

---


# Variables

A variable is a way to store information, like a box where you can put
something for using later. Variables have names, which is like a label on the
box. You can set or change change the contents of the box with the '=',
which we call the 'assignment operator'.

Here is an examples of assigning a variable: 

```python
tony = turtle.Turtle()
```

Surprise! You've been using variables all along! Here the name of the variable 
is `tony` and the contents of the variable, like the contents of a box, is a turtle. 


Here are some more examples, storing numnbers into variables 

```python
apples = 10
oranges = 6
```

How many fruits do we have? We can add them: 

```python 
print(apples+oranges)
16
```

Since variables can hold numbers, and we can add numbers, so we can add the variables to get the answer. 

Try it yourself. But first, notice the last line, which has `assert` on it, which means, 
'complain if this is not true'. The assert will produce an error message if
 your variables don't add to 15.  Make the variables add to 15 to make the
 `assert` happy, then try making it unhappy by making them add to any other
 number, just to see whan an error looks like. We will sometimes use `assert`
 to check if your answers are correct. 

<iframe width="100%" height="250" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=%23%20Make%20the%20numbers%20add%20to%2015%0A%0Ax%20%3D%2010%0Ay%20%3D%20%20%20%23%20Finish%20the%20line%20with%20the%20right%20string%0A%0Aassert%20x%20%2B%20y%20%3D%3D%2015%2C%20%22The%20sum%20should%20be%2015%22%0A%0Aprint%28%22Yeah%21%20%F0%9F%8E%89%22%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>


We've already seen addition, but we can also subtract, multiply and divide.
However, multiplication and division use symbols that are a little different
from what you are used to:

* Multiplication uses "*", so `10*5 == 50`
* Division uses "/", so `50/5 == 10`

For instance: 

```python 
pizza_slices = 16
people = 4
pizza_per_person = pizza_slices / 4

assert pizza_per_person == 4 # What is this????

```

## Strings

In Python, there are many different types of things we can put in the
variable, including numbers and words, which we will call "text"
or "strings".

It might seem weird that words are called "strings" but it's not if you think
about it like a computer, which is that it is made of letters, one after the other, like a friendship bracelet. 

<img src="https://i.pinimg.com/originals/86/47/ce/8647ce37cd76a5188c04be03d8969ad5.jpg" alt="Friendship Bracelet" width="200"/>

Strings work a bit differently than numbers; when we add them, they are _concatenated_ which means "combined end to end"

```python 
h = "Hello"
s = " "
w = "World"
print(h+s+w)
Hello World
```

Now, try the same thing we did with numbers, but with strings: 

<iframe width="100%" height="250" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=%23%20Make%20the%20numbers%20add%20to%2015%0A%0Ax%20%3D%20%22Hello%20%22%0Ay%20%3D%20%20%20%23%20Finish%20the%20line%20with%20the%20right%20number%0A%0Aassert%20x%20%2B%20y%20%3D%3D%20%22Hello%20World%22%0Aprint%28%22Yeah%21%20%22%2Bx%2By%2B%22%20%F0%9F%8E%89%22%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>


We can use variables to store commands for our turtle. Let's start with a program that we created 
earlier, but update it to use variables. 

<iframe width="100%" height="500" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0A%0Aforward%20%3D%20%23%20Amount%20to%20move%20forward%0Aleft%20%3D%20%23%20amount%20to%20turn%20left%0A%0A%0A%23%20In%20the%20lines%20below%2C%20use%20the%20variables%20%0A%23%20instead%20of%20numbers.%20%0A%0Atina.forward%2850%29%0Atina.left%2890%29%0A%0Atina.forward%2850%29%0Atina.left%2890%29%0A%0Atina.forward%2850%29%0Atina.left%2890%29%0A%0Atina.forward%2850%29%0Atina.left%2890%29%0A%0A%23%20Now%2C%20try%20changing%20the%20values%20for%20%0A%23%20forward%20and%20left%20and%20see%20what%20new%20%0A%23%20shapes%20Tina%20draws." frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>
