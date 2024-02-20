---
title: If and Else

---


# If and Else

All programming languages have a way of making choices, doing one thing or
the other. In Python we can make choices with `if`, `elif` and `else`. Here is
a simple program to tell you if a number is bigger than 10:

<iframe width="100%" height="375.6" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=while%20True%3A%20%23%20This%20loop%20will%20run%20until%20the%20%27break%27%0A%0A%20%20%20%20num%20%3D%20input%28%22Enter%20a%20number%3A%22%29%0A%20%20%20%20num%20%3D%20int%28num%29%20%23%20Make%20the%20input%20an%20integer%0A%0A%20%20%20%20if%20num%20%3D%3D%200%3A%0A%20%20%20%20%20%20%20%20break%20%23%20Exit%20the%20loop%20if%20the%20number%20is%200%0A%20%20%20%20%0A%20%20%20%20if%20num%20%3E%2010%3A%0A%20%20%20%20%20%20%20%20print%28%22It%27s%20big%21%22%29%0A%20%20%20%20else%3A%0A%20%20%20%20%20%20%20%20print%28%22It%27s%20small%22%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Let's use the if statement to write a program to greet your friend. You might
want to look at earlier programs for clues 

<iframe width="100%" height="392.40000000000003" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=%23%20Make%20a%20list%20of%20your%20friends%2C%20by%20adding%20%0A%23%20on%20to%20this%20starter%20list%0A%0Afriends%20%3D%20%5B%20%27friend1%27%2C%27friend2%27%5D%0A%0A%23%20Ask%20the%20user%27s%20name%0Aname%20%3D%20...%0A%0A%23%20Write%20a%20loop%20that%20iterates%20over%20all%20of%20your%20%0A%23%20friends%2C%20and%20if%20the%20user%27s%20name%20is%20the%20same%20%0A%23%20as%20a%20friends%20name%2C%20print%20%22Hello%20Friend%22%0A%0Afor%20friend%20in%20...%20%3A%0A%20%20%20%20..." frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

