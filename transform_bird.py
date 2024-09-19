import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def Find_white_point(path):
    img = Image.open(path)
    img_array = np.array(img)
   
    white_point = np.where((img_array[:, :, 0] == 255)  &
                            (img_array[:, :, 1] == 255) &
                            (img_array[:, :, 2] == 255)
                            )
    white_coordinates = list(zip(white_point[0], white_point[1]))

    if not white_coordinates:
        print("There is not White Point")

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
    print(f'x가 가장 작을 때 y의 점: {min_x_point}')
    print(f'x가 가장 클 때 y의 점: {max_x_point}')
       

    # y가 가장 작은 경우
    min_y_index = np.argmin(white_coordinates[:, 0])  # y좌표에서 최소값의 인덱스
    min_y_x_values = white_coordinates[min_y_index, 1]  # 해당 x좌표
    min_y_min = min_y_x_values
    min_y_max = min_y_x_values

    for point in white_coordinates:
        if point[0] == white_coordinates[min_y_index, 0]:  # y가 최소인 경우
            min_y_min = min(min_y_min, point[1])
            min_y_max = max(min_y_max, point[1])

   
    print(f'y가 가장 작을 때 x의 최소: ({min_y_min}, {white_coordinates[min_y_index, 0]}), 최대: ({min_y_max}, {white_coordinates[min_y_index, 0]})')

    p1 = [min_y_min, white_coordinates[min_y_index, 0]] #좌상
    p2 = [min_y_max, white_coordinates[min_y_index, 0]] #우상
    p3 = max_x_point #우하
    p4 = min_x_point #좌하

    return p1, p2, p3, p4
    

path = "C:/Users/monog/line/lane_detection2/theta_25test0.jpg"


p1, p2, p3, p4 = Find_white_point(path)

for i in range(0,1):

    path = f"C:/Users/monog/line/lane_detection2/theta_25test{i}.jpg"

    img = cv.imread(path)

    src_points = np.float32([p1, p2, p3, p4])
    height, width = img.shape[:2]
    dst_points = np.float32([[0, 0],    # 왼쪽 아래 (BL)
                            [width, 0],         # 왼쪽 위 (TL)
                            [width, height],     # 오른쪽 위 (TR)
                            [0, height]]) # 오른쪽 아래 (BR)


    M = cv.getPerspectiveTransform(src_points, dst_points)

    BEV_img = cv.warpPerspective(img, M, (width, height))

    cv.imwrite(f"C:/Users/monog/line/lane_detection2/BEV{i}.jpg", BEV_img)