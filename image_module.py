import sys, subprocess, cv2
from PIL import Image, ImageDraw
import numpy as np


# def image_find(target_image : Image, image_to_find : Image):
#     # if (len(sys.argv) > 2):
#     #    print (sys.argv[1], sys.argv[2])
#     #    target_image = sys.argv[1]
#     #    image_to_find = sys.argv[2]
#     # else:
#     #    print ('Specify target image, followed by the image to search for.')
#     #    print ('Example: search-image.py target_image.png image_to_find.png [markfile.png]')
#     #    sys.exit()
#     #
#     # Example 1:
#     # search-image.py examples\100-orig.png examples\menu_hamburger.png
#     #
#     # Example 2:
#     # copy examples\100-orig.png marked_result.png
#     # search-image.py examples\100-orig.png examples\menu_hamburger.png marked_result.png
#
#     #print ('\nSTEP 1: Load images and get dimensions - y,x')
#     # target_image
#
#     im = np.array(target_image)
#     tmp = np.array(image_to_find)
#
#     #image_size = cv2.GetSize(im)
#     #template_size = cv2.GetSize(tmp)
#     image_size = im.shape[:2]
#     template_size = tmp.shape[:2]
#
#     print ('image_size (y,x)', image_size)
#     print ('template_size (y,x)', template_size)
#     #print ('DEBUG:image_size is of type', type(image_size))
#
#     #print ('\nSTEP 2: Calculate result_size')
#
#     #result_size = [ s[0] - s[1] + 1 for s in zip(image_size, template_size) ]
#     #result_size = [ result_size[1], result_size[0] ] # reverse values to change y,x to x,y
#
#     #print ('DEBUG:result_size - x,y', result_size)
#
#     #print ('\nSTEP 3: Use Computer Vision to create a result image of the desired result_size')
#
#     #result = cv2.CreateImage(result_size, cv2.IPL_DEPTH_32F, 1)
#     #result = np.zeros((result_size[0], result_size[1], 3), np.uint8)
#     #print ('DEBUG:result', result)
#
#
#     #CV_TM_SQDIFF is the match method, smaller min_val means better match. min_loc is the best match location
#     #with other matching methods you need to look at max_val and max_loc
#     #http://opencv.itseez.com/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
#     #http://docs.opencv.org/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
#
#
#     #print ('\nSTEP 4: Match Tempalte')
#
#     #cv2.MatchTemplate(im, tmp, result, cv2.CV_TM_SQDIFF)
#     result = cv2.matchTemplate(im, tmp, cv2.TM_SQDIFF)
#
#     #print ('DEBUG:result', result)
#
#
#     #print ('\nSTEP 5: Get the Min Max Loc')
#
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#
#     #print ('\n')
#
#     #print ('result', result)
#     print ('min_val', min_val)
#     print ('max_val', max_val)
#     print ('min_loc', min_loc, 'X')
#     print ('max_loc', max_loc)
#
#     confidence = (9999999999 - min_val) / 100000000
#     print ('primary confidence', '%.2f %%' % confidence)
#
#     altconfidence = 100 - ((min_val / max_val)*100)
#     print ('alternate confidence', '%.2f %%' % altconfidence)
#
#     topleftx = min_loc[0]
#     toplefty = min_loc[1]
#     sizex = template_size[1]
#     sizey = template_size[0]
#
#     if (altconfidence > 99) or ((confidence > 97) and (altconfidence > 93)) or ((confidence > 95.7) and (altconfidence > 96.3)):
#        print ('The image of size', template_size, '(y,x) was found at', min_loc)
#        # if (len(sys.argv) > 3):
#        #    print ('Marking', sys.argv[3], 'with a red rectangle')
#        #    marked = Image.open(sys.argv[3])
#        #    draw = ImageDraw.Draw(marked)
#        #    draw.line(((topleftx,         toplefty),         (topleftx + sizex, toplefty)),           fill="red", width=2)
#        #    draw.line(((topleftx + sizex, toplefty),         (topleftx + sizex, toplefty + sizey)),   fill="red", width=2)
#        #    draw.line(((topleftx + sizex, toplefty + sizey), (topleftx,         toplefty + sizey)),   fill="red", width=2)
#        #    draw.line(((topleftx,         toplefty + sizey), (topleftx,         toplefty)),           fill="red", width=2)
#        #    del draw
#        #    marked.save(sys.argv[3], "PNG")
#     else:
#        print ('The image was not found')
#
#     return min_loc




#정확도를 반환. 반환이 안되는 경우가 없음.
def confidence_by_image_search(target_image: np.ndarray, image_to_find: np.ndarray, name1="기본", name2=""):
    try:
        # Image.fromarray(target_image).show()
        # Image.fromarray(image_to_find).show()
        image_size = target_image.shape[:2]
        template_size = image_to_find.shape[:2]

        print ('image_size (y,x)', image_size)
        print ('template_size (y,x)', template_size)

        result = cv2.matchTemplate(target_image, image_to_find, cv2.TM_SQDIFF)
        (min_val, max_val, minloc, maxloc) = cv2.minMaxLoc(result)

        altconfidence = 100 - ((min_val / max_val) * 100)
        print(name1, name2, "의 altconfidence:", altconfidence)
        return altconfidence
    except Exception as ex:
        print(name1, "에서", ex)
        return -1


#카운트 개수만큼의 모든 이미지 찾은 위치 좌측상단 위치를 리스트로 반환하는 함수. 카운트 개수만큼 못찾으면 에러생성
def image_multi_search(source_image: Image, find_image: Image, find_count: int):
    # source_image.show()
    # find_image.show()
    im = np.array(source_image)
    tmp = np.array(find_image)

    template_size = tmp.shape[:2]

    #조금 느리지만 안정적인 방법. 정확한 Count도 반환가능하고
    result = 0
    find_list = []
    for idx in range(find_count):
        result = cv2.matchTemplate(im, tmp, cv2.TM_SQDIFF)
        (min_val, max_val, minloc, maxloc) = cv2.minMaxLoc(result)
        altconfidence = 100 - ((min_val / max_val) * 100)
        if altconfidence < 96:
            raise Exception("image_multi_search: 이미지 못찾음", idx, altconfidence)
        x1, y1 = minloc[0], minloc[1]
        x2, y2 = minloc[0] + template_size[1], minloc[1] + template_size[0]

        find_list.append([x1, y1])
        im[y1:y2, x1:x2] = 0

    # 빠른 방법이지만 불완전함.
    # result2 = np.reshape(result, result.shape[0] * result.shape[1])
    # sort = np.argsort(result2)
    # find_list = []
    # for idx in range(find_count):
    #     y1, x1 = np.unravel_index(sort[idx], result.shape)  # best match
    #     find_list.append([x1, y1])

    # sorted(find_list, key=lambda k: [k[1], k[0]])
    # y축 좌표를 통한 간접정렬
    #TODO 정렬 기법 체크
    find_list = np.array(find_list)
    ind = np.lexsort((find_list[:, 1], find_list[:, 0]))
    find_list = find_list[ind]

    # print(find_list)
    # print(sort)
    # image2.show()
    return find_list


#np.ndarray타입에서 임계값을 넘은 최적 이미지를 찾아서 !!!우측!!! 상단 위치를 튜플로 반환, 못찾을 경우 -1 반환.
def image_np_search_correct(target_image: np.ndarray, image_to_find: np.ndarray, accurancy: int = 99):
    image_size = target_image.shape[:2]
    template_size = image_to_find.shape[:2]

    # print ('image_size (y,x)', image_size)
    # print ('template_size (y,x)', template_size)

    result = cv2.matchTemplate(target_image, image_to_find, cv2.TM_SQDIFF)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #
    # print ('min_val', min_val)
    # print ('max_val', max_val)
    # print ('min_loc', min_loc, 'X')
    # print ('max_loc', max_loc)

    rightx = min_loc[0] + template_size[1]
    topy = min_loc[1]


    confidence = (9999999999 - min_val) / 100000000
    # print ('primary confidence', '%.2f %%' % confidence)

    altconfidence = 100 - ((min_val / max_val)*100)
    print('image_np_search_correct: alternate confidence', '%.2f %%' % altconfidence)

    if (altconfidence > accurancy) or ((confidence > 97) and (altconfidence > 93)) or ((confidence > 95.7) and (altconfidence > 96.3)):
        # print ('The image of size', template_size, '(y,x) was found at', min_loc)
        return rightx, topy
    else:
        print('///image_serch_correct: 해당 이미지 못찾음///')
        return -1, -1


#완벽하게 거의 완전히 이미지가 서칭되는 경우 그 영역을 반환
def image_match_area_search(target_image: np.ndarray, image_to_find: np.ndarray):
    result = cv2.matchTemplate(target_image, image_to_find, cv2.TM_SQDIFF)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    find_image_sizes = image_to_find.shape[:2]
    find_image_x_len = find_image_sizes[1]
    find_image_y_len = find_image_sizes[0]

    x2 = min_loc[0] + find_image_x_len
    y2 = min_loc[1] + find_image_y_len

    # print("x2, y2", x2, y2)
    # print("min_loc", min_loc)

    confidence = (9999999999 - min_val) / 100000000

    altconfidence = 100 - ((min_val / max_val) * 100)
    print("altconfidence:", altconfidence)
    if altconfidence > 99:
        # print ('The image of size', template_size, '(y,x) was found at', min_loc)
        return (min_loc[0], min_loc[1], x2, y2)
    else:
        return False


#이미지가 거의 완전히 같은 것을 찾으면 True를 반환
def is_image_exist(target_image: np.ndarray, image_to_find: np.ndarray):
    # Image.fromarray(target_image).show()
    # Image.fromarray(image_to_find).show()

    result = cv2.matchTemplate(target_image, image_to_find, cv2.TM_SQDIFF)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    confidence = (9999999999 - min_val) / 100000000
    # print ('primary confidence', '%.2f %%' % confidence)

    altconfidence = 100 - ((min_val / max_val) * 100)
    print('is_image_exist: ', altconfidence)

    if altconfidence > 99:
        # print('primary confidence', '%.2f %%' % confidence)
        # print('alternate confidence', '%.2f %%' % altconfidence)
        # Image.fromarray(target_image).show()
        # Image.fromarray(image_to_find).show()

        # print ('The image of size', template_size, '(y,x) was found at', min_loc)
        return True
    else:
        return False



