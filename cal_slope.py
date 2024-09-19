import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math

def Find_white_point_for_slope(path):
    img = Image.open(path)
    img_array = np.array(img)
   
    white_point = np.where((img_array[:, :, 0] == 255)  &
                            (img_array[:, :, 1] == 255) &
                            (img_array[:, :, 2] == 255)
                            )
    white_coordinates = list(zip(white_point[0], white_point[1]))

    if not white_coordinates:
        print("There is not White Point")
        return [0, 0], [0, 0]

    else:
            # numpy 배열로 변환
        white_coordinates = np.array(white_coordinates)

        # x가 가장 작은 경우의 y 최소점 찾기
    min_x_index = np.argmin(white_coordinates[:, 1])  # x좌표에서 최소값의 인덱스
    min_x_y_value = white_coordinates[min_x_index, 0]  # 해당 y좌표
    min_x_point = [white_coordinates[min_x_index, 1], min_x_y_value]  # (x, y) 형식으로 저장

    # x가 가장 큰 경우의 y 최소점 찾기
    max_x_index = np.argmax(white_coordinates[:, 1])  # x좌표에서 최대값의 인덱스
    max_x_y_min = white_coordinates[max_x_index, 0]  # 해당 y좌표

    # 모든 점에서 x가 최대인 경우의 y 최소값 찾기
    for point in white_coordinates:
        if point[1] == white_coordinates[max_x_index, 1]:  # x가 최대인 경우
            max_x_y_min = min(max_x_y_min, point[0])

    max_x_point = [white_coordinates[max_x_index, 1], max_x_y_min]  # (x, y) 형식으로 저장

    # 결과 출력
    
       

    # y가 가장 작은 경우
    min_y_index = np.argmin(white_coordinates[:, 0])  # y좌표에서 최소값의 인덱스
    min_y_x_values = white_coordinates[min_y_index, 1]  # 해당 x좌표
    min_y_min = min_y_x_values
    min_y_max = min_y_x_values

    for point in white_coordinates:
        if point[0] == white_coordinates[min_y_index, 0]:  # y가 최소인 경우
            min_y_min = min(min_y_min, point[1])
            min_y_max = max(min_y_max, point[1])

   
    

    p1 = [min_y_min, white_coordinates[min_y_index, 0]] 
    p2 = [min_y_max, white_coordinates[min_y_index, 0]] 
    p3 = max_x_point 
    p4 = min_x_point

    print(p1, p4)
    return p1, p4 # For calculate slope at left side

def cal_slope_angle(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]

    if dx == 0:
        slope = np.inf
        angle = 90
        return slope, angle
    else:
        slope = dy/dx
        angle = math.degrees(math.atan2(dy,dx))
        return slope, angle

filename = 'slope_angle.txt'
with open(filename, 'w') as file:
    for i in range(0,-75,-5):
        path = f"C:/Users/monog/line/lane_detection2/theta_25test{i}.jpg"
        path_BEV = f"C:/Users/monog/line/lane_detection2/BEV{i}.jpg"
       
        p1, p2 = Find_white_point_for_slope(path)
        p1_BEV, p2_BEV = Find_white_point_for_slope(path_BEV)
        slope, angle = cal_slope_angle(p1,p2)
        slope_BEV, angle_BEV = cal_slope_angle(p1_BEV, p2_BEV)
        file.write(f"{i} For theta: slope {slope}, angle {angle} For BEV: slope {slope_BEV}, angle {angle_BEV} \n")
        print(f"Complete theta{i}")    
    