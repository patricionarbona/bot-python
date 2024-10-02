import cv2

img = cv2.imread('./demos/ejemplo1.png')

roi = cv2.selectROI("Seleccione el ROI", img)

img_crop = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

cv2.imshow("ROI Seleccionado", img_crop)
cv2.waitKey(0)
cv2.destroyAllWindows()