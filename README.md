# Final-Proyect-Snake

Hello, this is a short explanation of my final python project.

#The Game Concept
The premise is pretty simple. Its a basic snake game (counters, graphics, sound bites,etc). But the apple bounces around randomly and uncontrollably,
adding a layer of difficulty and complexity to the basic game.

#How to run it

The elements are included in the "Final Proyect" File, and should suffice to run the game effectively, however, one important change must be done. That is, changing
the location of the elements to your system. This can be a little complicated for beginners, but I assure you its not a big deal. Simply go where the 
2 different kinds of sprites are allocated inside the code (after downloading the same files in your computer, of course) and change this:

"Apple_img =pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Apple.png").convert_alpha()),(cell_size,cell_size))"

into this:

"Apple_img =pygame.transform.scale((pygame.image.load("Elements/Apple.png").convert_alpha()),(cell_size,cell_size))"

do this for every file that needs it, and you should be able to run the game without any more hitches.

#About classes & features

5 classes were implemented:

MAINFUNCTIONS: To handle game updates, movement, fluidity, spawning of apples, etc. Basically everything regarding the playability of the game.

Snake: Handles sprites, movement, reposition and initial position, growth after consuming apples, and drawing the snake into the window.

Apple: Handles the apple sprite, the apple reroll after being consumed, the 8-directional movement of the apple and drawing the apple into the window.

Background: Handles the view of the window in a checkerboard pattern, green and dark green.

Scoreboard: Handles font and keeps count of the amount of apples eaten 

The features are:

-movement of snake in 4 different axis

-movement of apple in 8 different axis, including a bounce similar to that of a DVD logo.

-reroll of apples after being consumed

-fluid movement through average between predicted vectors and current vectors

-Timer of attempt and location in coords (x,y) of apple reroll
