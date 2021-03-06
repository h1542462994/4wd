
# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

# version : 3
# 小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24

#超声波引脚定义
EchoPin = 0
TrigPin = 1

#灭火电机引脚设置
OutfirePin = 2

# 小车按键定义
key = 8
#舵机引脚定义
ServoPin = 23
# 循迹红外引脚定义
# TrackSensorLeftPin1 TrackSensorLeft/Pin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1 = 3  # 定义左边第一个循迹红外传感器引脚为3口
TrackSensorLeftPin2 = 5  # 定义左边第二个循迹红外传感器引脚为5口
TrackSensorRightPin1 = 4  # 定义右边第一个循迹红外传感器引脚为4口
TrackSensorRightPin2 = 18  # 定义右边第二个循迹红外传感器引脚为18口

# 设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)


# 忽略警告信息
GPIO.setwarnings(False)

speed_fast = 20  # 块
speed_middle = 18  # 小弯的速度
speed_slow = 15
speed_veryslow = 12
time_sleep = 0.005
sonic_sleep = 5
sonic_distance = 40
end_distance = 20

angle_right = 45
angle_front = 80
angle_left = 135

blood = 5

# 电机引脚初始化为输出模式
# 按键引脚初始化为输入模式
# 寻迹引脚初始化为输入模式
def init():
    global pwm_ENA
    global pwm_ENB
    global pwm_servo
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(key, GPIO.IN)
    GPIO.setup(ServoPin, GPIO.OUT)
    GPIO.setup(TrackSensorLeftPin1, GPIO.IN)
    GPIO.setup(TrackSensorLeftPin2, GPIO.IN)
    GPIO.setup(TrackSensorRightPin1, GPIO.IN)
    GPIO.setup(TrackSensorRightPin2, GPIO.IN)
    GPIO.setup(OutfirePin, GPIO.OUT, initial=GPIO.HIGH)
    # RGB三色灯设置为输出模式
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)

    GPIO.setup(EchoPin, GPIO.IN)
    GPIO.setup(TrigPin, GPIO.OUT)

    # 设置pwm引脚和频率为2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    #设置舵机的频率和起始占空比
    pwm_servo = GPIO.PWM(ServoPin, 50)
    pwm_servo.start(0)


#舵机旋转到指定角度
def servo_appointed_detection(pos):
    for i in range(18):
        pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)

# 小车前进
def run(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


# 小车后退
def back(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


# 小车左转
def left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


# 小车右转
def right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


# 小车原地左转
def spin_left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


# 小车原地右转
def spin_right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)


def out_fire(fire):
    if fire:
        GPIO.output(OutfirePin, GPIO.LOW)
    else:
        GPIO.output(OutfirePin, GPIO.HIGH)

# 小车停止
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


# 按键检测
def key_scan():
    while GPIO.input(key):
        pass
    while not GPIO.input(key):
        time.sleep(0.01)
        if not GPIO.input(key):
            time.sleep(0.01)
        while not GPIO.input(key):
            pass


def track_sensor():
    TrackSensorLeftValue1 = GPIO.input(TrackSensorLeftPin1)
    TrackSensorLeftValue2 = GPIO.input(TrackSensorLeftPin2)
    TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
    TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
    return (TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1, TrackSensorRightValue2)


#超声波函数
def distance_test():
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
    t1 = time.time()
    while GPIO.input(EchoPin):
        pass
    t2 = time.time()
    value = ((t2 - t1) * 340 / 2) * 100
    print "distance is %d " % value
    time.sleep(0.001)
    return value


def distance_test_super():
    list = []
    for i in range(0, 1):
        list.append(distance_test())
    min_value = min(list)
    print "distance is %d " % min_value

    return min_value


def light(r, g, b):
    if r:
        GPIO.output(LED_R, GPIO.HIGH)
    else:
        GPIO.output(LED_R, GPIO.LOW)
    if g:
        GPIO.output(LED_G, GPIO.HIGH)
    else:
        GPIO.output(LED_G, GPIO.LOW)
    if b:
        GPIO.output(LED_B, GPIO.HIGH)
    else:
        GPIO.output(LED_B, GPIO.LOW)


def do_scan():
    tick = 2
    start = time.time()
    #舵机旋转到0度，即右侧，测距
    servo_appointed_detection(angle_right)
    out_fire(1)

    while True:
        t2 = time.time() % 10
        t3 = time.time() % 11
        t4 = time.time() % 12
        r = 255 * t2 / 10
        g = 255 * t3 / 11
        b = 255 * t4 / 12

        t = time.time() % 0.05 * 1000
        if t < r / 255 * 50:
            GPIO.output(LED_R, GPIO.HIGH)
        else:
            GPIO.output(LED_R, GPIO.LOW)
        if t < g / 255 * 50:
            GPIO.output(LED_G, GPIO.HIGH)
        else:
            GPIO.output(LED_G, GPIO.LOW)
        if t < b / 255 * 50:
            GPIO.output(LED_B, GPIO.HIGH)
        else:
            GPIO.output(LED_B, GPIO.LOW)
        end = time.time()
        if end - start > tick * 0.45:
            servo_appointed_detection(angle_left)
        if end - start > tick * 0.9:
            servo_appointed_detection(angle_front)
        if end - start > tick:
            break
        time.sleep(0.03)
    out_fire(0)


def do_state(state):
    if state == 0:
        spin_right(speed_slow, speed_veryslow)
    elif state == 1:
        spin_left(speed_veryslow, speed_slow)
    elif state == 2:
        right(speed_middle, 0)
    elif state == 3:
        left(0, speed_middle)
    elif state == 4:
        run(speed_fast, speed_fast)
    elif state == -1:
        brake()

def doing():
    # 延时2s
    global blood
    time.sleep(2)

    # try/except语句用来检测try语句块中的错误，
    # 从而让except语句捕获异常信息并处理。
    try:
        init()
        key_scan()
        (TrackSensorLeftValue1Old, TrackSensorLeftValue2Old, TrackSensorRightValue1Old, TrackSensorRightValue2Old) = (True, True, True, True)
        # car_state = 1
        distance_old = 100
        last_tick = time.time() - sonic_sleep - 1
        run_state = -1
        servo_appointed_detection(angle_front)
        while blood > 0:
            # 检测到黑线时循迹模块相应的指示灯亮，端口电平为LOW
            # 未检测到黑线时循迹模块相应的指示灯灭，端口电平为HIGH
            (TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1, TrackSensorRightValue2) = track_sensor()

            # car_state: 0=在预定轨迹内，1=第一次偏离轨迹，2=非第一次偏离轨迹
            if TrackSensorLeftValue2 == 0 or TrackSensorRightValue1 == 0:
                car_state = 0
            else:
                car_state = 1

            if car_state == 1:
                # if TrackSensorLeftValue2Old == False and TrackSensorRightValue1Old == False:
                #     d = distance_test()
                #     if d < end_distance:
                #         # time.sleep(time_sleep)
                #         # (TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1,
                #         #  TrackSensorRightValue2) = track_sensor()
                #         # if TrackSensorLeftValue1 == 1 and TrackSensorLeftValue2 == 1 and TrackSensorRightValue1 == 1 and TrackSensorRightValue2 == 1:
                #         brake()
                #         while True:
                #             time.sleep(time_sleep)
                #             (TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1,
                #              TrackSensorRightValue2) = track_sensor()
                #             light(1, 0, 0)
                #             if TrackSensorLeftValue2 == 0 or TrackSensorRightValue1 == 0:
                #                 break
                #     else:
                #         pass

                # 四路循迹引脚电平状态
                # X X X 0
                # 以上6种电平状态时小车原地右转
                # 处理右锐角和右直角的转动
                if TrackSensorRightValue2Old == False:
                    run_state = 0
                    do_state(run_state)
                    if TrackSensorRightValue2 != TrackSensorRightValue2Old:
                        time.sleep(time_sleep)

                # 四路循迹引脚电平状态
                # 0 X X X
                # 处理左锐角和左直角的转动
                elif TrackSensorLeftValue1Old == False:
                    run_state = 1
                    do_state(run_state)
                    if TrackSensorLeftValue1 != TrackSensorLeftValue1Old:
                        time.sleep(time_sleep)



            # 四路循迹引脚电平状态
            # X 0 1 X
            # 处理左小弯
            elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
                run_state = 3
                do_state(run_state)

            # 四路循迹引脚电平状态
            # X 1 0 X
            # 处理右小弯
            elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
                run_state = 2
                do_state(run_state)

            # 四路循迹引脚电平状态
            # X 0 0 X
            # 处理直线
            elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
                run_state = 4
                do_state(run_state)

            # 当为1 1 1 1时小车保持上一个小车运行状态
            TrackSensorLeftValue1Old, TrackSensorLeftValue2Old, TrackSensorRightValue1Old, TrackSensorRightValue2Old = TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1, TrackSensorRightValue2

            # 显示血量
            blood_time = time.time() % 3
            if blood_time < blood * 0.4:
                b_time = blood_time % 0.4
                if b_time < 0.2:
                    light(0, 1, 0)

            distance = distance_test()

            if distance < sonic_distance and distance_old >= sonic_distance:
                current_tick = time.time()
                if current_tick - last_tick > sonic_sleep:
                    brake()
                    do_scan()
                    do_state(run_state)
                    last_tick = current_tick
                    blood = blood - 1
            distance_old = distance
    except KeyboardInterrupt:
        pass
    pwm_ENA.stop()
    pwm_ENB.stop()
    pwm_servo.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    doing()

