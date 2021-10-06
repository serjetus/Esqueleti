import cv2
import numpy as np

def conectividade(img,pts):
    #transições  de branco para preto, nos pixels que circundam o pixel central precisa ser 1
    cont=0  
    for j in range(1,8,1):
        if(img[pts[j][0]][pts[j][1]]>127 and img[pts[j+1][0]][pts[j+1][1]]<127):
            cont+=1
    
    if(img[pts[8][0]][pts[8][1]]>127 and img[pts[1][0]][pts[1][1]]<127):
        cont+=1
    if(cont == 1):
        return True
    return False


def PixelsPretos(img,pts):
    #numeros de pixels pretos vizinhos >=2 <=6
    cont=0
    for p in range(1,9,1):
        if(img[pts[p][0]][pts[p][1]]<127):
            cont+=1
    if(cont>=2 and cont<=6):
        return True
    return False

def BrancoCima(img,pts):
    #Ao  menos  um  dos  I(i,j+1),  I(i-1,j)  e  I(i,  j-1)  são  fundo
    if(img[pts[1][0]][pts[1][1]]>127 or img[pts[3][0]][pts[3][1]]>127 or img[pts[7][0]][pts[7][1]]>127):
        return True
    return False

def BrancoEsquerda(img,pts):
    #Ao  menos  um  dos  I(i-1,j),  I(i+1,j)  e  I(i,  j-1)  são  fundo
    if(img[pts[1][0]][pts[1][1]]>127 or img[pts[5][0]][pts[5][1]]>127 or img[pts[7][0]][pts[7][1]]>127):
        return True
    return False
    
def BrancoDireita(img,pts):
    #Ao  menos  um  dos  I(i-1,j),  I(i,j+1)  e  I(i+1,  j)  são  fundo
    if(img[pts[1][0]][pts[1][1]] >127 or img[pts[3][0]][pts[3][1]]>127 or img[pts[5][0]][pts[5][1]]>127):
        return True
    return False    


def BrancoInferior(img,pts):
    #Ao  menos  um  dos  I(i,j+1),  I(i+1,j)  e  I(i,  j-1)  são  fundo
    if(img[pts[7][0]][pts[7][1]]>127 or img[pts[5][0]][pts[5][1]]>127 or img[pts[3][0]][pts[3][1]]>127):
        return True
    return False

def PB(img):
    # retorna imagem preto e branco passando uma imagem colorida por parametro 
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    lin, col = img.shape
    img2 = np.zeros((lin,col,1), dtype=np.uint8)
    for i in range(lin):
        for j in range(col):
            if img[i][j] < 200:
                img2[i][j] = 0
            else:
                img2[i][j] = 255

    return img2

def afinador(img):
    linha,coluna,_ = img.shape
    cont=1
    flag = True
    while(cont>0):
        cont=0
        excluidos=[]
        for i in range(1,linha-1,1):
            for j in range(1,coluna-1,1):
                pts = np.zeros((9,2),dtype=int)
                pts[0][0]=i
                pts[0][1]=j
                pts[1][0]=i-1
                pts[1][1]=j
                pts[2][0]=i-1
                pts[2][1]=j+1
                pts[3][0]=i
                pts[3][1]=j+1
                pts[4][0]=i+1
                pts[4][1]=j+1
                pts[5][0]=i+1
                pts[5][1]=j
                pts[6][0]=i+1
                pts[6][1]=j-1
                pts[7][0]=i
                pts[7][1]=j-1
                pts[8][0]=i-1
                pts[8][1]=j-1
                if(img[i][j]<127):  
                    if(conectividade(img,pts) and PixelsPretos(img,pts)):
                        if(flag):
                            if(BrancoCima(img,pts) and BrancoEsquerda(img,pts)):
                                excluidos.append([i,j])
                                cont+=1
                        else:
                            if(BrancoInferior(img,pts) and BrancoDireita(img,pts)):
                                excluidos.append([i,j])
                                cont+=1
        for i in range(len(excluidos)):
            img[excluidos[i][0]][excluidos[i][1]]=255
            flag = not flag
    return img


img= cv2.imread("letraforma.jpg")
imgPreta=PB(img)
cv2.imshow("preta",imgPreta)
cv2.imshow("afinador",afinador(imgPreta))

cv2.waitKey(0)