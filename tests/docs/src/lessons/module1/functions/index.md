---
title: Functions

---


# Functions

A function is like a recipe, a series of steps that the computer will follow.
But we've been giving the compter steps to follow all along! What is different
about a function? The important thing about functions is that they have
names, inputs, and outputs.

Let's imagine that you have this program to add two numbers:

```python 
a = 10
b = 20
c = a + b
print(c)
```

It works! But what if you want to add more than once? You'd have to write something like: 

```python 
a = 10
b = 20
c = a + b
print(c)

a = 5
b = 6
c = a + b
print(c)

```

With a function, we can stop repeating ourselves. Let's make a function for addition: 

```python
def add(a, b):
	c = a + b
	return c

print(add(10,20))
print(add(5,6))
```

Notice that the important part of the addition procedure is now inside the
function. The `def` keyword says that we are going to *def*ine a fuction, and the
variables in the parentheses, `(a,b)` are called the _argument list_. Those are the inputs to 
the function. 

The last line, `return c` is the output from the function. That is the value that we want to print. 

Notice that you've already seen functions, we've been using them all along. Here is
part of the first program we made:

```python
tina = turtle.Turtle()
tina.shape('turtle')
```


Try running this program and see what you get.

<iframe width="100%" height="207.60000000000002" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=def%20add%28a%2C%20b%29%3A%0A%09c%20%3D%20a%20%2B%20b%0A%09return%20c%0A%0Aprint%28add%2810%2C20%29%29%0Aprint%28add%285%2C6%29%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Now re-write the program to multiply the two numbers. 

<iframe width="100%" height="241.20000000000002" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=%23%20Change%20me%20to%20multiply%21%20Be%20sure%20to%20change%20the%0A%23%20name%20of%20the%20function.%20%0Adef%20add%28a%2C%20b%29%3A%0A%09c%20%3D%20a%20%2B%20b%0A%09return%20c%0A%0Aprint%28add%2810%2C20%29%29%0Aprint%28add%285%2C6%29%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

You can have a different number of arguments for the input to the function.
Re-write it again to multiply three numbers. 


<iframe width="100%" height="258.0" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=%23%20Change%20me%20to%20multiply%2C%20and%20make%20it%20multiply%20three%20numbers%21%0A%23%20Be%20sure%20to%20change%20the%20name%20of%20the%20function.%20%0Adef%20add%28a%2C%20b%29%3A%0A%09c%20%3D%20a%20%2B%20b%0A%09return%20c%0A%0Aprint%28add%2810%2C20%29%29%0Aprint%28add%285%2C6%29%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

## Make Five Cakes

Earlier we talked about how **functions are like recipes**. In this exercise,
we've already taught Tina the recipe for making a picture of a cake and she's
made three.  Tell her to make more cakes by **calling** the function with
different `x` and `y` locations at the very bottom of the program.  

How many cakes should she make?

<iframe width="100%" height="594.0" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%3Dturtle.Turtle%28%29%0Atina.shape%28%27turtle%27%29%0A%0Adef%20make_cake%28x%3D0%2C%20y%3D0%29%3A%0A%20%20%20%20tina.penup%28%29%0A%20%20%20%20tina.color%28%27pink%27%29%0A%20%20%20%20tina.goto%28x%2C%20y%29%0A%20%20%20%20tina.pendown%28%29%0A%20%20%20%20tina.begin_fill%28%29%0A%20%20%20%20tina.goto%28x%20%2B%2020%2C%20y%29%0A%20%20%20%20tina.goto%28x%20%2B%2020%2C%20y%20%2B%2020%29%0A%20%20%20%20tina.goto%28x%20-%2020%2C%20y%20%2B%2020%29%0A%20%20%20%20tina.goto%28x%20-%2020%2C%20y%29%0A%20%20%20%20tina.goto%28x%2C%20y%29%20%20%0A%20%20%20%20tina.end_fill%28%29%0A%20%20%20%20tina.goto%28x%2C%20y%20%2B%2020%29%0A%20%20%20%20tina.color%28%27yellow%27%29%0A%20%20%20%20tina.goto%28x%2C%20y%20%2B%2035%29%0A%20%20%20%20tina.goto%28x%2C%20y%20%2B%2030%29%0A%20%20%20%20tina.color%28%27black%27%29%0A%20%20%20%20tina.goto%28x%2C%20y%20%2B%2020%29%0A%20%20%20%20tina.penup%28%29%0A%20%20%20%20tina.goto%28x%2C%20y%20%2B%2010%29%0A%20%20%20%20%0Amake_cake%280%2C0%29%0Amake_cake%28-100%2C0%29%0Amake_cake%28100%2C0%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Hint: The first number in `make_cake()` is **how far left or right** Tina should go, while the second is **how high or low** she should go before starting to draw.

Run this program, then change the program how ever you want. Some things you can try: 
* Change the colors of the cakes
* Make the cakes bigger
* Put the cakes in different places
* Use a loop to make more cakes

## Functions and Loops

Let update a square function one more time. This time remove the redundancy in
the program with a loop, but also use a function; your loop should run a
function many times, and the function should draw part of the square. 

<iframe width="100%" height="560.4000000000001" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0A%0Aforward%20%3D%2050%0Aleft%20%3D%2090%0A%0A%23%20First%2C%20write%20a%20function%20that%20performs%0A%23%20the%20important%20part%20of%20the%20code%20below.%20%0A%23%20Be%20sure%20to%20include%20the%20correct%20arguments%0A%23%20for%20the%20variables.%20%0A%0A%23%20Second%2C%20call%20that%20function%20from%20a%20loop%0A%23%20to%20do%20it%20the%20right%20number%20of%20times.%20%0A%0A%0Atina.forward%28forward%29%0Atina.left%28left%29%0A%0Atina.forward%28forward%29%0Atina.left%28left%29%0A%0Atina.forward%28forward%29%0Atina.left%28left%29%0A%0Atina.forward%28forward%29%0Atina.left%28left%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

When your program is correctly drawing a square, try changing the 
variable to see what other shapes you can make. 


---

Thanks to Trinket.io for providing the 5 cakes assignment, part of their
[Hour of Python] (https://hourofpython.com/a-visual-introduction-to-python/) course.


