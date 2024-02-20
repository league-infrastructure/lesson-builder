---
title: First Look at Lists

---


# First Look at Lists


Like we said before, a list is a lot like a list that you already know about, like a grocery list:

```
Things To Buy
  - apples
  - oranges
  - bread 
  - milk
```

But in Python we would write it like this: 

```python 
things_to_buy = [ 'apples','oranges','bread','milk']
```

The brackets, `[` and `]` are most often used to mean that something is a list. 

There are a lot of neat things we can do with a list.

First, you can get a specific item from a list, using the `[]` with a number inside. 

```python
things_to_buy[1]
> oranges
```

Getting values out of a list like this is called "indexing".


Like most programming languages, the first item in a list is 0, not 1, so if
you wanted to get `apples` from the list, you would write `things_to_get[0]`

Another important thing about lists is you can _iterate_ them, which means 'do
something repeatedly'. Here is how we would print out all of the items in the
list: 


<iframe width="100%" height="174.0" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=things_to_buy%20%3D%20%5B%20%27apples%27%2C%27oranges%27%2C%27bread%27%2C%27milk%27%5D%0A%0Afor%20item%20in%20things_to_buy%3A%0A%20%20%20%20print%28item%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Loops and lists could be very useful for our turtle programs. For instance, we could make a square with 
a different color on each side: 

<iframe width="100%" height="325.20000000000005" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0A%0Aforward%20%3D%2050%0Aleft%20%3D%2090%0Acolors%20%3D%20%5B%20%27red%27%2C%20%27blue%27%2C%20%27black%27%2C%20%27orange%27%5D%0A%0Afor%20color%20in%20colors%3A%0A%20%20%20%20tina.color%28color%29%0A%20%20%20%20tina.forward%28forward%29%0A%20%20%20%20tina.left%28left%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>

Or, we could change the angle that tina turns: 

<iframe width="100%" height="274.8" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0A%0Aforward%20%3D%2050%0A%0Afor%20left%20in%20%5B%2045%2C%2060%2C%2090%2C%2045%2C%20-90%2C%2060%2C%2022%20%2C%20-45%2C%2090%5D%3A%0A%20%20%20%20tina.forward%28forward%29%0A%20%20%20%20tina.left%28left%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>


Here is a way that we could change two variables at once, using array indexes:


<iframe width="100%" height="375.6" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29%0A%0Aforward%20%3D%2050%0Alefts%20%3D%20%5B%2045%2C%20-60%2C%2090%2C%2045%2C%20-90%2C%2060%2C%2022%20%2C%20-45%20%5D%0Acolors%20%3D%20%5B%20%27red%27%2C%20%27blue%27%2C%20%27black%27%2C%20%27orange%27%2C%20%27red%27%2C%20%27blue%27%2C%20%27black%27%2C%20%27orange%27%5D%0A%0Afor%20%20i%20in%20range%288%29%3A%0A%20%20%20%20left%20%3D%20lefts%5Bi%5D%0A%20%20%20%20color%20%3D%20colors%5Bi%5D%0A%0A%20%20%20%20tina.color%28color%29%0A%20%20%20%20tina.forward%28forward%29%0A%20%20%20%20tina.left%28left%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>


Now, write your own crazy program. You can copy and change the programs we've done previously.

<iframe width="100%" height="600" src="https://trinket.io/tools/1.0/jekyll/embed/python#code=import%20turtle%0Atina%20%3D%20turtle.Turtle%28%29%0Atina.shape%28%22turtle%22%29" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>


