import pygame
import random
import sys
from threading import Thread
pygame.init()

def swap(arr, first, second):
    pygame.time.delay(delay)
    arr[first], arr[second] = arr[second], arr[first]
    draw(arr, [first, second], (255, 255, 255))

def compare(arr):
    return
 
def draw(arr: list, highlights: list = None, color: tuple[int, int, int] = None) -> None:
    win.fill((0, 0, 0))
    for i in range(len(arr)):
        if highlights is not None:
            for j in range(len(highlights)):
                if i == highlights[j]:
                    pygame.draw.rect(win, color, (startX + width * i, sizeY - arr[i] * height, width, arr[i] * height))
                else:
                    pygame.draw.rect(win, (255, 0, 0), (startX + width * i, sizeY - arr[i] * height, width, arr[i] * height))
        else:
            pygame.draw.rect(win, (255, 0, 0), (startX + width * i, sizeY - arr[i] * height, width, arr[i] * height))
    pygame.display.update()

def drawInstructions():
    mappings = [
        "Heap Sort: h",
        "Insertion Sort: i",
        "Selection Sort: s",
        "Bubble Sort: b",
        "Quick Sort: q",
        "Bogo Sort: x",
    ]
    text_surface = font.render("These are the available sorts and their respectives controls", True, (255, 255, 255))
    win.blit(text_surface, (0, 0))

    for i in range(0, len(mappings), 1):
        text_surface = font.render(mappings[i], True, (255, 255, 255))
        win.blit(text_surface, (10, (i * 30) + 30))

    pygame.display.update()

def HeapSort(arr):
    BuildMaxHeap(arr)
    for i in range(len(arr) - 1, 0, -1):
        swap(arr, 0, i)
        MaxHeapify(arr, i, 0)

def BuildMaxHeap(arr):
    heapsize = len(arr)
    for i in range(heapsize // 2 - 1, -1, -1):
        MaxHeapify(arr, len(arr), i)

def MaxHeapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[largest] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r
    
    if largest != i:
        swap(arr, i, largest)
        MaxHeapify(arr, n, largest)

def InsertionSort(arr, index):
    if len(arr) == index:
        return
    
    for i in range(index, 0, -1):
        if arr[i] < arr[i - 1]:
            swap(arr, i, i - 1)
        else:
            break
    InsertionSort(arr, index + 1)

def SelectionSort(arr):
    for i in range(0, len(arr)):
        minIndex = i
        for j in range(i, len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        swap(arr, i, minIndex)

def BubbleSort(arr):
    for _ in range(0, len(arr)):
        for i in range(0, len(arr) - 1):
            if arr[i] > arr[i + 1]:
                swap(arr, i, i + 1)

def BogoSort(arr):
    bogoCount = 0
    sorted = False
    while not sorted:
        sorted = True
        for i in range(0, len(arr) - 1):
            if arr[i] > arr[i + 1]:
                sorted = False
                break
        if sorted:
            return
        else:
            bogoCount += 1
            text_surface = font.render(str(bogoCount), True, (255, 255, 255))
            random.shuffle(arr)
        draw(arr)
        win.blit(text_surface, (10, 10))
        pygame.display.update()

def Partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            swap(arr, i, j)
    
    swap(arr, i + 1, high)
    return i + 1

def Quicksort(arr, low, high):
    if low < high:
        index = Partition(arr, low, high)
        Quicksort(arr, low, index - 1)
        Quicksort(arr, index + 1, high)

#   SETTINGS
size = 1000
num_items = 100
delay = 0
startX = 0
startY = 50
randomNumbers = False

#   CALCULATED SETTINGS
width = size / num_items
height = size / num_items 
sizeX = num_items * width
sizeY = num_items * height

#   VARIABLES
arr = []
functions = {
    'HeapSort': (HeapSort, (arr, )), 
    'InsertionSort': (InsertionSort, (arr, 0)),
    'SelectionSort': (SelectionSort, (arr, )),
    'BubbleSort': (BubbleSort, (arr, )),
    'BogoSort': (BogoSort, (arr, )),
    'Quicksort': (Quicksort, (arr, 0, num_items - 1))
}
running = False
win = pygame.display.set_mode((sizeX, sizeY))
font = pygame.font.Font(None, 36)
pygame.display.set_caption("Sorting")

#   Additional Function
def SortRunner(sort):
    global running
    func, args = sort
    func(*args)
    draw(arr)
    running = False

def RunRandom():
    global running
    running = True
    func = random.choice(list(functions))
    thread = Thread(target=SortRunner, args = (functions[func],))
    thread.daemon = True
    thread.start()

#  MAIN
if randomNumbers:
    for i in range(num_items):
        arr.append(random.randint(1, num_items))
else:
    for i in range(num_items):
        arr.append(i)
    random.shuffle(arr)

draw(arr)
drawInstructions()

while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not running and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                random.shuffle(arr)
                draw(arr)
                drawInstructions()
            elif event.key == pygame.K_a:
                RunRandom()
            elif event.key == pygame.K_h:
                running = True
                thread = Thread(target=SortRunner, args=(functions['HeapSort'],))
                thread.daemon = True
                thread.start()
            elif event.key == pygame.K_i:
                running = True
                thread = Thread(target=SortRunner, args=(functions['InsertionSort'],))
                thread.daemon = True
                thread.start()
            elif event.key == pygame.K_s:
                running = True
                thread = Thread(target=SortRunner, args=(functions['SelectionSort'],))
                thread.daemon = True
                thread.start()
            elif event.key == pygame.K_b:
                running = True
                thread = Thread(target=SortRunner, args=(functions['BubbleSort'],))
                thread.daemon = True
                thread.start()
            elif event.key == pygame.K_x:
                running = True
                thread = Thread(target=SortRunner, args=(functions['BogoSort'],))
                thread.daemon = True
                thread.start()
            elif event.key == pygame.K_q:
                running = True
                thread = Thread(target=SortRunner, args=(functions['Quicksort'],))
                thread.daemon = True
                thread.start()
