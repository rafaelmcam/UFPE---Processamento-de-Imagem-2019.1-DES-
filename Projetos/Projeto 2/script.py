# Nome: Rafael Mendes Campello
# Disciplina: Processamento de Imagem 2019.1 - DES

#python3 script.py "nome_do_vídeo"

import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import glob

class InPaint_Video():
    def __init__(self, videoName, resizeVideo = True):
        self.videoName = videoName
        self.resizeVideo = resizeVideo

        firstFrame = self.getFirstFrame()

        if self.check_exist() == False:
            self.painter(firstFrame)

        self.videoInPainted()

        return

    def painter(self, frame):
        global ix,iy,drawing,mode, mode2
        global ix2, iy2, erasing

        mask = np.zeros(frame.shape, dtype = np.uint8)

        drawing = False # true if mouse is pressed
        mode = True # write/erase
        mode2 = True # circle or ret
        
        ix,iy = -1,-1
        ix2, iy2 = -1, -1

        img_copy = frame.copy()

        # mouse callback function
        def draw_circle(event,x,y,flags,param):
            global ix,iy,drawing,mode, mode2
            global ix2, iy2, erasing

            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                ix,iy = x,y

            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing == True:
                    if mode == True:
                        #cv2.rectangle(img_copy,(ix,iy),(x,y),(255,255,255),-1)
                        if mode2 == True:
                            cv2.rectangle(mask,(ix,iy),(x,y),(255,255,255),-1)
                        else:
                            cv2.circle(mask, (x, y), 3, (255, 255, 255), -1)
                    else:
                        #cv2.circle(img_copy,(x,y),5,(255,255,255),-1)
                        if mode2 == True:
                            cv2.rectangle(mask,(ix,iy),(x,y),(0,0,0),-1)
                        else:
                            cv2.circle(mask, (x, y), 3, (0, 0, 0), -1)


            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                if mode2 == True:
                    if mode == True:
                        cv2.rectangle(mask,(ix,iy),(x,y),(255,255,255),-1)
                    else:
                        cv2.rectangle(mask,(ix,iy),(x,y),(0,0,0),-1)
                        #cv2.circle(img,(x,y),5,(0,0,255),-1)
                else:
                    if mode == True:
                        cv2.circle(mask,(x,y), 3, (255,255,255),-1)
                    else:
                        cv2.circle(mask,(x,y), 3,(0,0,0),-1)


        #img = np.zeros((512,512,3), np.uint8)
        #img = img_copy
        cv2.namedWindow("Pressiona as teclas \"m\" e \"n\" para alternar entre os modos.")
        cv2.setMouseCallback("Pressiona as teclas \"m\" e \"n\" para alternar entre os modos.",draw_circle)

        while(1):
            img = frame.copy()
            img = cv2.add(img, mask)


            cv2.putText(img, "Pressiona as teclas \"m\" e \"n\" para alternar entre os modos.".format(mode), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(img, "Mask/Erase: {}".format(mode), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(img, "Retangle/Circle: {}".format(mode2), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)


            cv2.imshow("Pressiona as teclas \"m\" e \"n\" para alternar entre os modos.", img)
        
            k = cv2.waitKey(1) & 0xFF
            if k == ord('m'):
                mode = not mode
            if k == ord('n'):
                mode2 = not mode2
            elif k == 27:
                break

        cv2.destroyAllWindows()
        
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        plt.imshow(mask)
        cv2.imwrite("Masks/mask_{}.png".format(self.videoName.split(".")[0]), mask)
        self.mask = mask

        return



    def check_exist(self):
        self.already_exists = [file.split("/")[-1] for file in glob.glob("Masks/*")]
        check = "mask_{}.png".format(self.videoName.split(".")[0])
        bol = False
        #self.bol = False
        if check in self.already_exists:
            print("Já Existe: ", check)
            print("Pular para vídeo.")
            bol = True
            self.mask = cv2.imread("Masks/mask_{}.png".format(self.videoName.split(".")[0]), 0)
        return bol


    def getFirstFrame(self):

        cap = cv2.VideoCapture(self.videoName)
        ret, frame = cap.read()

        if self.resizeVideo:
            frame = cv2.resize(frame, (600, 400))
        return frame

    def videoInPainted(self):
        cap = cv2.VideoCapture(self.videoName)

        mode = True
        mask = self.mask
        while(1):
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.resize(frame, (600, 400))
    
                inpainted = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)

                cv2.putText(frame, "Pressiona a tecla \"i\" para ativar/desativa InPaint.".format(mode), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(inpainted, "Pressiona a tecla \"i\" para ativar/desativa InPaint.".format(mode), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

                cv2.putText(frame, "Ativado: {}".format(mode), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(inpainted, "Ativado: {}".format(mode), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                
                
                # cv2.imshow('image', frame)
                # cv2.imshow('inpainted', inpainted)
                
                if mode == True:
                    cv2.imshow("Pressione a tecla i para alternar a versão InPainted e Original.", inpainted)
                else:
                    cv2.imshow("Pressione a tecla i para alternar a versão InPainted e Original.", frame)
                
                k = cv2.waitKey(1) & 0xFF
                if k == ord('i'):
                    mode = not mode
                elif k == 27:
                    break
    
        cv2.destroyAllWindows()
        return 


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='InPaint Vídeo.')
    parser.add_argument("v", metavar = "videoName", help = "Video Name")

    args = parser.parse_args() 
    
    c = InPaint_Video(args.v, True)