from PIL import Image, ImageFont, ImageDraw
from PIL.ImageOps import invert
import random
import numpy as np

def generate_grid_with_letters(letters , cell_size=100):
  n = len(letters)
  img_size = n * cell_size
  img = Image.new('L', (img_size, img_size), color='white')
  draw = ImageDraw.Draw(img)
  
  font = ImageFont.truetype("arial.ttf", 65)
  
  for row in range(n):
    for col in range(n):
      top_left = (col * cell_size, row * cell_size)
      bottom_right = ((col + 1) * cell_size, (row + 1) * cell_size)
      draw.rectangle([top_left, bottom_right], outline="black", width=2)

      textbbox = draw.textbbox(xy=(0,0),text=letters[row][col], font=font)
      text_width = textbbox[2] - textbbox[0]
      text_height = textbbox[3] - textbbox[1]
      text_position = (col * cell_size + (cell_size - text_width) // 2, row * cell_size + (cell_size - text_height) // 2 - 10)
      draw.text(text_position, letters[row][col], fill="black", font=font)

  return img

def get_random_letter_grid(n, letters, unique_letters):
  grid = [[random.choice(letters) for _ in range(n)] for _ in range(n)]
  
  all_positions = [(i, j) for i in range(n) for j in range(n)]
  unique_positions = random.sample(all_positions, len(unique_letters))
  
  for i,position in enumerate(unique_positions):
    grid[position[0]][position[1]] = unique_letters[i]
  return grid

def get_letter_images_from_grid(img, n, cell_size=100) -> list[Image.Image]:  
  letter_images = []
  
  for row in range(n):
    for col in range(n):
      left = col * cell_size + 2
      upper = row * cell_size + 2
      right = (col + 1) * cell_size - 2
      lower = (row + 1) * cell_size - 2
      
      letter_img = img.crop((left, upper, right, lower))
      
      letter_images.append(letter_img)
          
  return letter_images

def grid_to_letters(grid, n, model):
  img_dimension = 28
  
  alphabet_mapping = {i: chr(64 + i +1) for i in range(0,26)}
  img = Image.open(grid)
  letters_images = get_letter_images_from_grid(img=img, n=n)

  # letter image to list
  for i,letter in enumerate(letters_images):
    letter.thumbnail((img_dimension,img_dimension))
    letter = invert(letter)
    letter = np.asarray(letter, dtype="int32")/255
    letter = letter.reshape((1,img_dimension,img_dimension,1))
    letters_images[i] = letter
  
  letters_images = np.asarray(letters_images)
  letters_images = letters_images.reshape((n,n,1,img_dimension,img_dimension,1))

  letters = np.empty((n,n), dtype='str')
  for i in range(n):
    for j in range(n):
      letter_prediction = model.predict(letters_images[i][j])
      max = np.argmax(letter_prediction)
      letter = alphabet_mapping.get(max)
      letters[i][j] = letter
  
  return letters



  
