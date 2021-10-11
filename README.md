# LFSR-RNG
A Linear Feed Shift Register Random Number Generator written in python. Was written after watching a very interesting [video](https://www.youtube.com/watch?v=Ks1pw1X22y4&t=162s&ab_channel=Computerphile) by Computerphile. In theory a usable random number generator but due to lack of speed and optimisations, you're probably better off using the built in `random` library :smile:.

```python
from lfsrrng import Generator

rng = Generator(seed=345667)
number = rng.range(0, 10)                         # generate a number between 0 and 10 (10 not included)
letter = rng.choice('abcdefghijklmnopqrstuvwxyz') # get a random element from an iterable
```


