import cv2 as cv

class Camera:
    def __init__(self):
        #Apertura della videocamera di default (indice 0, se si possiedono più videocamere bisogna specificare l'indice)
        self.camera = cv.VideoCapture(0)
        if not self.camera.isOpened():
            raise ValueError("Errore nel riconoscimento della videocamera!")
            
        #Salva larghezza e altezza del frame catturato
        self.width = int(self.camera.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv.CAP_PROP_FRAME_HEIGHT))

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

    def get_frame(self):
        #Restituisce un frame dalla videocamera
        if self.camera.isOpened():
            ret, frame = self.camera.read() 
            if ret:
                #Conversione da BGR (OpenCV) a RGB (uso comune nelle GUI)
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            return (ret, None) 
        return None  
