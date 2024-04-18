import easyocr
from mss import mss
from PIL import Image
import numpy as np
from tabulate import tabulate
import pyautogui
import time 
import re

def find_nearest_color(rgb, image):
    colors = {
        'Brown': image.getpixel((720, 822)),
        'Yellow': image.getpixel((765, 822)),
        'Pink': image.getpixel((809, 822)),
        'Black': image.getpixel((853, 822)),
        'White': image.getpixel((898, 822)),
        'Green': image.getpixel((985, 822)),
        'Blue': image.getpixel((941, 822))
    }
    
    distances = {color: np.linalg.norm(np.array(rgb) - np.array(color_rgb)) for color, color_rgb in colors.items()}
    closest_color = min(distances, key=distances.get)
    return closest_color

def find_nearest_color_result(rgb):
    colors = {
        'Correct': (99, 199, 77),
        'Partially_Correct': (218, 211, 61),
        'Wrong': (254, 174, 52),
        'Bomb':  (228, 59, 68)
    }
    distances = {color: np.linalg.norm(np.array(rgb) - np.array(color_rgb)) for color, color_rgb in colors.items()}
    closest_color = min(distances, key=distances.get)
    return closest_color

def first_get_screenshot():
    with mss() as sct:
        monitor_number = 2
        monitor = sct.monitors[monitor_number]

        screenshot_path = 'screenshot_1.png'
        sct.shot(mon=monitor_number, output=screenshot_path)

    image = Image.open(screenshot_path)
    return image
    
def second_get_screenshot():
    with mss() as sct:
        monitor_number = 2
        monitor = sct.monitors[monitor_number]

        screenshot_path = 'screenshot_2.png'
        sct.shot(mon=monitor_number, output=screenshot_path)

    image = Image.open(screenshot_path)
    return image

def first_cycle(image_1):
    trial_1 = []
    coordinates = [(739, 624), (788, 624), (838, 624), (887, 624)]
    for coord in coordinates:
        rgb = image_1.getpixel(coord)
        color_name = find_nearest_color(rgb, image_1)
        trial_1.append(color_name)
    return trial_1

def first_get_feedback(image_1):
    result_1 = []
    coordinates = [(754, 607), (803, 607), (852, 607), (902, 607)]
    for coord in coordinates:
        rgb = image_1.getpixel(coord)
        color_name = find_nearest_color_result(rgb)
        result_1.append(color_name)
    return result_1
    
def second_cycle(image_1):
    trial_1 = []
    coordinates = [(739, 567), (788, 567), (838, 567), (887, 567)]
    for coord in coordinates:
        rgb = image_1.getpixel(coord)
        color_name = find_nearest_color(rgb, image_1)
        trial_1.append(color_name)
    return trial_1
    
def second_get_feedback(image_1):
    result_1 = []
    coordinates = [(753, 548), (802, 548), (852, 548), (902, 548)]
    for coord in coordinates:
        rgb = image_1.getpixel(coord)
        color_name = find_nearest_color_result(rgb)
        result_1.append(color_name)
    return result_1    

def make_first_move():
    pyautogui.click(x=-1180, y=612)
    pyautogui.click(x=-1190, y=813)
    pyautogui.click(x=-1145, y=814)
    pyautogui.click(x=-1106, y=817)
    pyautogui.click(x=-1062, y=817)
    pyautogui.click(x=-1101, y=668)
    time.sleep(3)

def start_game():
    pyautogui.click(x=-832, y=804)
    time.sleep(3)  
    
def second_trial_strategy(first_trial, first_result):
    # Define all available colors and the colors used in the first trial
    all_colors = {'Brown', 'Yellow', 'Pink', 'Black', 'White', 'Green', 'Blue'}
    used_colors = set(first_trial)
    remaining_colors = list(all_colors - used_colors)  # Convert to list for indexing

    # Initialize the second trial with None values
    second_trial = [None] * 4

    # Process 'Correct' results first
    for i, result in enumerate(first_result):
        if result == 'Correct' and remaining_colors:
            second_trial[i] = remaining_colors[0]
            remaining_colors.pop(0)

    # Process 'Partially_Correct' results
    for i, result in enumerate(first_result):
        if result == 'Partially_Correct' and remaining_colors:
            second_trial[i] = remaining_colors[0]
            remaining_colors.pop(0)

    # Process 'Wrong' and 'Bomb' results
    for i, result in enumerate(first_result):
        if (result == 'Wrong' or result == 'Bomb') and remaining_colors:
            second_trial[i] = remaining_colors[0]
            remaining_colors.pop(0)

    # Fill the last spot with a 'Correct' or 'Partially_Correct' color from the first trial
    # but not the same as it was in the first trial.
    for i, color in enumerate(second_trial):
        if color is None:  # This finds the unfilled spot
            for j, first_color in enumerate(first_trial):
                if first_result[j] in ['Correct', 'Partially_Correct'] and first_color != first_trial[i]:
                    second_trial[i] = first_color
                    break

    if second_trial[3] == None:
        second_trial[3] = second_trial[2]
    return second_trial
    
    
def make_second_move(second_trial):
    pyautogui.click(x=-1178, y=559)
    for color in second_trial:
        if color == 'Brown':
            pyautogui.click(x=-1192, y=816)
        if color == 'Yellow':
            pyautogui.click(x=-1149, y=816)
        if color == 'Pink':
            pyautogui.click(x=-1105, y=816)
        if color == 'Black':
            pyautogui.click(x=-1062, y=816)
        if color == 'White':
            pyautogui.click(x=-1018, y=816)
        if color == 'Blue':
            pyautogui.click(x=-974,  y=816)
        if color == 'Green':
            pyautogui.click(x=-929,  y=816)
    pyautogui.click(x=-1101, y=668)
    time.sleep(3)
    
def third_trial_strategy(first_trial, first_result, second_trial, second_result):
    all_colors = {'Brown', 'Yellow', 'Pink', 'Black', 'White', 'Green', 'Blue'}
    confirmed_correct = [None] * 4
    confirmed_positions = set()
    
    # Initialize the second trial with None values
    third_trial = [None] * 4

    # Loop through the results to check for correct colors
    for i in range(len(first_trial)):
        if first_result[i] == 'Correct':
            third_trial[i] = first_trial[i]
            confirmed_positions.add(i)
        elif second_result[i] == 'Correct':
            third_trial[i] = second_trial[i]
            confirmed_positions.add(i)

    free_places = third_trial.count(None)

    # Check for colors that were 'Partially_Correct' in both trials
    partially_correct_both_trials = {}
    for color in all_colors:
        if color in first_trial and first_result[first_trial.index(color)] == 'Partially_Correct' and \
           color in second_trial and second_result[second_trial.index(color)] == 'Partially_Correct':
            partially_correct_both_trials[color] = True

    for color in partially_correct_both_trials:
        for i in range(len(third_trial)):
            # Only place color if the spot is free and the color was not in this position before
            if third_trial[i] is None and color != first_trial[i] and color != second_trial[i]:
                third_trial[i] = color
    
    # Fill in remaining spots with other partially correct colors not yet placed in those positions
    for i in range(len(third_trial)):
        if third_trial[i] is None:  # Spot is still free
            for trial, result in zip([first_trial, second_trial], [first_result, second_result]):
                for j, color in enumerate(trial):
                    if result[j] == 'Partially_Correct' and color not in third_trial and color != trial[i]:
                        third_trial[i] = color
                        break  # Found a suitable color, move to the next free spot
                if third_trial[i] is not None:
                    break  # Break the outer loop if the spot has been filled
    
    
    
    free_positions = [i for i in range(4)] 
    for i in range(len(first_trial)):
        if first_result[i] == 'Correct':
            confirmed_correct[i] = first_trial[i]
            free_positions.remove(i)
        elif second_result[i] == 'Correct':
            confirmed_correct[i] = second_trial[i]
            free_positions.remove(i)
            
    partial_correct_positions = {}
    for i, (color, result) in enumerate(zip(first_trial, first_result)):
        if result == 'Partially_Correct':
            partial_correct_positions[color] = partial_correct_positions.get(color, set()).union({i})
    for i, (color, result) in enumerate(zip(second_trial, second_result)):
        if result == 'Partially_Correct':
            partial_correct_positions[color] = partial_correct_positions.get(color, set()).union({i})

    for i in free_positions:
        for trial, result in zip([first_trial, second_trial], [first_result, second_result]):
            for j, color in enumerate(trial):
                if result[j] == 'Partially_Correct' and color not in confirmed_correct and j != i:
                    confirmed_correct[i] = color
                    break 
            if confirmed_correct[i] is not None:
                break

    # If there are still None values, fill them with any available partially correct color
    for i in range(4):
        if third_trial[i] is None:  # Spot is still free
            for color in partial_correct_positions.keys():
                if color not in third_trial:  # Use the color if it hasn't been used yet
                    third_trial[i] = color
                    break  # Found a suitable color, move to the next free spot
    
    for i in range(4):
        if third_trial[i] is None:  # Spot is still free
            third_trial[i] = third_trial[i-1]


    return third_trial

def make_third_move(third_trial):
    pyautogui.click(x=-1180, y=492)
    for color in third_trial:
        if color == 'Brown':
            pyautogui.click(x=-1192, y=816)
        if color == 'Yellow':
            pyautogui.click(x=-1149, y=816)
        if color == 'Pink':
            pyautogui.click(x=-1105, y=816)
        if color == 'Black':
            pyautogui.click(x=-1062, y=816)
        if color == 'White':
            pyautogui.click(x=-1018, y=816)
        if color == 'Blue':
            pyautogui.click(x=-974,  y=816)
        if color == 'Green':
            pyautogui.click(x=-929,  y=816)
    
    pyautogui.click(x=-1101, y=668)
    time.sleep(3)

def game_strategy():
    make_first_move()
    image_1 = first_get_screenshot()
    trial_1 = first_cycle(image_1)
    result_1 = first_get_feedback(image_1)
    second_trial = second_trial_strategy(trial_1, result_1)
    if len(second_trial) != 4:
        import sys
        sys.exit()

    make_second_move(second_trial)
    image_2 = second_get_screenshot()
    trial_2 = second_cycle(image_2)
    result_2 = second_get_feedback(image_2)
    third_trial = third_trial_strategy(trial_1, result_1, trial_2, result_2)
    if len(third_trial) != 4:
        import sys
        sys.exit()
    make_third_move(third_trial)
    
def next_game():
    pyautogui.click(x=-1000,  y=493)
    pyautogui.click(x=-825, y=806)
    time.sleep(3)

def end_game():
    pass
    
def ticket_get_screenshot():
    pyautogui.click(x=-455,  y=600)
    pyautogui.click(x=-40,  y=343)
    with mss() as sct:
        monitor_number = 2
        screenshot_path = 'screenshot_tickets.png'
        sct.shot(mon=monitor_number, output=screenshot_path)

    image = Image.open(screenshot_path)
    x1, y1, x2, y2 = 1880, 310, 1910, 330
    cropped_image = image.crop((x1, y1, x2, y2))
    return cropped_image

def read_tickets():
    reader = easyocr.Reader(['en'])
    image = ticket_get_screenshot()
    image_np = np.array(image)  
    ocr_result = reader.readtext(image_np)
    print(ocr_result)
    recognized_text = ocr_result[0][1]
    extracted_number = re.sub(r'\D', '', recognized_text)
    if extracted_number:
        extracted_number = float(extracted_number)
    return extracted_number

for i in range(1, 200):
    start_game()
    game_strategy()
    
    tickets = read_tickets()
    if tickets > 2000:
        end_game()
    else:
        next_game()