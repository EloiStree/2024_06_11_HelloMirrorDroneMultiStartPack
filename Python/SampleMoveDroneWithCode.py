import socket
import struct
import threading
import time
import random

UDP_IP = "127.0.0.1"  
UDP_PORT_LISTEN_BYTE = 2571  
UDP_PORT_SEND_BYTE = 2560


# Set here the drone index in your team
# Change it before the match as you don't know before the match which drone you will be red or blue
# Option will be add to receive only your drone value
int_index_of_drone_in_team_112=1

yourIndex011= int_index_of_drone_in_team_112-1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT_LISTEN_BYTE))


long_server_current_time = 0
long_server_previous_time = 0
long_server_current_frame=0
long_server_previous_frame=0

class DroneSoccer12:
    def __init__(self,index,team:str, position_x, position_y, position_z, euler_x, euler_y, euler_z):
        self.index_1_12 = index
        self.team= team
        self.x = position_x
        self.y = position_y
        self.z = position_z
        self.euler_x = euler_x
        self.euler_y = euler_y
        self.euler_z = euler_z


drone_soccer_arena_current=[
    DroneSoccer12 (1,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (2,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (3,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (4,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (5,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (6,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (7,"Blue", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (8,"Blue", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (9,"Blue", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (10,"Blue",0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (11,"Blue",0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (12,"Blue",0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
]
drone_soccer_arena_previous=[
    DroneSoccer12 (1,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (2,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (3,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (4,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (5,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (6,"Red", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (7,"Blue", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (8,"Blue", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (9,"Blue", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (10,"Blue",0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (11,"Blue",0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    DroneSoccer12 (12,"Blue",0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
]


class SoccerPoint:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z


red_euley_y_angle=90.0
blue_euley_y_angle=270.0

class DronePlus:
    def __init__(self, previous:DroneSoccer12,current:DroneSoccer12):
        # Direction since last frame
        self.delta_direction= (x,y,z)
        # Forward of the drone but on XY flat
        self.flat_forward= (x,y,z)
        
        
# Supposed !!!!
# Need to be update from received data
red_goal= SoccerPoint(5.0,2.0,0.0)
# Supposed !!!!
# Need to be update from received data
blue_goal= SoccerPoint(-5.0,2.0,0.0)



        

       

def listen_to_server_state_byte():
    global long_server_current_time
    global long_server_previous_time
    global long_server_current_frame
    global long_server_previous_frame
    global drone_soccer_arena_current
    global drone_soccer_arena_previous
    global yourIndex011
    
    while True:
        data, addr = sock.recvfrom(1024)

        # Define the format string for the initial part
        header_format_str = 'Bqq'  # 1 byte, 2 unsigned long longs (8 bytes each)
        byte = data[0]
        long1 = struct.unpack("Q",data[1:9])
        long2 =  struct.unpack("Q",data[9:17])
        header_size = 1+8+8
        #print((header_size))
    
        # Remaining data after the initial part
        remaining_data = data[header_size:]
        #print(len(remaining_data))
        # Define the format string for one set of 3 shorts and 3 bytes
        set_format_str = '3h3B'  # 3 shorts (2 bytes each) and 3 bytes

        # Calculate the size of one set
        set_size = struct.calcsize(set_format_str)

        # Number of sets
        num_sets = len(remaining_data) // set_size

        # Unpack the sets
        sets = []
        for i in range(num_sets):
            start = i * set_size
            end = start + set_size
            sets.append(struct.unpack(set_format_str, remaining_data[start:end]))


        long_server_previous_frame = long_server_current_frame
        long_server_previous_time=  long_server_current_time
        long_server_current_frame = long2
        long_server_previous_time= long1
        # Display results
        #print(f"Byte: {byte}")
        #print(f"Long 1: {long1}")
        #print(f"Long 2: {long2}")
        #print("Sets of 3 shorts and 3 bytes:")
        
        short_max= 32767.0
        red_striker= drone_soccer_arena_current[0]
        blue_striker= drone_soccer_arena_current[6] 
        for i, (short1, short2, short3, byte1, byte2, byte3) in enumerate(sets):
            #print(f"Set {i + 1}: Shorts = ({short1}, {short2}, {short3}), Bytes = ({byte1}, {byte2}, {byte3})")
            
            drone_soccer_arena_previous[i].x = drone_soccer_arena_current[i].x
            drone_soccer_arena_previous[i].y = drone_soccer_arena_current[i].y
            drone_soccer_arena_previous[i].z = drone_soccer_arena_current[i].z
            
            drone_soccer_arena_previous[i].euler_x = drone_soccer_arena_current[i].euler_x
            drone_soccer_arena_previous[i].euler_y = drone_soccer_arena_current[i].euler_y
            drone_soccer_arena_previous[i].euler_z = drone_soccer_arena_current[i].euler_z
            
            drone_soccer_arena_current[i].x = short1/1000
            drone_soccer_arena_current[i].y = short2/1000
            drone_soccer_arena_current[i].z = short3/1000
            
            drone_soccer_arena_current[i].euler_x = (byte1/255.0)*360.0
            drone_soccer_arena_current[i].euler_y = (byte2/255.0)*360.0
            drone_soccer_arena_current[i].euler_z = (byte3/255.0)*360.0
            
        your_drone=drone_soccer_arena_current[yourIndex011]
        #print(f"Drone{yourIndex011}: {your_drone.x} , {your_drone.y} , {your_drone.z} , {your_drone.euler_y}")
        #print(f"Flags Red {red_striker.x} , {red_striker.y} , {red_striker.z}")
        #print(f"Flags Blue {blue_striker.x} , {blue_striker.y} , {blue_striker.z}")     
        
        
 # Create and start the game logic thread
game_thread = threading.Thread(target=listen_to_server_state_byte)
game_thread.start()


def display_game_state():
    global drone_soccer_arena_current
    global gamepad 
    global yourIndex011 
    
    while True:
        print(f"Drone {yourIndex011}: Position ({drone_soccer_arena_current[yourIndex011].x}, {drone_soccer_arena_current[yourIndex011].y}, {drone_soccer_arena_current[yourIndex011].z}), Euler Angles ({drone_soccer_arena_current[yourIndex011].euler_x}, {drone_soccer_arena_current[yourIndex011].euler_y}, {drone_soccer_arena_current[yourIndex011].euler_z})")
        print(f"Gamepad: {gamepad.joystickLeftX_rotate_left_right}, {gamepad.joystickLeftY_move_down_up}, {gamepad.joystickRightX_move_left_right}, {gamepad.joystickRightY_move_back_forward} | {gamepad.integer_representation}")
        time.sleep(1)
        # for drone in drone_soccer_arena_current:
        #     print(f"Drone {drone.index_1_12}: Position ({drone.x}, {drone.y}, {drone.z}), Euler Angles ({drone.euler_x}, {drone.euler_y}, {drone.euler_z})")

# Create and start the display thread
display_thread = threading.Thread(target=display_game_state)
display_thread.start()

class GamepadInput:
    def __init__(self):
        self.joystickLeftX_rotate_left_right=0.0
        self.joystickLeftY_move_down_up=0.0
        self.joystickRightX_move_left_right=0.0
        self.joystickRightY_move_back_forward=0.0
        self.integer_representation=0
        self.drone_id20=-1
        
    def zero(self):
        self.joystickLeftX_rotate_left_right=0.0
        self.joystickLeftY_move_down_up=0.0
        self.joystickRightX_move_left_right=0.0
        self.joystickRightY_move_back_forward=0.0
        self.integer_representation=0
        self.drone_id20=-1
    
        
    def parse_percent11_to_1_99(self,value):    
        return round((((value +1.0)/2.0)*98.0)+1.0)
    
    def update_integer_representation(self):
        is_negative = self.drone_id20 < 0
        int_cmd = 0
        int_cmd += self.parse_percent11_to_1_99(self.joystickLeftX_rotate_left_right) * 1000000
        int_cmd += self.parse_percent11_to_1_99(self.joystickLeftY_move_down_up) * 10000
        int_cmd += self.parse_percent11_to_1_99(self.joystickRightX_move_left_right) * 100
        int_cmd += self.parse_percent11_to_1_99(self.joystickRightY_move_back_forward) * 1
        int_cmd += abs( self.drone_id20) * 100000000
        if(is_negative):
            int_cmd = -int_cmd
        self.integer_representation = int_cmd
    
    def set_joysticks(self,joystickLeftX_rotate_left_right,joystickLeftY_move_down_up,joystickRightX_move_left_right,joystickRightY_move_back_forward):
        self.joystickLeftX_rotate_left_right=joystickLeftX_rotate_left_right
        self.joystickLeftY_move_down_up=joystickLeftY_move_down_up
        self.joystickRightX_move_left_right=joystickRightX_move_left_right
        self.joystickRightY_move_back_forward=joystickRightY_move_back_forward
        
        self.integer_representation=0
        self.drone_id20=-1
        
        self.update_integer_representation()
    
     
gamepad= GamepadInput()
    


def send_udp_int_as_byte(value:int):
    global UDP_PORT_SEND_BYTE, UDP_IP
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    byte_value =struct.pack('<i', value)
    sock.sendto(byte_value, (UDP_IP, UDP_PORT_SEND_BYTE))
    print("I: "+str(value))
    sock.close()
    

#-----------------------------------------------------------------------#
# Your coder here to move the drone as beginner example
#-----------------------------------------------------------------------#


#----------------------#
#  Drone Move Actions  #
#----------------------#



def push_gamepad():
    global gamepad
    send_udp_int_as_byte(gamepad.integer_representation)
        

def  move_forward():
    global gamepad
    gamepad.set_joysticks(0.0,0.0,0.0,1)
    push_gamepad()

def  move_backward():
    global gamepad
    gamepad.set_joysticks(0.0,0.0,0.0,-1)
    push_gamepad()
    
def  rotate_left():
    global gamepad
    gamepad.set_joysticks(-1,0,0,0)
    push_gamepad()
    
def  rotate_right():
    global gamepad
    gamepad.set_joysticks(1.0,0,0,0)
    push_gamepad()
    
def  move_left():
    global gamepad
    gamepad.set_joysticks(0.0,0,-1.0,0.0)
    push_gamepad()

def  move_right():
    global gamepad
    gamepad.set_joysticks(0,0,1.0,0)
    push_gamepad()

def  move_down():
    global gamepad
    gamepad.set_joysticks(0,-1.0,0,0)
    push_gamepad()

def  move_up():
    global gamepad
    gamepad.set_joysticks(0,1.0,0,0)
    push_gamepad()

def RF32():
    return round((2.0*random.random())-1.0,2)


def game_logic_start():

    print("Hello Drone Soccer XR !")
    seconds_between_actions=5
    while True:
        
        
        time.sleep(seconds_between_actions)
        move_forward()
        time.sleep(seconds_between_actions)
        move_backward()
        time.sleep(seconds_between_actions)
        rotate_left()
        time.sleep(seconds_between_actions)
        rotate_right()
        time.sleep(seconds_between_actions)
        move_left()
        time.sleep(seconds_between_actions)
        move_right()
        time.sleep(seconds_between_actions)
        move_down()
        time.sleep(seconds_between_actions)
        move_up()
        time.sleep(seconds_between_actions)
        
        
        gamepad.set_joysticks(0.0,0.0,0.0,0.0)
        push_gamepad()
        time.sleep(seconds_between_actions)
        gamepad.set_joysticks(-1,-1,-1,-1)
        push_gamepad()
        time.sleep(seconds_between_actions)
        gamepad.set_joysticks(1,1,1,1)
        push_gamepad()
        time.sleep(seconds_between_actions)
        
        gamepad.set_joysticks(RF32(),RF32(),RF32(),RF32())
        push_gamepad()
        time.sleep(3)
        
        print("Tick ")
        
        
        

















game_logic_start()






