from lib.msg_to_chat_responce import responce
from serial import Serial
from time import sleep
from pykakasi import kakasi
import time
import sys
import RPi.GPIO as GPIO

def switch_callback(gpio_pin):
	global move, move_time,move_start_time
	move = not move
	if move == True:
		GPIO.output(mortor_pin, True)
		move_start_time = time.time()
	else:
		GPIO.output(mortor_pin, False)
		move_time += time.time() - move_start_time
	print("コールバック",gpio_pin)
	

# モーター関連
move = False
move_time = 0
move_start_time = 0
# PIN関連
speaker_a_pin = 22
mortor_pin = 24
GPIO.setmode(GPIO.BOARD)
GPIO.setup(mortor_pin, GPIO.OUT)
GPIO.setup(speaker_a_pin, GPIO.IN)
GPIO.add_event_detect(speaker_a_pin, GPIO.FALLING,bouncetime=100)
GPIO.add_event_callback(speaker_a_pin, switch_callback) #スイッチ入力端子の状態をcallbackのトリガとして指定します。     

class text2speech(object):

	SERIALPORT = '/dev/ttyAMA0'
	DEVICE     = 'ATP3012'
	TIMEOUT   = 3
	BAUDRATE = 9600
	DICT_BEFORE = {'こんにちは':'konnitiwa','は、':'wa,','？':'?','！':'\'.','～':'kara',
		'（':',','）':',','「':',','」':',','、':',','':'','。':'.','．':'.','＝':"=","：":","}
	DICT_AFTER = {'uu':'u-','oo':'o-','ou':'o-','ee':'e-','aa':'a-','ii':'i-','iu':'yu-','ha,':'wa,'}

	def __init__(self, model='ATP3012'):
		self.model=model
		self.ser = Serial(self.SERIALPORT, baudrate=self.BAUDRATE, timeout=self.TIMEOUT)

	def write(self, msg):
		self.msg = self.kanji2roman(msg) + "\r"
		print(self.msg)
		# self.msg = msg
		print('speak start')
		while True:
			self.ser.write(bytes("\r",'ascii'))
			rx = self.ser.read()
			status = rx.decode('utf-8') # status is null
			print(status)
			if status=='*':    # busy
				sleep(1)
			elif status=='>':  # ready
				print(bytes(self.msg,'ascii'))
				self.ser.write(bytes(self.msg,'ascii'))
				rx = self.ser.read()
				break
		print('speak end')




