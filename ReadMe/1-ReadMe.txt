#installation guide of SmartPrice-slave
#device supported = Raspberry pi 3 model B
#HAT supported = Adafruit HAT Hub75
#Matrix supported = Led Outdoor P5 64x32px matrix
#python version tested 3.9
#Raspberry Pi Os 32bit, debian bullseye, 0.4gb


#FOR A CORRECT INSTALLATION, YOU MUST FOLLOW THIS FILE, DO NOT SKIP ANY STEP!

device username = raspberry
device password = smartprice-rpi
device local hostname = smartprice-slave(n).local

if you didn't install SmartPrice with git, please install git: sudo apt install git
rename the entire folder from SmartPrice-Duo-slave to SmartPrice: sudo mv SmartPrice-Duo-slave SmartPrice
navigate into /SmartPrice
install python3-venv: sudo apt install python3-venv
create a virtual environment into /SmartPrice: python3 -m venv venv
activate it: source venv/bin/activate
install the packages into the virtual environment: pip3 install -r requirements.txt
install rpi-rgb-led-matrix library (see the file "rpi-rgb-led-matrix")
after installing rpi-rgb-led-matrix, deactivate the venv: deactivate
create the service file (see the file "service-config")
check if everything works by connecting to the master device web service, change the prices and they should appear on your client device
please note that you have to wait around a minute before the two device connect to eachother

IMPORTANT NOTE:
THE FOLLOWING INSTRUCTIONS ARE WRITTEN FOR SMARTPRICE-DUO(SLAVE) DEVICE OF THE SMARTPRICE-DUO SOLUTION
TO COMPLETE THE INSTALLATION OF SP-DUO YOU NEED TO FOLLOW THE SMARTPRICE-DUO(MASTER) INSTRUCTIONS
ON THE SECOND DEVICE, IF YOU NEED TO RUN SMARTPRICE ON A SINGLE DEVICE PLEASE INSTALL 'SMARTPRICE'
NOT THE 'DUO' VERSION.

if you got any troubles on the installation and configuration feel free to ask help at our helpdesk
send an email to: lopreiatoclaudio.finnd@gmail.com
in the email, describe your problem in short, leave ur name, surname, company name and a phone number
we will contact you back to solve your problems

Thank you for trusting in us!
 
