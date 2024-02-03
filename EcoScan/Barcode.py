import cv2
from pyzbar.pyzbar import decode

# https://www.geeksforgeeks.org/how-to-make-a-barcode-reader-in-python/

def readBarcode(image):
    img = cv2.imread(image)
    barcodes = decode(img)

    if (not barcodes):
        print("The barcode couldn't be read")
    else:
        for barcode in barcodes:
            (x,y,w,h) = barcode.rect

            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10), 
                          (255, 0, 0), 2)
            
            if barcode.data != "":
                print(barcode.data)
                print(barcode.type)

    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image="barcode2.jpg"
    readBarcode(image)
