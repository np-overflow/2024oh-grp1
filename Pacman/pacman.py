#Pacman in Python with PyGame
#https://github.com/hbokmann/Pacman
  
import pygame #._view
import random
import copy
import time

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow   = ( 255, 255,   0)
colours = [blue,green,purple,yellow]
rand_color = random.randint(0,len(colours))

Trollicon=pygame.image.load('Pacman\\images\\Overflow.png')
pygame.display.set_icon(Trollicon)

#Add music =================================== Future can add our own music =========================================
pygame.mixer.init()
pygame.mixer.music.load('Pacman/pacman.mp3')
pygame.mixer.music.play(-1, 0.0)

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain()
     
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],colours[rand_color-1])
        wall_list.add(wall)
        all_sprites_list.add(wall)
         
    # return our new list
    return wall_list

def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,white))
      all_sprites_list.add(gate)
      return gate

# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
  
    # Set speed vector
    change_x=0
    change_y=0
  
    # Constructor function
    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Find a new position for the player
    def update(self,walls,gate):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y

#Inheritime Player klassist
class Ghost(Player):
    # Change the speed of the ghost
    def changespeed(self,list,ghost,turn,steps,l):
      try:
        z=list[turn][2]
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1
        else:
          if turn < l:
            turn+=1
          elif ghost == "clyde":
            turn = 2
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]

Pinky_directions = [
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

Blinky_directions = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

Inky_directions = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

Clyde_directions = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

# pl = len(Pinky_directions)-1
# bl = len(Blinky_directions)-1
# il = len(Inky_directions)-1
# cl = len(Clyde_directions)-1


# ============================!!!!!!!!!!!! NEW LINE FROM GHOST SPEED ====================================

all_directions = [Pinky_directions, Blinky_directions, Inky_directions, Clyde_directions]
#Generates random pause amount and pause duration for ghost
def speedAlgorithm(pintlow,pintup,dintlow,dintup, directions_copy):
    for direction_set in directions_copy:
        pause_amount = random.randint(pintlow,pintup)
        while pause_amount > 0:
            pause_duration = random.randint(dintlow,dintup)
            set_length = len(direction_set) -1
            set_index = random.randint(2,set_length)
            direction_set.insert(set_index, [0,0,pause_duration])
            pause_amount -= 1

def difficultySelect(screen):
  font = pygame.font.Font(None, 36)
  title_font = pygame.font.Font(None,42)
  selected_option = 0
  difficulty_options = ["Easy", "Medium", "Hard"]
  return_value = 3
  active = True
  while active: 
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(difficulty_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Easy, Medium, Hard
                        return_value = 0
                    elif selected_option == 1: 
                        return_value = 1
                    elif selected_option == 2:
                        return_value = 2
                    active = False
      
      diff_background = pygame.image.load('Pacman/images/scoreboard.png')
      screen.blit(diff_background, (-30,0))
      draw_text("Select Difficulty", title_font, white, 180, 75)
      for idx, option in enumerate(difficulty_options):
            if idx == selected_option:
                draw_text("> " + option + " <", font, white, 240, 195 + idx * 50)
                
            else:
                draw_text(option, font, white, 240, 195 + idx * 50)
      pygame.display.flip()
  return return_value                 

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

# ============================!!!!!!!!!!!! NEW LINE FROM GHOST SPEED ====================================


# Call this function so the Pygame library can initialize itself
pygame.init()
  
# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'


# Set the title of the window
pygame.display.set_caption('Pacman')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()
  
# Fill the screen with a black background
background.fill(black)



clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)
font_small = pygame.font.Font("freesansbold.ttf", 20)

#default locations for Pacman and monstas
w = 303-16 #Width
p_h = (7*60)+19 #Pacman height
m_h = (4*60)+19 #Monster height
b_h = (3*60)+19 #Binky height
i_w = 303-16-32 #Inky width
c_w = 303+(32-16) #Clyde width

def startSingleplayerGame():

  username = nameEntry(screen)
  return_value = difficultySelect(screen)
  #Adds pauses if difficulty is easy or medium
  if return_value == 0:
    directions = copy.deepcopy(all_directions)
    speedAlgorithm(13,15,2,5, directions)
    
  elif return_value == 1:
    directions = copy.deepcopy(all_directions)
    speedAlgorithm(6,9,1,3, directions)

  elif return_value == 2:
    directions = copy.deepcopy(all_directions)
     
  Pinky_directions = directions[0]
  Blinky_directions = directions[1]
  Inky_directions = directions[2]
  Clyde_directions = directions[3]
  pl = len(Pinky_directions)-1
  bl = len(Blinky_directions)-1
  il = len(Inky_directions)-1
  cl = len(Clyde_directions)-1

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  monsta_list = pygame.sprite.RenderPlain()

  pacman_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)


  p_turn = 0
  p_steps = 0

  b_turn = 0
  b_steps = 0

  i_turn = 0
  i_steps = 0

  c_turn = 0
  c_steps = 0


  # Create the player paddle object
  Pacman = Player( w, p_h, "Pacman/images/Overflow.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  Blinky=Ghost( w, b_h, "Pacman/images/AmongUsGreen.png" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky=Ghost( w, m_h, "Pacman/images/AmongUsRed.png" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky=Ghost( i_w, m_h, "Pacman/images/AmongUsYellow.png" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde=Ghost( c_w, m_h, "Pacman/images/AmongUsOrange.png" )
  monsta_list.add(Clyde)
  all_sprites_list.add(Clyde)

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  score = 0

  done = False

  i = 0

  start = time.time()

  while done == False:
      cur_time = time.time()
      stopwatch_time = cur_time - start
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)
          
      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
   
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      Pacman.update(wall_list,gate)

      returned = Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      p_turn = returned[0]
      p_steps = returned[1]
      Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      Pinky.update(wall_list,False)

      returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      b_turn = returned[0]
      b_steps = returned[1]
      Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      Blinky.update(wall_list,False)

      returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      i_turn = returned[0]
      i_steps = returned[1]
      Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      Inky.update(wall_list,False)

      returned = Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      c_turn = returned[0]
      c_steps = returned[1]
      Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      Clyde.update(wall_list,False)

      # See if the Pacman block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
       
      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
          
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
      bg = pygame.image.load('Pacman/images/map_bg.png') ######## uncomment for map background ##########
      screen.blit(bg, (200, 200)) ######## uncomment for map background ##########
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)
    
      

      text=font.render("Score: "+str(score)+"/"+str(bll), True, red)
      screen.blit(text, [10, 10])

      game_time =font.render(f"Time: {stopwatch_time:.4f}", True, red)
      screen.blit(game_time, [430, 10])

      if score == bll:
        if return_value == 0:
            with open ('scoresEas.csv', 'a') as file:
                file.write(f"{username} , {stopwatch_time:.4f}\n")
        elif return_value == 1:
            with open ('scoresMed.csv', 'a') as file:
                file.write(f"{username} , {stopwatch_time:.4f}\n")
        else:
            with open ('scoresHar.csv', 'a') as file:
                file.write(f"{username} , {stopwatch_time:.4f}\n")
        doNextSingleplayer("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

      if monsta_hit_list:
        doNextSingleplayer("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      clock.tick(10)

def startMultiplayerGame():

  username = nameEntry(screen)
  return_value = difficultySelect(screen)
  #Adds pauses if difficulty is easy or medium
  if return_value == 0:
    directions = copy.deepcopy(all_directions)
    speedAlgorithm(13,15,2,5, directions)
    
  elif return_value == 1:
    directions = copy.deepcopy(all_directions)
    speedAlgorithm(6,9,1,3, directions)

  elif return_value == 2:
    directions = copy.deepcopy(all_directions)
     
  Pinky_directions = directions[0]
  Blinky_directions = directions[1]
  Inky_directions = directions[2]
  Clyde_directions = directions[3]
  pl = len(Pinky_directions)-1
  bl = len(Blinky_directions)-1
  il = len(Inky_directions)-1
  cl = len(Clyde_directions)-1
  
  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  monsta_list = pygame.sprite.RenderPlain()

  pacman_collide = pygame.sprite.RenderPlain()

  pacman2_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)


  p_turn = 0
  p_steps = 0

  b_turn = 0
  b_steps = 0

  i_turn = 0
  i_steps = 0

  c_turn = 0
  c_steps = 0


  # Create the player paddle object
  Pacman = Player( w, p_h, "Pacman/images/Overflow.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  Pacman2 = Player( w, p_h, "Pacman/images/Overflow2.png" )
  all_sprites_list.add(Pacman2)
  pacman2_collide.add(Pacman2)
   
  Blinky=Ghost( w, b_h, "Pacman/images/AmongUsGreen.png" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky=Ghost( w, m_h, "Pacman/images/AmongUsRed.png" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky=Ghost( i_w, m_h, "Pacman/images/AmongUsYellow.png" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde=Ghost( c_w, m_h, "Pacman/images/AmongUsOrange.png" )
  monsta_list.add(Clyde)
  all_sprites_list.add(Clyde)

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            p2_collide = pygame.sprite.spritecollide(block, pacman2_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  score = 0
  pacman1_score = 0
  pacman2_score = 0

  done = False

  i = 0

  start = time.time()

  while done == False:
      cur_time = time.time()
      stopwatch_time = cur_time - start
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,30)
              if event.key == 97:
                  print(event.key)
                  Pacman2.changespeed(-30,0)
              if event.key == 100:
                  print(event.key)
                  Pacman2.changespeed(30,0)
              if event.key == 119:
                  Pacman2.changespeed(0,-30)
              if event.key == 115:
                  Pacman2.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)
              if event.key == 97:
                  Pacman2.changespeed(30,0)
              if event.key == 100:
                  Pacman2.changespeed(-30,0)
              if event.key == 119:
                  Pacman2.changespeed(0,30)
              if event.key == 115:
                  Pacman2.changespeed(0,-30)
          
      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
   
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      Pacman.update(wall_list,gate)
      Pacman2.update(wall_list,gate)

      returned = Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      p_turn = returned[0]
      p_steps = returned[1]
      Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      Pinky.update(wall_list,False)

      returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      b_turn = returned[0]
      b_steps = returned[1]
      Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      Blinky.update(wall_list,False)

      returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      i_turn = returned[0]
      i_steps = returned[1]
      Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      Inky.update(wall_list,False)

      returned = Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      c_turn = returned[0]
      c_steps = returned[1]
      Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      Clyde.update(wall_list,False)

      # See if the Pacman block has collided with anything.
      pacman1_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
      pacman2_hit_list = pygame.sprite.spritecollide(Pacman2, block_list, True)

      # See if the Pacman2 block has collided with anything.
      blocks_hit_list = pacman1_hit_list + pacman2_hit_list


      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      if len(pacman1_hit_list) > 0:
          pacman1_score +=len(pacman1_hit_list)
      if len(pacman2_hit_list) > 0:
          pacman2_score +=len(pacman2_hit_list)
      
          
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
      bg = pygame.image.load('Pacman/images/map_bg.png') ######## uncomment for map background ##########
      screen.blit(bg, (200, 200)) ######## uncomment for map background ##########
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)
    
      

      text=font_small.render("Score: "+str(score)+"/"+str(bll), True, red)
      screen.blit(text, [300, 10])
      text1=font_small.render("Light: "+str(pacman1_score)+"/"+str(bll), True, red)
      screen.blit(text1, [10, 10])
      text2=font_small.render("Dark: "+str(pacman2_score)+"/"+str(bll), True, red)
      screen.blit(text2, [160, 10])

      game_time =font_small.render(f"Time: {stopwatch_time:.4f}", True, red)
      screen.blit(game_time, [460, 10])

      if score == bll:
        if return_value == 0:
            with open ('scoresMultiplayerEas.csv', 'a') as file:
                file.write(f"{username} , {stopwatch_time:.4f}\n")
        elif return_value == 1:
            with open ('scoresMultiplayerMed.csv', 'a') as file:
                file.write(f"{username} , {stopwatch_time:.4f}\n")
        else:
            with open ('scoresMultiplayerHar.csv', 'a') as file:
                file.write(f"{username} , {stopwatch_time:.4f}\n")
        doNextMultiplayer("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)



      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)
      
      monsta_hit_list2 = pygame.sprite.spritecollide(Pacman2, monsta_list, False)

      if monsta_hit_list or monsta_hit_list2:
        # with open ('scoresMultiplayer.csv', 'a') as file:
        #     file.write(username + " , " + str(score) +'\n')
        doNextMultiplayer("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      clock.tick(10)

def doNextSingleplayer(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            mainMenu(screen)
            
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            startSingleplayerGame()

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)


def doNextMultiplayer(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            mainMenu(screen)
            
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            startMultiplayerGame()

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

def nameEntry(screen):
    input_font = pygame.font.Font(None, 36)
    name = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    input_active = False  # Player entered name, exit loop
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # Remove last character on backspace
                else:
                    name += event.unicode  # Add typed character to name

        #screen.fill(black)
        name_background = pygame.image.load('Pacman/images/name-entry.png')
        screen.blit(name_background, (-20,0))

        text_surface = input_font.render("Enter your name: " + name, True, white)
        screen.blit(text_surface, (100, 200))

        pygame.display.flip()

    return name

def scoreBoard():
    return_value = difficultySelect(screen)
    #screen.fill(black)
    score_background = pygame.image.load('Pacman/images/scoreboard.png')
    screen.blit(score_background, (-20,0))
    scoreboard_font = pygame.font.Font(None, 36)

    #Adds pauses if difficulty is easy or medium
    if return_value == 0:
        try:
            with open('scoresEas.csv', 'r') as file:
                lines = file.readlines()
            lines.sort(key=lambda x: float(x.split(',')[1]))  # Sort scores by the second column (score)
            

            title = scoreboard_font.render("Scoreboard", True, white)
            title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(title, title_rect)

            max_width = 0
            score_entries = []

            alpha_label = scoreboard_font.render("Alpha Lion King Dragon Winner", True, yellow)
            alpha_rect = alpha_label.get_rect(center=(screen.get_width() // 2, 80))
            screen.blit(alpha_label, alpha_rect)

            first_entry = lines[0]  # First entry will be displayed above "The Rest"
            first_data = first_entry.strip().split(',')
            first_name = first_data[0]
            first_score = float(first_data[1])

            # Display first entry above "The Rest"
            first_text = f"1. {first_name}: {first_score}"
            first_surface = scoreboard_font.render(first_text, True, yellow)
            first_rect = first_surface.get_rect(center=(screen.get_width() // 2, 120))
            screen.blit(first_surface, first_rect)
            max_width = max(max_width, first_surface.get_width())

            rest_entries = lines[1:5]  # Rest of the entries to be displayed under "The Rest"

            # Render "The Rest" below the first-place entry
            rest_text = scoreboard_font.render("The Rest", True, white)
            rest_rect = rest_text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(rest_text, rest_rect)

            starting_y = 250
            padding = 60  # Increased padding between entries
            for i, line in enumerate(rest_entries):  # Display rest of the scores
                score_data = line.strip().split(',')
                name = score_data[0]
                score = float(score_data[1])

                score_text = f"{i + 2}. {name}: {score}"  # Start numbering from 2 for the rest
                score_surface = scoreboard_font.render(score_text, True, white)
                score_entries.append(score_surface)
                max_width = max(max_width, score_surface.get_width())

            max_width += 20  # Adding additional padding to the maximum width

            starting_y = 250
            for i, entry in enumerate(score_entries):  # Render rest of the entries with adjusted alignment
                entry_rect = entry.get_rect(center=(screen.get_width() // 2, starting_y))
                entry_rect.centerx = screen.get_width() // 2  # Set the center of the rect horizontally
                screen.blit(entry, entry_rect)
                starting_y += padding  # Increase the Y-coordinate spacing between entries


        except :
            error_message = scoreboard_font.render("No scores yet!", True, white)
            error_rect = error_message.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(error_message, error_rect)


        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainMenu(screen)
    
    elif return_value == 1:
        try:
            with open('scoresMed.csv', 'r') as file:
                lines = file.readlines()
            lines.sort(key=lambda x: float(x.split(',')[1]))  # Sort scores by the second column (score)
            

            title = scoreboard_font.render("Scoreboard", True, white)
            title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(title, title_rect)

            max_width = 0
            score_entries = []

            alpha_label = scoreboard_font.render("Alpha Lion King Dragon Winner", True, yellow)
            alpha_rect = alpha_label.get_rect(center=(screen.get_width() // 2, 80))
            screen.blit(alpha_label, alpha_rect)

            first_entry = lines[0]  # First entry will be displayed above "The Rest"
            first_data = first_entry.strip().split(',')
            first_name = first_data[0]
            first_score = float(first_data[1])

            # Display first entry above "The Rest"
            first_text = f"1. {first_name}: {first_score}"
            first_surface = scoreboard_font.render(first_text, True, yellow)
            first_rect = first_surface.get_rect(center=(screen.get_width() // 2, 120))
            screen.blit(first_surface, first_rect)
            max_width = max(max_width, first_surface.get_width())

            rest_entries = lines[1:5]  # Rest of the entries to be displayed under "The Rest"

            # Render "The Rest" below the first-place entry
            rest_text = scoreboard_font.render("The Rest", True, white)
            rest_rect = rest_text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(rest_text, rest_rect)

            starting_y = 250
            padding = 60  # Increased padding between entries
            for i, line in enumerate(rest_entries):  # Display rest of the scores
                score_data = line.strip().split(',')
                name = score_data[0]
                score = float(score_data[1])

                score_text = f"{i + 2}. {name}: {score}"  # Start numbering from 2 for the rest
                score_surface = scoreboard_font.render(score_text, True, white)
                score_entries.append(score_surface)
                max_width = max(max_width, score_surface.get_width())

            max_width += 20  # Adding additional padding to the maximum width

            starting_y = 250
            for i, entry in enumerate(score_entries):  # Render rest of the entries with adjusted alignment
                entry_rect = entry.get_rect(center=(screen.get_width() // 2, starting_y))
                entry_rect.centerx = screen.get_width() // 2  # Set the center of the rect horizontally
                screen.blit(entry, entry_rect)
                starting_y += padding  # Increase the Y-coordinate spacing between entries


        except :
            error_message = scoreboard_font.render("No scores yet!", True, white)
            error_rect = error_message.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(error_message, error_rect)


        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainMenu(screen)

    elif return_value == 2:
        try:
            with open('scoresHar.csv', 'r') as file:
                lines = file.readlines()
            lines.sort(key=lambda x: float(x.split(',')[1]))  # Sort scores by the second column (score)
            

            title = scoreboard_font.render("Scoreboard", True, white)
            title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(title, title_rect)

            max_width = 0
            score_entries = []

            alpha_label = scoreboard_font.render("Alpha Lion King Dragon Winner", True, yellow)
            alpha_rect = alpha_label.get_rect(center=(screen.get_width() // 2, 80))
            screen.blit(alpha_label, alpha_rect)

            first_entry = lines[0]  # First entry will be displayed above "The Rest"
            first_data = first_entry.strip().split(',')
            first_name = first_data[0]
            first_score = float(first_data[1])

            # Display first entry above "The Rest"
            first_text = f"1. {first_name}: {first_score}"
            first_surface = scoreboard_font.render(first_text, True, yellow)
            first_rect = first_surface.get_rect(center=(screen.get_width() // 2, 120))
            screen.blit(first_surface, first_rect)
            max_width = max(max_width, first_surface.get_width())

            rest_entries = lines[1:5]  # Rest of the entries to be displayed under "The Rest"

            # Render "The Rest" below the first-place entry
            rest_text = scoreboard_font.render("The Rest", True, white)
            rest_rect = rest_text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(rest_text, rest_rect)

            starting_y = 250
            padding = 60  # Increased padding between entries
            for i, line in enumerate(rest_entries):  # Display rest of the scores
                score_data = line.strip().split(',')
                name = score_data[0]
                score = float(score_data[1])

                score_text = f"{i + 2}. {name}: {score}"  # Start numbering from 2 for the rest
                score_surface = scoreboard_font.render(score_text, True, white)
                score_entries.append(score_surface)
                max_width = max(max_width, score_surface.get_width())

            max_width += 20  # Adding additional padding to the maximum width

            starting_y = 250
            for i, entry in enumerate(score_entries):  # Render rest of the entries with adjusted alignment
                entry_rect = entry.get_rect(center=(screen.get_width() // 2, starting_y))
                entry_rect.centerx = screen.get_width() // 2  # Set the center of the rect horizontally
                screen.blit(entry, entry_rect)
                starting_y += padding  # Increase the Y-coordinate spacing between entries


        except :
            error_message = scoreboard_font.render("No scores yet!", True, white)
            error_rect = error_message.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(error_message, error_rect)


        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainMenu(screen)


def multiplayerScoreBoard():
    return_value = difficultySelect(screen)
    #screen.fill(black)
    score_background = pygame.image.load('Pacman/images/scoreboard.png')
    screen.blit(score_background, (-20,0))
    scoreboard_font = pygame.font.Font(None, 36)

    #Adds pauses if difficulty is easy or medium
    if return_value == 0:
        try:
            with open('scoresMultiplayerEas.csv', 'r') as file:
                lines = file.readlines()
            lines.sort(key=lambda x: float(x.split(',')[1]))  # Sort scores by the second column (score)
            

            title = scoreboard_font.render("Scoreboard", True, white)
            title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(title, title_rect)

            max_width = 0
            score_entries = []

            alpha_label = scoreboard_font.render("Alpha Lion King Dragon Winner", True, yellow)
            alpha_rect = alpha_label.get_rect(center=(screen.get_width() // 2, 80))
            screen.blit(alpha_label, alpha_rect)

            first_entry = lines[0]  # First entry will be displayed above "The Rest"
            first_data = first_entry.strip().split(',')
            first_name = first_data[0]
            first_score = float(first_data[1])

            # Display first entry above "The Rest"
            first_text = f"1. {first_name}: {first_score}"
            first_surface = scoreboard_font.render(first_text, True, yellow)
            first_rect = first_surface.get_rect(center=(screen.get_width() // 2, 120))
            screen.blit(first_surface, first_rect)
            max_width = max(max_width, first_surface.get_width())

            rest_entries = lines[1:5]  # Rest of the entries to be displayed under "The Rest"

            # Render "The Rest" below the first-place entry
            rest_text = scoreboard_font.render("The Rest", True, white)
            rest_rect = rest_text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(rest_text, rest_rect)

            starting_y = 250
            padding = 60  # Increased padding between entries
            for i, line in enumerate(rest_entries):  # Display rest of the scores
                score_data = line.strip().split(',')
                name = score_data[0]
                score = float(score_data[1])

                score_text = f"{i + 2}. {name}: {score}"  # Start numbering from 2 for the rest
                score_surface = scoreboard_font.render(score_text, True, white)
                score_entries.append(score_surface)
                max_width = max(max_width, score_surface.get_width())

            max_width += 20  # Adding additional padding to the maximum width

            starting_y = 250
            for i, entry in enumerate(score_entries):  # Render rest of the entries with adjusted alignment
                entry_rect = entry.get_rect(center=(screen.get_width() // 2, starting_y))
                entry_rect.centerx = screen.get_width() // 2  # Set the center of the rect horizontally
                screen.blit(entry, entry_rect)
                starting_y += padding  # Increase the Y-coordinate spacing between entries


        except :
            error_message = scoreboard_font.render("No scores yet!", True, white)
            error_rect = error_message.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(error_message, error_rect)


        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainMenu(screen)
    
    elif return_value == 1:
        try:
            with open('scoresMultiplayerMed.csv', 'r') as file:
                lines = file.readlines()
            lines.sort(key=lambda x: float(x.split(',')[1]))  # Sort scores by the second column (score)
            

            title = scoreboard_font.render("Scoreboard", True, white)
            title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(title, title_rect)

            max_width = 0
            score_entries = []

            alpha_label = scoreboard_font.render("Alpha Lion King Dragon Winner", True, yellow)
            alpha_rect = alpha_label.get_rect(center=(screen.get_width() // 2, 80))
            screen.blit(alpha_label, alpha_rect)

            first_entry = lines[0]  # First entry will be displayed above "The Rest"
            first_data = first_entry.strip().split(',')
            first_name = first_data[0]
            first_score = float(first_data[1])

            # Display first entry above "The Rest"
            first_text = f"1. {first_name}: {first_score}"
            first_surface = scoreboard_font.render(first_text, True, yellow)
            first_rect = first_surface.get_rect(center=(screen.get_width() // 2, 120))
            screen.blit(first_surface, first_rect)
            max_width = max(max_width, first_surface.get_width())

            rest_entries = lines[1:5]  # Rest of the entries to be displayed under "The Rest"

            # Render "The Rest" below the first-place entry
            rest_text = scoreboard_font.render("The Rest", True, white)
            rest_rect = rest_text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(rest_text, rest_rect)

            starting_y = 250
            padding = 60  # Increased padding between entries
            for i, line in enumerate(rest_entries):  # Display rest of the scores
                score_data = line.strip().split(',')
                name = score_data[0]
                score = float(score_data[1])

                score_text = f"{i + 2}. {name}: {score}"  # Start numbering from 2 for the rest
                score_surface = scoreboard_font.render(score_text, True, white)
                score_entries.append(score_surface)
                max_width = max(max_width, score_surface.get_width())

            max_width += 20  # Adding additional padding to the maximum width

            starting_y = 250
            for i, entry in enumerate(score_entries):  # Render rest of the entries with adjusted alignment
                entry_rect = entry.get_rect(center=(screen.get_width() // 2, starting_y))
                entry_rect.centerx = screen.get_width() // 2  # Set the center of the rect horizontally
                screen.blit(entry, entry_rect)
                starting_y += padding  # Increase the Y-coordinate spacing between entries


        except:
            error_message = scoreboard_font.render("No scores yet!", True, white)
            error_rect = error_message.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(error_message, error_rect)


        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainMenu(screen)

    elif return_value == 2:
        try:
            with open('scoresMultiplayerHar.csv', 'r') as file:
                lines = file.readlines()
            lines.sort(key=lambda x: float(x.split(',')[1]))  # Sort scores by the second column (score)
            

            title = scoreboard_font.render("Scoreboard", True, white)
            title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(title, title_rect)

            max_width = 0
            score_entries = []

            alpha_label = scoreboard_font.render("Alpha Lion King Dragon Winner", True, yellow)
            alpha_rect = alpha_label.get_rect(center=(screen.get_width() // 2, 80))
            screen.blit(alpha_label, alpha_rect)

            first_entry = lines[0]  # First entry will be displayed above "The Rest"
            first_data = first_entry.strip().split(',')
            first_name = first_data[0]
            first_score = float(first_data[1])

            # Display first entry above "The Rest"
            first_text = f"1. {first_name}: {first_score}"
            first_surface = scoreboard_font.render(first_text, True, yellow)
            first_rect = first_surface.get_rect(center=(screen.get_width() // 2, 120))
            screen.blit(first_surface, first_rect)
            max_width = max(max_width, first_surface.get_width())

            rest_entries = lines[1:5]  # Rest of the entries to be displayed under "The Rest"

            # Render "The Rest" below the first-place entry
            rest_text = scoreboard_font.render("The Rest", True, white)
            rest_rect = rest_text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(rest_text, rest_rect)

            starting_y = 250
            padding = 60  # Increased padding between entries
            for i, line in enumerate(rest_entries):  # Display rest of the scores
                score_data = line.strip().split(',')
                name = score_data[0]
                score = float(score_data[1])

                score_text = f"{i + 2}. {name}: {score}"  # Start numbering from 2 for the rest
                score_surface = scoreboard_font.render(score_text, True, white)
                score_entries.append(score_surface)
                max_width = max(max_width, score_surface.get_width())

            max_width += 20  # Adding additional padding to the maximum width

            starting_y = 250
            for i, entry in enumerate(score_entries):  # Render rest of the entries with adjusted alignment
                entry_rect = entry.get_rect(center=(screen.get_width() // 2, starting_y))
                entry_rect.centerx = screen.get_width() // 2  # Set the center of the rect horizontally
                screen.blit(entry, entry_rect)
                starting_y += padding  # Increase the Y-coordinate spacing between entries


        except :
            error_message = scoreboard_font.render("No scores yet!", True, white)
            error_rect = error_message.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(error_message, error_rect)


        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainMenu(screen)


def mainMenu(screen):
    menu_font = pygame.font.Font(None, 36)
    selected_option = 0
    menu_options = ["Start Singleplayer Game", "Start Multiplayer Game", "Singleplayer Scoreboard", "Multiplayer Scoreboard", "Quit"]
    username = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Start Game selected
                        startSingleplayerGame()
                    elif selected_option == 1:  # Quit selected
                        startMultiplayerGame()
                    elif selected_option == 2:  # Quit selected
                        scoreBoard()
                    elif selected_option == 3:  # Quit selected
                        multiplayerScoreBoard()
                    elif selected_option == 4:
                        quit()
                    
                        

        #screen.fill(black)
        welc_background = pygame.image.load('Pacman/images/welcome.png')
        screen.blit(welc_background, (-30,0))

        for idx, option in enumerate(menu_options):
            if idx == selected_option:
                text_surface = menu_font.render("> " + option + " <", True, white)
            else:
                text_surface = menu_font.render(option, True, white)
            screen.blit(text_surface, (150, 350 + idx * 50))

        pygame.display.flip()

def initScreen():
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Main Menu')
    return screen

def main():
    username = mainMenu(screen)
    if username:
        print("Username entered:", username)
        startSingleplayerGame()

    pygame.quit()

if __name__ == "__main__":
    main()
