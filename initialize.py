import os

def initialize():
    os.makedirs('extract/', exist_ok=True)
    os.makedirs('extract/by_category/', exist_ok=True)
    os.makedirs('extract/images/', exist_ok=True)

