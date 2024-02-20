---
title: Crazy Shapes

---


# Shapes and Colors

Here is the program we created to make squares with loops. Try modifying this 
program to make other shapes. Try some of these things:

* Change the number of sides
* Change the angle the turtle turns ( the `left` variable )
  * Try numbers that are even sections of a cirle, like 60, 45, 90 or 40
  * Try numbers that aren't even seconds of a circle, like 172 or 43


<iframe width="100%" height="358.8" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%20%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0Atina.speed%280%29%0A%0Aforward%20%3D%2050%0Aleft%20%3D%2090%0Asides%20%3D%204%0A%0Adef%20side%28turtle%2C%20forward%2C%20left%29%3A%0A%20%20turtle.forward%28forward%29%0A%20%20turtle.left%28left%29%0A%0Afor%20i%20in%20range%28sides%29%3A%0A%20%20side%28tina%2C%20forward%2C%20left%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Here are some more ideas for you. You can put a loop inside a loop! Try this
program. 

<iframe width="100%" height="291.6" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0Atina.speed%280%29%0A%0Aleft%20%3D%2020%0A%0Afor%20i%20in%20range%286%29%3A%0A%20%20for%20forward%20in%20range%28-50%2C50%2C10%29%3A%0A%20%20%20%20tina.forward%28forward%29%0A%20%20%20%20tina.left%28left%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Here is another crazy program: 


<iframe width="100%" height="442.8" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0Atina.speed%280%29%0A%0Aforward%20%3D%2050%0A%0A%0Adef%20side%28turtle%2C%20forward%2C%20left%29%3A%0A%20%20turtle.forward%28forward%29%0A%20%20turtle.left%28left%29%0A%0A%0Adef%20make_shape%28turtle%2C%20forward%2C%20left%2C%20sides%29%3A%0A%20%20for%20i%20in%20range%28sides%29%3A%0A%20%20%20%20side%28turtle%2C%20forward%2C%20left%29%0A%0Afor%20sides%20in%20range%284%2C%209%29%3A%0A%20%20left%20%3D%20360%20/%20sides%0A%20%20make_shape%28tina%2C%20forward%2C%20left%2C%20sides%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Now try creating your own crazy progam. This time, you will start from an empty
file, so copy parts from other programs to get started. 

<iframe width="100%" height="600" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>


Now we can get to writing a more complex program. Use what you know about Tina the Turtle from previous programs, and what you've just learned about loops to write the program below. Read the comments for hints about what you should do. 

<iframe width="100%" height="829.2" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0A%0A%0Awindow%20%3D%20turtle.Screen%28%29%0Awindow.bgcolor%28%27white%27%29%0A%0A%23%20This%20code%20makes%20a%20new%20Turtle.%20Pick%20a%20new%20%0A%23%20name%20for%20the%20turtle%0Amy_turtle%20%3D%20turtle.Turtle%28%29%0A%0A%23%20Make%20your%20turtle%27s%20shape%20%27turtle%27%2C%20.shape%28%27turtle%27%29%0A%0A%23%20Set%20your%20turtle%27s%20speed%20using%20.speed%282%29%0A%0A%23%20Set%20your%20turtle%27s%20color%20using%20.color%28%27green%27%29%20%0A%23%20and%20.pencolor%28%27blue%27%29%0A%0A%23%20Move%20your%20turtle%20forward%20using%20.forward%28100%29%0A%23%20TEST%20%20%20%20Did%20your%20turtle%20move%20forward%3F%0A%0A%23%20Move%20your%20turtle%20left%20or%20right%20using%20.left%2890%29%20%0A%23%20or%20.right%2890%29%0A%0A%23%20Now%20put%20the%20forward%20and%20left/right%20code%20into%20a%20for%20%0A%23%20loop%20to%20repeat%204%20times.%0A%23%20TEST%20%20%20%20Did%20your%20turtle%20draw%20a%20square%3F%0A%0A%23%20Move%20your%20turtle%20to%20a%20new%20place%20on%20the%20%0A%23%20screen%20using%20.goto%28x%2C%20y%29%20x%3D0%20and%20y%3D0%20is%20the%20%0A%23%20center%20of%20the%20screen%0A%0A%23%20Have%20your%20turtle%20draw%20a%20circle%20using%20%0A%23%20.circle%28radius%2C%20steps%3D30%29%0A%23%20TEST%20%20%20%20Did%20your%20turtle%20draw%20a%20circle%3F%0A%0A%23%20Add%20color%20to%20your%20shape%20by%20adding%20.begin_fill%28%29%20%0A%23%20before%20drawing%20the%20circle%0A%23%20and%20.end_fill%28%29%20below%0A%0A%23%20Draw%203%20more%20shapes%20with%20different%20fill%20colors%21%0A%0A%23%20%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%20DO%20NOT%20EDIT%20THE%20CODE%20BELOW%20%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%0Aturtle.done%28%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>



