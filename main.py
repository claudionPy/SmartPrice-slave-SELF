# Importing the modules
import socketio
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import config
import logging
import logging_config
import json
import time

# Setting a variable containing the master device server link
master_url = 'http://smartprice.local:80/'

# Initializing the logging configuration from logging_config.py file
logging_config.setup_logging()

# Initializing RGB MATRIX options from config.py file
options = RGBMatrixOptions()
for key, value in config.LED_OPTIONS.items():
    setattr(options, key, value)
matrix = RGBMatrix(options=options)

# Setting fonts and color
font_large = graphics.Font()
font_large.LoadFont("/home/raspberry/SmartPrice/fonts/custom.bdf")

font_small = graphics.Font()
font_small.LoadFont("/home/raspberry/SmartPrice/fonts/custom_small.bdf")

text_color = graphics.Color(255, 255, 255)

# Defining background functions:

# This function splits the price in 2 parts 
# Displaying the price with the first 3 numbers at regular size and the last a little smaller
# Usually fuel prices are written like this to help customers read the valuable part of the price (0.00)
def split_price(price):
    return price[:-1], price[-1]

# This function saves the price recived from the user into a Json file
def save_json(fiprice, seprice, namefile="logprice.json"):
    logprice = {"fiprice": fiprice, "seprice": seprice}
    try:
        with open(namefile, 'w') as file:
            json.dump(logprice, file, indent=4)
        logging.info("Prices saved to JSON successfully.")
    except IOError as e:
        logging.error(f"Failed to save prices to JSON: {e}")

# This function reads the price from the previous created Json file
def read_json(namefile="logprice.json"):
    try:
        with open(namefile, 'r') as file:
            prices = json.load(file)
            return prices.get("fiprice"), prices.get("seprice")
    except FileNotFoundError:
        logging.warning(f"File {namefile} not found")
    except json.JSONDecodeError:
        logging.error("Decoding JSON failed")
    return None, None

# This function simply displays the prices that will come from the user
def display_prices(price1, price2):
    try:
        # Clears the matrix from other texts (there shouldn't be any text, but it's common practice to clear everything)
        matrix.Clear()

        # Sets the returning result of the split_price function on 2 variables ({first 3 numbers}, {last number})
        price1_main, price1_last = split_price(price1)
        price2_main, price2_last = split_price(price2)

        # Here we use the splitted prices to display in normal size the first 2 numbers
        graphics.DrawText(matrix, font_large, 64, 31, text_color, price1_main)
        graphics.DrawText(matrix, font_large, 0, 31, text_color, price2_main)

        # Sets the offset space to display the last small number in the right position
        offset_large = graphics.DrawText(matrix, font_large, 64, 31, text_color, price1_main)
        graphics.DrawText(matrix, font_small, 64 + offset_large, 21, text_color, price1_last)

        offset_large = graphics.DrawText(matrix, font_large, 0, 31, text_color, price2_main)
        graphics.DrawText(matrix, font_small, 0 + offset_large, 21, text_color, price2_last)

    except Exception as e:
        logging.error(f"error, couldn't update the matrix: {e}")
        raise

# Here we can find the part of the script that runs at first boot or at every reboot
# This is made to prevent the panel to lose the prices if he gets rebooted or the script break and restart
fiprice, seprice = read_json()
if fiprice and seprice:
    display_prices(fiprice, seprice)
else:
    logging.error("Couldn't find prices in logprice.json")

# This function attempts a connection to the master device
def attempt_connection():
    while True:
        try:
            sio.connect(master_url)
            break
        except socketio.exceptions.ConnectionError:
            logging.error(f"error, connection to master device failed, retrying in 10s")
            time.sleep(10)

# Below here we instatiate socketio and set events that handles the connection and disconnection
sio = socketio.Client()

@sio.event
def connect():
    logging.info("Successfully connected to the server.")

@sio.event
def disconnect():
    logging.info("Disconnected from the server.")

# Here we update the prices when recived from the master device
@sio.on('update_prices')
def on_price_recived(data):
    try:
        price1 = data['price1']
        price2 = data['price2']
        display_prices(price1, price2)
        save_json(price1, price2)
    except KeyError as e:
        logging.error(f"Key error: {e} - data received: {data}")

# running the functions
if __name__ == '__main__':
    attempt_connection()
    sio.wait()
