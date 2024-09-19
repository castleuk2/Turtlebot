import math
import numpy as np
from PIL import Image, ImageDraw
import os
import matplotlib.pyplot as plt
def Find_angle(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1

    angle_radian = math.atan2(dy,dx)
    angle_degree = math.degrees(angle_radian)

    return angle_degree



def rotate_points(points_array, angle):
    # 회전 각도를 라디안으로 변환
    pi = np.radians(angle)
    rotated_points = np.zeros_like(points_array)
    
    rotated_points[:, 0] = points_array[:,0] * math.cos(pi) - points_array[:,1] * math.sin(pi)
    rotated_points[:, 1] = points_array[:,0] * math.sin(pi) + points_array[:,1] * math.cos(pi)
    
    return rotated_points


def make_line_pic(delta=0.0, pi=0.0):
    # 단위는 mm 기준
    Focal_length = 3.67

    # degree
    Horizontal_FOV = 70.42
    Vertical_FOV = 43.3

    # lens width, height  --> w: 5.18mm, h: 2.91mm
    lens_width = 2 * Focal_length * math.tan(math.radians(Horizontal_FOV/2))
    lens_height = 2 * Focal_length * math.tan(math.radians(Vertical_FOV/2))


    h = 145
    theta = 25

    PINHOLE_point = (0,delta,h)
    PINHOLE_point_xy = (0,delta)
    PINHOLE_point_xz = (0,h)
    pixel_list = []
    # X, Y, Z 좌표 계산 -> 원점기준
    pixel_x = Focal_length  # X 좌표는 상수
    for i in range(1,1081):
        pixel_z = (Focal_length * math.tan(math.radians(Vertical_FOV / 2)) -
                        (lens_height / 1080) * 0.5 -
                        (lens_height / 1080) * (i- 1)) + h  # Z 좌표
        for j in range(1,1921):
            pixel_y = (-Focal_length * math.tan(math.radians(Horizontal_FOV / 2)) +
                        (lens_width / 1920) * 0.5 +
                        (lens_width / 1920) * (j - 1)) 
            pixel_list.append([pixel_x, pixel_y, pixel_z])

    pixel_array = np.array(pixel_list)
    print('========기준 array===========')
    print(pixel_array)   
    

    angle_list = []

    for point in pixel_array:
        x,y,z = point
        point_xy = (x,y)
        point_xz = (x,z)
        azimuth_angle = Find_angle(PINHOLE_point_xy, point_xy)  
        elevation_angle = Find_angle(PINHOLE_point_xz, point_xz) 
        angle_list.append([azimuth_angle,elevation_angle])
    
    org_angle_array = np.array(angle_list)
    print('==========original angle array===============')
    print(org_angle_array)
   
    # angle_array[:,0] += pi
    theta_angle_array = org_angle_array[:,1] - theta

    print('======transform theta, pi angle ===========')
    print(theta_angle_array)
    
    # z=0일 때의 점들
    points_on_z0 = []
    
    for angle in org_angle_array:
        azimuth_angle, elevation_angle = angle
        azimuth_angle = math.radians(azimuth_angle)
        elevation_angle = math.radians(elevation_angle)
        
        
        x = -h/math.tan(elevation_angle)
        y = x * math.tan(azimuth_angle) 

        points_on_z0.append([x,y])

    # 결과를 NumPy 배열로 변환
    points_on_z0 = np.array(points_on_z0)
    # rotate pi
    points_on_z0 = rotate_points(points_on_z0, pi)
    # move delta
    points_on_z0[:,1] -= delta
    
    print('=======z=0 array =============')
    print(points_on_z0)




    
    plt.plot(points_on_z0[ : , 0],points_on_z0[ : , 1], marker='o')
    plt.plot(range(0,2500), [131 for i in range(0,2500)])
    plt.plot(range(0,2500), [-131 for i in range(0,2500)])
    
    plt.show()

    # 좌표 비교
    black_white_list = []
    for point in points_on_z0:
        x, y = point
        if ((-150 <= y <= -131) or (131 <= y <= 150)) and x>0 :
            black_white_list.append(1)
        else:
            black_white_list.append(0)

    black_white_array = np.array(black_white_list)
    print('==============black-white array=============')
    print(black_white_array)
  
    # theta = 0 angle_array, theta=25 angle_array 비교
    result = np.where((org_angle_array[:, 0] == theta_angle_array[:, 0]) & 
                  (org_angle_array[:, 1] == theta_angle_array[:, 1]), 1, 0)
    print('============result============')
    print(result)
    result_list = result.tolist()

    # image
    my_point = (0,delta,h)
    print(f"My point{my_point}, pi:{pi}, theta: 25")
  
    image_size = (1920,1080)

    img = Image.new("RGB", image_size, 'black')
    
    x, y = 0, 0
    point_list = []
    for k, l in black_white_list, result_list:
         if y >= 1080:  # y가 이미지 높이를 초과하는지 확인
              break
         if x >= 1920:  # x가 이미지 너비를 초과하는지 확인
               x = 0
               y += 1
        
         if y < 1080:  # y가 유효한 범위인지 확인
            if k == 1 and l ==1 :
                 point_list.append((x, y))
                 img.putpixel((x, y), (255, 255, 255))

         x += 1
    # for k in black_white_list:
    #     if x == 1920:
    #         x = 0
    #         y = y + 1
    #     if k == 1:
    #         point_list.append((x,y))
    #         img.putpixel((x,y), (255,255,255))
    #     x = x + 1
    print(x,y)
    print(len(black_white_list), 1920*1080)
    if len(point_list) != 0:
        print("Find white line")
        return img

    else:
        print("There is not white line")
        return img
  

   

    
    
    
 

output_dir = "/home/vialab/Seonguk/line/lane"
os.makedirs(output_dir, exist_ok=True)

# 1000개의 이미지 생성 및 저장

for i in range(1):
   
   img = make_line_pic(delta = 0, pi = 0)
   delta = 0.0
   img.save(os.path.join(output_dir, f"theta_25test{0}.jpg"))
