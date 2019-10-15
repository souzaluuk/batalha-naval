import json

def read_ships(name_file='ships.json'):
    return json.loads(open(name_file).read())

def generate_coordinate(pixel_a:tuple,pixel_b:tuple):
    def calc_m(p1:tuple,p2:tuple):
        x1,y1 = p1
        x2,y2 = p2
        delta_x = x2-x1
        delta_y = y2-y1
        return delta_y/delta_x if delta_x!=0 else delta_y

    def reflexao(p1:tuple,p2:tuple):
        trocaxy = trocax = trocay = False
        valor_m = calc_m(p1,p2) # coeficiente angular

        x1,y1 = p1
        x2,y2 = p2

        if  valor_m > 1 or valor_m < -1:
            x1,y1 = y1,x1
            x2,y2 = y2,x2
            trocaxy = True # ativa flag de troca para xy
        if x1 > x2:
            x1 = -x1 # inverte x de p1
            x2 = -x2 # inverte x de p2
            trocax = True # ativa flag de troca para x
        if y1 > y2:
            y1 = -y1 # inverte y de p1
            y2 = -y2 # inverte y de p2
            trocay = True # ativa flag de troca para y
        return (x1,y1),(x2,y2),trocaxy,trocax,trocay

    def _reflexao(lista_pixels,trocaxy,trocax,trocay):
        for i in range(len(lista_pixels)): # troca para os pixels da lista
            x,y = lista_pixels[i]
            if trocay:
                y = -y
            if trocax:
                x = -x
            if trocaxy:
                x,y = y,x
            lista_pixels[i] = (x,y)
        trocay = trocax = trocaxy = False

    p1,p2,trocaxy,trocax,trocay = reflexao(pixel_a,pixel_b) # retorna reflexão com flags

    m = calc_m(p1,p2) # guarda o cálculo de (x2-x1)/(y2-y1)

    if m != 0:
        raise Exception('As coordenadas não são válidas')

    x1,y1 = p1
    x2,_ = p2

    pixels = list() # lista de pixels que será retornada
    e = m - 0.5 # primeiro valor de 'e'

    pixels.append(p1)
    while x1 < x2-1:
        if e >= 0:
            y1 += 1
            e -= 1
        x1 += 1
        e += m
        pixels.append((x1,y1))
    pixels.append(p2)
    _reflexao(pixels,trocaxy,trocax,trocay)
    return pixels