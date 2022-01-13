import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import os


def CarCamera(car_image):
    plt.style.use('dark_background')

    # Read Input Image
    
    img_ori = cv2.imread(car_image)
    # img_ori = cv2.imread('C:\\data_science202007\\notebook\\data\\1.jpg')

    height, width, channel = img_ori.shape

    hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
    gray = hsv[:,:,2]

    # Adaptive Thresholding

    img_blurred = cv2.GaussianBlur(gray, ksize=(5,5), sigmaX=0)
    #GaussianBlur - noise 처리


    #adaptiveThreshold - img 구분하기 쉽게, 정해진 값 이하는 0으로, 이상은 지정한 maxValue,(255) 로
    # 검은색과 흰색으로 나눠버림
    img_thresh = cv2.adaptiveThreshold(
        img_blurred,
        maxValue=255.0,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )

    #Find Contours
    contours, _ = cv2.findContours(
        img_thresh,
        mode=cv2.RETR_LIST,
        method=cv2.CHAIN_APPROX_SIMPLE
    )

    temp_result = np.zeros((height,width,channel), dtype=np.uint8)
    cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255,255,255))


    #Prepare Data

    temp_result = np.zeros((height,width,channel), dtype=np.uint8)

    contours_dict=[]

    for contour in contours:
        #boudningRect() - 윤곽선을 감싸는 사각형을 구한다.
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(temp_result, pt1=(x,y),pt2=(x+w,y+h),color=(255,255,255),thickness=2)
        
        #insert to dict
        contours_dict.append({
            'contour':contour,
            'x':x,
            'y':y,
            'w':w,
            'h':h,
            'cx':x+(w/2),
            'cy':y+(h/2)
        })

    # Select Candidates by Char Size
    # 번호판 숫자의 후보들을 정해줌
    # 번호판 크기 80, 번호판 너비,높이 2 / 8 , 가로,세로 비율 0.25/1.0
    MIN_AREA=80
    MIN_WIDTH, MIN_HEIGHT= 2,8
    MIN_RATIO,MAX_RATIO=0.25, 1.0

    possible_contours=[]

    cnt=0

    for d in contours_dict:
        area = d['w'] * d['h']
        ratio = d['w'] / d['h']
        
        if area > MIN_AREA \
        and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
        and MIN_RATIO < ratio < MAX_RATIO:
            d['idx'] = cnt
            cnt += 1
            possible_contours.append(d)
            
    # visualize possible contours
    temp_result = np.zeros((height,width,channel), dtype=np.uint8)

    for d in possible_contours:
        cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'],d['y']+d['h']), color=(255,255,255), thickness=2)


    # Select Candidates by Arrangement of Contours

    # 값 조정해줄수 있음 (번호판으로 인식할 contour들의 조건 설정)
    # 첫번째 contour와 다음 contour의 대각선의 중심간의 거리가 첫번째 contour의 대각선길이의 5배 안에 있어야한다.
    MAX_DIAG_MULTIPLYER = 5
    # 첫번쨰 contour와 다음 contour의 중심을 이었을때 생기는 직각삼각형의 angle(theta)의 최대값 (너무벌어져있으면 후보군에 들지않아!)
    MAX_ANGLE_DIFF = 12.0
    MAX_AREA_DIFF = 0.5
    MAX_WIDTH_DIFF = 0.8
    MAX_HEIGHT_DIFF = 0.2
    MIN_N_MATCHED = 3 # 위의 조건을 만족하는 contour의 최소 개수가 3개이상이어야만 번호판으로 인정

    # Recursive(재귀)함수로 계속 찾을거
    def find_chars(contour_list):
        matched_result_idx=[]
        
        # contour d1
        for d1 in contour_list:
            matched_contours_idx = []
            
            # contour d2
            for d2 in contour_list:
                # contour d1 과 contour d2가 같은 index면 같은 contour이기 때문에 continue
                if d1['idx'] == d2['idx']:
                    continue
                    
                dx = abs(d1['cx'] - d2['cx'])
                dy = abs(d1['cy'] - d2['cy'])
                
                diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)

                distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
                if dx == 0:
                    angle_diff = 90
                else:
                    angle_diff = np.degrees(np.arctan(dy / dx))
                    
                area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
                width_diff = abs(d1['w'] - d2['w']) / d1['w']
                height_diff = abs(d1['h'] - d2['h']) / d1['h']

                if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
                and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                    matched_contours_idx.append(d2['idx'])
            
            # append this contour
            matched_contours_idx.append(d1['idx'])

            if len(matched_contours_idx) < MIN_N_MATCHED:
                continue

            matched_result_idx.append(matched_contours_idx)

            unmatched_contour_idx = []
            for d4 in contour_list:
                if d4['idx'] not in matched_contours_idx:
                    unmatched_contour_idx.append(d4['idx'])

            unmatched_contour = np.take(possible_contours, unmatched_contour_idx)
            
            # recursive
            recursive_contour_list = find_chars(unmatched_contour)
            
            for idx in recursive_contour_list:
                matched_result_idx.append(idx)

            break

        return matched_result_idx
        
    result_idx = find_chars(possible_contours)

    matched_result = []
    for idx_list in result_idx:
        matched_result.append(np.take(possible_contours, idx_list))


    # visualize possible contours
    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    for r in matched_result:
        for d in r:
    #         cv2.drawContours(temp_result, d['contour'], -1, (255, 255, 255))
            cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255, 255, 255), thickness=2)


    # Rotate Plate Images
    PLATE_WIDTH_PADDING = 1.3 # 1.3
    PLATE_HEIGHT_PADDING = 1.5 # 1.5
    MIN_PLATE_RATIO = 3
    MAX_PLATE_RATIO = 10

    plate_imgs = []
    plate_infos = []

    for i, matched_chars in enumerate(matched_result):
        sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])

        plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2
        plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2
        
        plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING
        
        sum_height = 0
        for d in sorted_chars:
            sum_height += d['h']

        plate_height = int(sum_height / len(sorted_chars) * PLATE_HEIGHT_PADDING)
        
        triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
        triangle_hypotenus = np.linalg.norm(
            np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) - 
            np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
        )
        
        angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenus))
        
        rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)
        
        img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(width, height))
        
        img_cropped = cv2.getRectSubPix(
            img_rotated, 
            patchSize=(int(plate_width), int(plate_height)), 
            center=(int(plate_cx), int(plate_cy))
        )
        
        if img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO or img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO > MAX_PLATE_RATIO:
            continue
        
        plate_imgs.append(img_cropped)
        plate_infos.append({
            'x': int(plate_cx - plate_width / 2),
            'y': int(plate_cy - plate_height / 2),
            'w': int(plate_width),
            'h': int(plate_height)
        })

    # Another Thresholding to Find Chars

    longest_idx, longest_text = -1, 0
    plate_chars = []

    for i, plate_img in enumerate(plate_imgs):
        plate_img = cv2.resize(plate_img, dsize=(0, 0), fx=1.6, fy=1.6)
        _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # find contours again (same as above)
        contours, _ = cv2.findContours(plate_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        
        plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
        plate_max_x, plate_max_y = 0, 0

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            area = w * h
            ratio = w / h

            if area > MIN_AREA \
            and w > MIN_WIDTH and h > MIN_HEIGHT \
            and MIN_RATIO < ratio < MAX_RATIO:
                if x < plate_min_x:
                    plate_min_x = x
                if y < plate_min_y:
                    plate_min_y = y
                if x + w > plate_max_x:
                    plate_max_x = x + w
                if y + h > plate_max_y:
                    plate_max_y = y + h
                    
        img_result = plate_img[plate_min_y:plate_max_y, plate_min_x:plate_max_x]
        
        img_result = cv2.GaussianBlur(img_result, ksize=(3, 3), sigmaX=0)
        _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # copyMakeBorder - 약간의 검은색의 여백을 줌 (pytesseract가 잘 인식하도록)
        img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT, value=(0,0,0))
        
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        
        # psm 7 - 이미지가 한 줄로 있다, oem 0 - 0번 engine을 쓰겠다.
        chars = pytesseract.image_to_string(img_result, lang='kor', config='--psm 7 --oem 0')
        
        
        result_chars = ''
        has_digit = False
        for c in chars:
            if ord('가') <= ord(c) <= ord('힣') or c.isdigit():
                if c.isdigit():
                    has_digit = True
                result_chars += c
        
        # print(result_chars)
        plate_chars.append(result_chars)

        if has_digit and len(result_chars) > longest_text:
            longest_idx = i


    # Result

    info = plate_infos[longest_idx]
    chars = plate_chars[longest_idx]

    return chars

# print(chars)

# img_out = img_ori.copy()

# cv2.rectangle(img_out, pt1=(info['x'],info['y']), pt2=(info['x']+info['w'], info['y']+info['h']), color=(255,0,0),
#             thickness=2)


# # 저장위치가 어디?
# cv2.imwrite( chars + '.jpg', img_out)
