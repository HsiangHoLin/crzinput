# CrzInput: Spelling Correction with Gesture

### Introduction
<em>crzinput</em> is an experimental English typing software on IOS. It can correct the user's input somewhat like [Fleksy](https://www.fleksy.com) does. The algorithm inside the project is simple and still distant from production. 

### The Algorithm
The algorithm inside crzinput is very simple. In sum, it takes the vector formed by user input on keyboard layout and compare it with the vectors in the predefined dictionary. Then the algorithms tries to find the dictionary word that is clostest to the input vector. To be more specific, the two vectors are normalized, and then we calculate the product of the two vectors. The closer their product is to 1, the more similar the twoe vectors are.

For example, after user typed "dog" on the keyboard, there will be two 2-D vectors, one is d->o and the other is o->g. The d->o vector, V1 is represented by (Xv1, Yv1) and the o->g vector, V2, is represented by (Xv2, Yv2). Thus, combining the two vectors into one, (Xv1, Yv1, Xv2, Yv2), we can represents the user input in only one vector. This solution is low complexity and practical. And the effect is similar to [Flesky][fl].

### Limitations
The algorithm compares the input word only with dictionary words with same length, that is, it cannot do something like word completing. Apple, however, features both word completing and correction.

Moreover, calculating normalized product means the algorithm won't take vectors' lengths into consideration, which I think would be helpful in enhancing accuracy.

The other critical problem is when the user input is a zero vector, the algorithm doesn't work because computing product with zero vector will always get zero.

### My Enhancement
To take both vector length and relative angle into consideration, I propose an algorithm to compute the distance between the vectors, that is |V1-V2|. The closer the distance, the more similar two vectors are.

I also implemented in a python script to compare the result of both algorithms. 

Moreover, considering that most of the time users only miss some characters of the whole typing, my proposed algorithm also take the matched character counts into consideration. The more charactors the user input and the dictionary word match, the more likely users mean the dictionary word.

[See my blogspot][my]
[cr]:https://github.com/HsiangHoLin/crzinput
[fl]:http://fleksy.com/
[my]:http://hsiangholin.github.io/blog/crzinput.html


Dictionary
===
The dictionary used is from [words](http://en.wikipedia.org/wiki/Words_(Unix\)). Scripts under ./dictgen in the project can generate the dictionary(resource) files for <em>crzinput</em>. 

You may:

1. Run BASH script <em>'gendict'</em> to generate <em>len(1..24).dict</em> files;

2. Edit <em>keycord.dat</em> according to the layout of your keyboard UI, each line as a space-seperated tuple (char, x, y);

3. Run <em>gendb.py</em> by [python 2.7](http://www.python.org)

4. Copy <em>veclen(1..24).dict</em> to xcode project resource folder and add them into the IOS project's copy-to-bundle list. 

Algorithm
===
As simple as junior school math. Take user input 'w', 'o', 'r', 'k' for example. When user touch the keyboard panel for the 4 letters, we have 4 touched 2D-coordinations, which lead to 3 2D-vectors: Vwo, Vor, Vrk. Listing the xs and ys we get a 6-dimension-vector:

> V = [Xvwo, Yvwo, Xvor, Yvor, Xvrk, Yvrk]; 

And using coordination data in keycord.dat we can calculate a standard vector of typing 'work':

> Vstandard = [x1, y1, x2, y2, x3, y3];

Then <em>cosine(V, Vstandard)</em> and <em>abs(|V| - |Vstandard|)</em> are used for evaluation of likelyness between the two typing gestures. The rest is to pick the most-likely word for the typing gesture. 

TODOs
===

1. Make the dictionary thinner, to increase accuracy(exclude unusual words), and to reduce searching/matching time;

2. Index the dictionary to speedup matching process;

3. UX and UI optimization;

4. Various languages support.

