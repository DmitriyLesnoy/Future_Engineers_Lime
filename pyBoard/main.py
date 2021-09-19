import pyb
import utime
import machine
from pyb import UART, Pin, Timer
from module import PWM, map, median, constrain, encoder, Thread

vcc = pyb.ADC("Y12")  # create an analog object from a pin
l1 = pyb.LED(2)

servo1 = pyb.Servo(1)
servo1.angle(0)

timer_move2 = -1
speed = 0
speed_fix = 0
timer_jumm = 0

# racer
m_A_shim = PWM("X6", 50000)
# m_B_shim = PWM('X7', 50000)

m_A_1 = Pin('X8', Pin.OUT_PP)
m_A_2 = Pin('X5', Pin.OUT_PP)

# m_B_1 = Pin('Y10', Pin.OUT_PP)
# m_B_2 = Pin('Y11', Pin.OUT_PP)

light = PWM("Y10", 50000)

enc = encoder('Y3')

print("Start work")

# uart = UART(6, 115200, stop=2, timeout=5)  # timeout=5, timeout_char=3
uart = UART(6, 115200, stop=1)  # timeout=5, timeout_char=3

r = -1
timer_move = 0
vcc_list = []
tt = utime.ticks_ms()

tencoder = utime.ticks_ms()

p2 = Pin("Y6")  # Y6
tim = Timer(1, freq=500)
ch = tim.channel(1, Timer.PWM, pin=p2)

for i in range(100, 3000, 10):
    tim.freq(i)
    ch.pulse_width_percent(30)
    utime.sleep_ms(1)
ch.pulse_width_percent(100)

msgs = ""
buffer = bytearray()
buf = bytearray()
flag_packet = False
light_flag = False

sw = pyb.Switch()
button_press = 0


def press():
    global button_press
    button_press = 1

sw.callback(press)


def move(m_left, m_right):
    global m_A_shim, m_B_shim, m_A_1, m_A_2, m_B_1, m_B_2
    # print("move ",m_left)
    # m_left = constrain(m_left, -100, 100)
    # m_right = constrain(m_right, -100, 100)
    if m_left >= 0:
        # print("l",m_left)
        m_A_1.high()
        m_A_2.low()
        m_A_shim.pwm_write(m_left)
    else:
        m_A_1.low()
        m_A_2.high()
        m_A_shim.pwm_write(-m_left)

def fix_move_t():
    global timer_move2, timer_move
    while 1:

        if timer_move > -1:
            if timer_move < utime.ticks_ms():
                move(0, 0)
                timer_move = -1
        utime.sleep_ms(1)


tr_move = Thread(target=fix_move_t)
tr_move.start()

def encoder_work():
    global speed, enc
    tencoder = utime.ticks_ms() + 10
    while 1:
        if utime.ticks_ms() > tencoder:
            speed = enc.value()
            if speed > 80:
                # print("sboy", speed)
                speed = 0
                enc.reset(add=False)
            else:
                enc.reset()

            tencoder = utime.ticks_ms() + 10
        utime.sleep_ms(1)


tr1 = Thread(target=encoder_work)
tr1.start()

filename = ""
last_error = 0
while 1:

    val = vcc.read()  # read an analog value
    vcc_list.append(float(val) * 0.00388)  # roboracer 0

    if len(vcc_list) > 100:
        vcc_list.pop(0)

    if utime.ticks_ms() - last_error > 3000:
        l1.off()

    if uart.any() > 0:
        buf += uart.read(uart.any())
        i = 0
        stop_marker = 0
        for b in buf:
            if b == 124:
                stop_marker = i
                flag_packet = True
            i += 1

        buffer = buf[:stop_marker]
        buf = buf[stop_marker:]

    if flag_packet == True:
        flag_packet = False
        msgss = b''
        try:
            msgss = str(buffer, "utf-8").split('|')
        except:
            continue
        buffer = bytearray()

        for msgs in msgss:
            if len(msgs) == 0:
                continue
            try:
                answ = ""
                command = msgs[0]
                # print(msgs)

                if command == 'M':
                    # print("move work")
                    m = msgs.split(',')
                    # print(m)
                    timer_move = utime.ticks_ms() + int(m[3])
                    m1 = map(int(m[1]), -255, 255, -100, 100)
                    m2 = map(int(m[2]), -255, 255, -100, 100)
                    move(m1, m2)
                    # answ = 'M,0|'
                elif command == 'C':
                    # RGB color
                    answ = 'C,0|'
                elif command == 'D':
                    answ = 'D,100|'
                elif command == 'P':
                    # VCC
                    answ = "P," + str(int(speed)) + '|'
                    # answ = '0|'

                elif command == 'V':
                    # VCC
                    v = '%.2f' % round(median(vcc_list), 2)
                    answ = "V," + str(v) + '|'
                    # answ = '0|'
                elif command == 'B':
                    # BUTTON
                    answ = "B," + str(button_press) + '|'
                    button_press = 0
                elif command == 'T':
                    # TONE
                    m = msgs.split(',')
                    # print("tone", m)
                    tim.freq(int(m[1]))
                    ch.pulse_width_percent(1)
                    utime.sleep_ms(int(m[2]))
                    ch.pulse_width_percent(100)
                    answ = "T," + '0|'
                elif command == 'S':  # S,4,-600,-20,1,40|
                    # SERVO
                    m = msgs.split(',')
                    # print(m)
                    servo1.angle(int(float(m[2])))
                    # answ = "S," + '0|'
                    # print("servo",int(float(m[1])))
                    # uart.write('S,1 \r\n')

                elif command == 'O':
                    # odometr
                    odometr = enc.odometr()
                    answ = 'O,' + str(round(odometr * 0.2, 1)) + ',' + str(round(odometr * 0.2, 1)) + '|'
                elif command == 'o':
                    enc.reset_odometr()
                    answ = 'o,' + str(0) + '|'


            except Exception as e:
                #                print("ERROR!", e, msgss)
                l1.on()
                last_error = utime.ticks_ms()
            if answ != "":
                try:
                    uart.write(answ)
                except Exception as e:
                    pass

        buffer = bytearray()
