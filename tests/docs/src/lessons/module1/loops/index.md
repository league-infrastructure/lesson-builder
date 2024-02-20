---
title: Make a Square with Loops

---


# Loops for Easy Squares

Here is how some students solve the last exercise, using variables to draw a square. 

```python
import turtle
tina = turtle.Turtle()
tina.shape("turtle")

forward = 50
left = 90

tina.forward(forward)
tina.left(left)

tina.forward(forward)
tina.left(left)

tina.forward(forward)
tina.left(left)

tina.forward(forward)
tina.left(left)

```


Notice that there is a lot of repetition in this program. Can we make this
program shorter by getting rid of the repetition? Yes, we can, with loops.  A
loop is a bit of code that causes the computer to do something multiple
times. Here is a loop for printing "Hello!" mutiple times. How many times do
you think it will print?

<iframe width="100%" height="207.60000000000002" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=for%20i%20in%20range%284%29%3A%0A%20%20%20%20print%28%22Hello%21%22%29%0A%0A%23%20Now%20change%20the%20program%20to%20make%20%0A%23%20it%20print%20hello%206%20times." frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Let's look at that in more detail:

```python
for i in range(4):
    print("Hello!")
```

The first line in the loop defines the loop and tells us how many times to do
the body of the loop. The body of the loop, the ` print("Hello!")` part,  is
indented. The ``range`` part will run the number of times inside the
parenthesis, in this case 4. 

The `i` part is also special; it is a variable. So, you could print it out too. 

```python
for i in range(4):
    print("Hello!", i)
```



## Make a Better Square. 

Here is our way of solving the square exercise. Can you edit this
program to make it much better, by replacing the repetition with a loop?

<iframe width="100%" height="409.2" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0A%0Aforward%20%3D%2050%0Aleft%20%3D%2090%0A%0Atina.forward%28forward%29%0Atina.left%28left%29%0A%0Atina.forward%28forward%29%0Atina.left%28left%29%0A%0Atina.forward%28forward%29%0Atina.left%28left%29%0A%0Atina.forward%28forward%29%0Atina.left%28left%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Once you have used a loop to help Tony make a square, try making other shapes,
like a triangle, a pentagon, or a hexagon, or maybe even a ... hendecagon.
(if you can figure out what that is. )


## Badgers Badgers Badgers

Use for loops (you will need more than one) to print the following lyrics from the Badger Song. You can only use the words “Badger”, “Mushroom” and “Snake” once each in your code.

<iframe width="560" height="315" src="https://www.youtube.com/embed/pzagBTcYsYQ?si=m3Vc66lQ4PhMfiFO" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Print 2 verses of the song as follows:

```
Badger, Badger, Badger, Badger, Badger, Badger, Badger,Badger, 
Badger,Badger, Badger, Badger, Mushroom, Mushroom

Badger, Badger, Badger,Badger, Badger, Badger, Badger,Badger, 
Badger, Badger, Badger, Badger, Mushroom, Mushroom

A Snake!!!
```

Or maybe: 🦡🦡🦡🦡🦡🦡🦡🦡🦡🦡🦡🦡🍄🍄 🦡🦡🦡🦡🦡🦡🦡🦡🦡🦡🦡🦡🍄🍄 🐍



<iframe width="100%" height="600" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>




## More about range

Another interesting things with the loops is that `range` can have more than
one number in it. If we put in two numbers, the values of `i` will go from
the first number to _one minus_ the second number, so if you want to print
out the numbers 4, 5, 6, 7, you would use `range(4,8)`:


```python 
for i in range(4, 7):
    print("Hello!", i)
```

Try that yourself. Write a program to print "Hello" next to all of the
numbers from 10 to 20:

<iframe width="100%" height="190.8" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=%23%20Change%20me%20to%20print%20Hello%20for%20the%20%0A%23%20numbers%20from%2010%20to%2020%0A%0Afor%20i%20in%20range%284%29%3A%0A%20%20%20%20print%28%22Hello%21%22%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

But there are more interesting things about `range()`: It can take a _third_
number, and all three of the numbers can be negative or positive. So you
could also type `range(10,20, 2)` or `range(20,10,-1)`. Let's explore `range
()` to figure out what the third number does. 

<iframe width="100%" height="325.20000000000005" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=%23%20Change%20me%20so%20range%28%29%20has%20three%20numbers%2C%20%0A%23%20and%20try%20to%20figure%20out%20what%20the%20third%0A%23%20number%20does.%20What%20happens%20if%20you%20make%20%0A%23%20some%20of%20the%20numbers%20negative%3F%0A%0A%23%20HINT%3A%20If%20the%20third%20number%20is%20negative%2C%20%0A%23%20the%20first%20number%20should%20be%20%2Abigger%2A%20than%0A%23%20the%20second%2C%20but%20if%20the%20third%20number%20is%20positive%2C%20%0A%23%20it%20should%20be%20smaller.%20%0A%0Afor%20i%20in%20range%2810%29%3A%0A%20%20%20%20print%28%22Hello%21%22%2C%20i%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>
