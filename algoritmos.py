import json

def ships_validation(ships,verbose=False):
    parts_per_type = {
        "type_5":5,
        "type_4":4,
        "type_3":3,
        "type_2":2
    }
    limits = 10
    all_parts = set()
    for type in ships.keys():
        for ship in ships[type]:
            try:
                ship_coords = generate_coordinate(ship['start'],ship['end'])
                if verbose: print('Navio:',ship,'Coord:',ship_coords)

                intersection = sorted(all_parts.intersection(ship_coords))
                if not intersection:
                    all_parts.update(ship_coords)
                else:
                    if verbose: print('Navio ',ship,' do tipo \'',type,'\' possui interceção em: ',intersection,sep='')
                    return False

                if len(ship_coords) != parts_per_type[type]:
                    if verbose: print('Navio ',ship,' do tipo \'',type,'\' não corresponde ao tamanho esperado',sep='')
                    return False
            except:
                if verbose: print('Coordenadas do navio ',ship,' do tipo \'',type,'\' não econtra-se na horizontal ou vertical.',sep='')
                return False

    parts_expected = [(x,y) for y in range(limits) for x in range(limits)]

    if not all_parts.issubset(parts_expected):
        if verbose: print("Coordenadas fora do limite do tabuleiro:",sorted(all_parts.difference(parts_expected)))
        return False
    if verbose:
        print("- Total de peças:",len(all_parts))
        for x in range(10):
            for y in range(10):
                print('0' if (x,y) in all_parts else '-',end=' ')
            print()
    return True
            

def read_ships(name_file='ships.json'):
    return json.loads(open(name_file).read())

def generate_coordinate(pixel_a:tuple,pixel_b:tuple):
    def calc_m(p1:tuple,p2:tuple):
        x1,y1 = p1
        x2,y2 = p2
        delta_x = x2-x1
        delta_y = y2-y1
        return delta_y/delta_x if delta_x!=0 else float('inf')

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
        raise Exception('As coordenadas devem formar uma linha na horizontal ou vertical')

    x1,y1 = p1
    x2,_ = p2

    pixels = set()
    e = m - 0.5 # primeiro valor de 'e'

    pixels.add(p1)
    while x1 < x2-1:
        if e >= 0:
            y1 += 1
            e -= 1
        x1 += 1
        e += m
        pixels.add((x1,y1))
    pixels.add(p2)
    pixels = sorted(pixels)
    _reflexao(pixels,trocaxy,trocax,trocay)
    return pixels