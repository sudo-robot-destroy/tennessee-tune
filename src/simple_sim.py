#!/usr/bin/env python
'''
servo_packet format:
float 	motor_speed [4]

fdm_packet format:
double timestamp
double imu_angular_velocity_rpy[3]
double imu_linear_acceleration_xyz[3]
double imu_orientation_quat[4]
double velocity_xyz[3]
double position_xyz[3]
(this info came from https://matthewgong.com/libraries/classSITL_1_1Gazebo.html)
'''

import socket
import struct


UDP_IP = "127.0.0.1"
SEND_UDP_PORT = 9003
REC_UDP_PORT = 9002

send_sock = socket.socket(socket.AF_INET,  # Internet
                          socket.SOCK_DGRAM)  # UDP

rec_sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
rec_sock.bind((UDP_IP, REC_UDP_PORT))
#measurement = XXX

trash_iter = 0
while True:
    servo_packet = rec_sock.recv(16)  # buffer size is 16 since a servo_packet is 4 floats (4x4=16)
    motor_vals = struct.unpack("4f", servo_packet)
    print "received motor values:", motor_vals
    fdm_packet = struct.pack("17d", trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter,trash_iter)#  17 doubles is 136 bytes (each is 8)
    send_sock.sendto(fdm_packet, (UDP_IP, SEND_UDP_PORT))
    trash_iter += 1

