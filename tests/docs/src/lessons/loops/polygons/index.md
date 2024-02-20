---
title: Polygons

---


# Polygons

A few lessons ago you told Tony the Turtle how to make a square. Did you also
make a polygon, like a hexagon?


Remember how we told Tony to make a square with a loop. Here is the really
important part of that program: 

```python
for i in range(4):
    tony.forward(50)
    tony.left(90)

```

Notice that Tony turned *90* degrees each time, and he turned *4* times. How
many degrees did he turn in total? Well, 90 * 4 == 360, right? And what is
turning 360 degrees? Its turning back to where you started!

For every polygon, if Tony is going to get back to where he started,  needs to
turn 360 degrees, no matter how many sides it has. So, lets combine what we've learned
about loops and variables to make Tony make other shapes. 


<iframe width="100%" height="500" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%20as%20turtle%0A%0Awindow%20%3D%20turtle.Screen%28%29%0Awindow.bgcolor%28%27white%27%29%0Atony%20%3D%20turtle.Turtle%28%29%0A%0A%23%20Make%20a%20new%20variable%20for%20the%20number%20of%20sides%0A%23%20of%20the%20shape%0A%0Asides%20%3D%20%23%20Put%20in%20a%20number%0A%0Adistance%20%3D%2050%20%23%20you%20can%20change%20how%20far%20Tony%20goes%0A%0A%23%20Put%20the%20number%20of%20sides%20into%20the%0A%23%20range%20statement%0Afor%20i%20in%20range%28%29%3A%0A%20%20%20%20%23%20How%20many%20degrees%20does%20tony%20have%20to%20turn%3F%0A%20%20%20%20%23%20Remember%20that%20degrees%20%2A%20sides%20%3D%20360.%20Also%0A%20%20%20%20%23%20remember%20that%20division%20uses%20%22/%22%22%0A%20%20%20%20degrees%20%3D%20%20%23%20Write%20an%20equation%0A%20%20%20%20tony.forward%28distance%29%0A%20%20%20%20tony.left%28degrees%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>


Now see if you can use 2 loops to make Tony make multiple shapes. Here is a
hint: In the loop statement with the range, like `for i in rage(4)`, the `i`
is a variable that you can use like other variables in your program. Also,
range can take two numbers; the first is the starting number, and the second
is one more than the ending number.

<iframe width="100%" height="250" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=for%20i%20in%20range%284%2C%207%29%3A%0A%20%20%20%20print%28i%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>


Now, can you use this new information to add a second loop to your program
that makes Tony draw multiple shapes?
