# KBAI-Ravens-Project

This is the project I used in Georgia Tech's Knowledge-Based AI Masters class.
The goal was to design an algorithm to solve visual intelligence tests - specifically [Raven's Progressive Matrices](https://en.wikipedia.org/wiki/Raven%27s_Progressive_Matrices).

For reference, here is an example problem:

![Example Raven's Progressive Matrices Problem](https://github.com/SealedSaint/KBAI-Ravens-Project/blob/master/RPM-Example.jpg)


### Methods

While a common approach to these problems is to utilize a [semantic network](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&cad=rja&uact=8&ved=0ahUKEwjUgd3D9M_SAhVS9GMKHW_tBccQFggiMAI&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSemantic_network&usg=AFQjCNH_3p3h-umSPq7G_ZiUc_6LYE_B3Q&sig2=FxHUc8aMC_pFGn-PFunyTw&bvm=bv.149397726,d.cGc)
to identify objects in your image and draw relationships between them, I chose to take a computer-vision approach.

I did my best to minimize assumptions about the image, and I tried to make my algoritm as flexible as possible.
By processing the image and analyzing pixel values only, I was able to draw relationships among the various matrix sectors.
Using these relationships, my algorithm constructs what it deems the "ideal" solution and then compares this "ideal" solution
to the available answers.
