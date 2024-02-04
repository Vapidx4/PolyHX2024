import cv2
from pyzbar.pyzbar import decode

# https://www.geeksforgeeks.org/how-to-make-a-barcode-reader-in-python/

def readBarcode(image):

    try:
        img = cv2.imread(image)
        barcode = decode(img)
    except Exception as e:
        print(f"Error: {e}")
        barcode = ""

    if (not barcode):
        return
    else:
        for barcode in barcode:
            (x,y,w,h) = barcode.rect

            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10), 
                          (255, 0, 0), 2)
            
            if (barcode.data != ""):
                barcodeCode = barcode.data.decode("utf-8")
                barcodeType = barcode.type

    return [barcodeCode, barcodeType]