# Conway's Game of Life
The zero player Darwinism simulation game as described by Conway (demonstrates Turing Completeness).


I created this script after having made attempts to do the same project in the past, but being limited by the horizons of my knowledge.
I've tried again recently and the algorithms I chose to use in this one were much faster. My old project often ran out of memory or spent ~20 seconds
in between each generation, this project gets through a couple hundred at least in the same amount of time, but I digress.

If you aren't already aware, Conway's Game of Life is a thought experiment turned into a program which simulates natural selection in order to demonstrate the
idea of Turing Completeness. In this "zero player game" as Conway described it, cells are given an initial state, or seed, and then the rules below are applied 
over and over, for an undecidable amount of time in most cases.

The rules are as follows:

  1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
  2. Any live cell with two or three live neighbours lives on to the next generation.
  3. Any live cell with more than three live neighbours dies, as if by overpopulation.
  4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

For further information on the game itself (and for generally interesting information told in a digestible format) see this video:
  https://www.youtube.com/watch?v=HeQX2HjkcNo

Keep reading if you care to know the implementation / thought process behind the program's algorithm (it isn't obvious just looking), 
otherwise you can stop here. (Note: this is all pure Python, no Cython)

The most naive approach, and the one I had used to tackle this problem the first time is essentially brute force. In this method, I stored every cell
in a list. When I needed a particular cell in a particular position, I used a method that would search that list, checking each and every Cell's x
and y values until I found the exact one I needed. Not the best time complexity wise, especially when you have to do something that simple so often.
Even worse, when grabbing the neighbors, I simply repeated the same thing 8 times. The benefits of such an approach are limited mostly to simplicity,
and of course, this approach did not work. At extremely small scales, with "non explosive" patterns, the algorithm did appear to work in terms of the
rules, but it certainly did not work with my GPU.

The next approach I tried, some few months later, was to use a dictionary to store cells by location. This is certainly getting there, and is actually 
implemented in my current version, however it does not go far enough. Neighbors were still grabbed manually, methods handling cell positions and graphics
were stil slow and unoptimized, and there was a lot of unnecessary clutter.

In the current approach, I store the grid in the format `dict[tuple[int, int], dict[tuple[int, int], bool]]` such that the outer tuples are the locations of a cell,
the inner dict tuples are locations of that cells neighbors, and the boolean values are the cells dead or alive status. This comes with the benefit of constant
lookup times in all aspects regarding cells, leaving almost all time constraints up to the algorithms themselves. I would love to say there are more major optimizations
but this data structure is actually hyper-efficient compared to my previous iterations of this project, and it's likely doing all the heavy lifting. That isn't to
say there aren't other optimizations, though. There are probably hundreds of micro-optimizations scattered throughout this code compared to the old attempts.

##################################################################################################################################################################

The reason I chose to write so much about this project is due to my lack of having a GitHub account before this. I did not upload the old versions of this project,
nor anything else I have ever written, and my digital organizational skills are poor, so they are lost to the sands of time as far as I'm considered. This readme is to
make up for that lost history, I suppose. In the future I'll only be doing this much if there is really this much to say. I'll also be uploading all my major and
minor projects (anything that is more than a "quick script") on GitHub from here on out. Thanks for reading.
