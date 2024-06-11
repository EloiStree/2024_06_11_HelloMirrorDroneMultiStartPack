import inputs
import time
import socket
import struct


# 0 means what ever, the drone I suppose to control when you don't play several of them
drone_soccer_fixed_id=0

# 1-6 is read team and 1 is the stricker
#drone_soccer_fixed_id=1

# 7-12 is blue team and 7 is the stricker
#drone_soccer_fixed_id=7

# negative means drone that I can control in soccer match
drone_soccer_fixed_id=-1

# INT COMMAND DRONE: ROTATE, VERTICAL, HORIZONTAL, DEPTH
#20 99 88 77 66
#2099887766
# PORT : 2560

# RD red drone BD blue drone 0-5  0 is the stricker
# DRONE ALIAS: ROTATE: VERTICAL: HORIZONTAL: DEPTH
#RD0:0.0:0.0:0.0:0.0
# PORT : 2559

drone_soccer_fixed_id=12
drone_soccer_fixed_id=-1




address_target = "127.0.0.1"
port_target_byte = 2560


# def push_cmd_as_text(cmd):
#         try:
#             sock_byte.sendto(cmd.encode(), (address_target, port_target_text))
#         except Exception as e:
#             i=0
#             print(f"Error pushing command T: {e}")
 
def send_udp_int_as_byte(value:int):
    global port_target_byte
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Convert the integer to a byte

    byte_value =struct.pack('i', value)

    # Send the byte over UDP to localhost on the specified port
    sock.sendto(byte_value, ('localhost', port_target_byte))

    # Close the socket
    sock.close()



def parse_joystick_to_command( alias, rotate, vertical, horizontal, depth):
    return f"{alias}:{round(rotate,1)}:{round(vertical,1)}:{round(horizontal,1)}:{round(depth,1)}"
   

    


def parse_percent11_to_1_99(value):
    
    value=value/32767.0
    return round((((value +1.0)/2.0)*98.0)+1.0)

def read_joystick_values():
    previous_int_cmd = 0
    gamepad = inputs.devices.gamepads[0]  # Assuming only one gamepad is connected
    
    joystick_1_x=0
    joystick_1_y=0
    joystick_2_x=0
    joystick_2_y=0
    joystick_1_x_percent=0
    joystick_1_y_percent=0
    joystick_2_x_percent=0
    joystick_2_y_percent=0
    joystick_1_x_percent_99=0
    joystick_1_y_percent_99=0
    joystick_2_x_percent_99=0
    joystick_2_y_percent_99=0


    while True:
        events = inputs.get_gamepad()
        for event in events:
            if event.code.startswith("ABS_X"):
                joystick_1_x=event.state 
                joystick_1_x_percent = event.state/32767.0
                joystick_1_x_percent_99 =parse_percent11_to_1_99 (event.state)
            elif event.code.startswith("ABS_Y"):
                joystick_1_y=event.state 
                joystick_1_y_percent = event.state/32767.0
                joystick_1_y_percent_99 =parse_percent11_to_1_99 (event.state)
            elif event.code.startswith("ABS_RX"):
                joystick_2_x=event.state 
                joystick_2_x_percent = event.state/32767.0
                joystick_2_x_percent_99 =parse_percent11_to_1_99 (event.state)
            elif event.code.startswith("ABS_RY"):
                joystick_2_y=event.state 
                joystick_2_y_percent = event.state/32767.0
                joystick_2_y_percent_99 =parse_percent11_to_1_99 (event.state)


        string_cmd =parse_joystick_to_command("RD0",joystick_1_x_percent,joystick_1_y_percent,joystick_2_x_percent,joystick_2_y_percent)
        

        is_negative = drone_soccer_fixed_id < 0
        int_cmd = 0
        int_cmd += (joystick_1_x_percent_99) * 1000000
        int_cmd += (joystick_1_y_percent_99) * 10000
        int_cmd += (joystick_2_x_percent_99) * 100
        int_cmd += (joystick_2_y_percent_99) * 1
        int_cmd += abs( drone_soccer_fixed_id) * 100000000
        if(is_negative):
            int_cmd = -int_cmd
            
        
        print("Cmd INT  :", int_cmd)
        print("Cmd TEXT :", string_cmd)
        print(f"Joystick 1 X:{joystick_1_x} Percent {joystick_1_x_percent}" )
        print(f"Joystick 1 Y:{joystick_1_y} Percent {joystick_1_y_percent}" )
        print(f"Joystick 2 X:{joystick_2_x} Percent {joystick_2_x_percent}" )
        print(f"Joystick 2 Y:{joystick_2_y} Percent {joystick_2_y_percent}" )

        if(previous_int_cmd != int_cmd):
            previous_int_cmd = int_cmd
            send_udp_int_as_byte(int_cmd)

        

read_joystick_values()
