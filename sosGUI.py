from lib import *


def get_image(name):
    """
    Chercher l'image dans le PATH indiqué
    en fonction du nom de l'image en paramètre
    :param name: nom de l'image (str)
    :return:
    """
    return "image\\" + name


def caseToPixel(num, default=0.0):
    """
    Convertir les coordoonées des cases en pixel
    :param num: numéro de la case (int)
    :param default: (int)
    """
    return math.floor(num * 43 + 22 + default)


def displayTextePlayer(texte, points, firstColor, secondColor, thirdColor, fX, fY, sX, sY, player):
    textePlayer = pygame.font.Font(POLICE, 48).render(texte, True, COLOR[firstColor], COLOR[secondColor])
    ecran.blit(textePlayer, (LONGUEUR * fX, HAUTEUR * fY))
    scorePlayer = pygame.font.Font(POLICE, 70).render(str(points[player]), True, COLOR[thirdColor], COLOR[secondColor])
    ecran.blit(scorePlayer, (LONGUEUR * sX, HAUTEUR * sY))


def displayScore(maxPlayers, points):
    """
    Afficher les joueurs et le score des joueurs
    :param maxPlayers: nombre de joueurs max (int)
    :param points: tableau des scores (int)
    :param player: joueur actuel (int)
    """
    if maxPlayers == 2:
        displayTextePlayer("Player1", points, 8, 3, 0, 0.1, 0.05, 0.15, 0.4, 0)
        displayTextePlayer("Player2", points, 8, 6, 1, 0.8, 0.05, 0.85, 0.4, 1)
    if maxPlayers > 2:
        displayTextePlayer("Player1", points, 8, 3, 0, 0.05, 0.05, 0.2, 0.05, 0)
        displayTextePlayer("Player2", points, 8, 6, 1, 0.85, 0.05, 0.8, 0.05, 1)
        displayTextePlayer("Player3", points, 8, 3, 2, 0.05, 0.3, 0.2, 0.3, 2)
        if maxPlayers > 3:
            displayTextePlayer("Player4", points, 8, 6, 3, 0.85, 0.3, 0.8, 0.3, 3)
            if maxPlayers > 4:
                displayTextePlayer("Player5", points, 8, 3, 4, 0.05, 0.6, 0.2, 0.6, 4)
                if maxPlayers > 5:
                    displayTextePlayer("Player6", points, 8, 6, 5, 0.85, 0.6, 0.8, 0.6, 5)


def displayPlayer(ecran, player):
    """
    Afficher le tour du jo ueur
    :param ecran: fenêtre créée
    :param player: joueur actuel (int)
    """
    if player == 0:
        textePlayer = pygame.font.Font(POLICE, 25).render("Player's turn 1", True, COLOR[6], COLOR[3])
        ecran.blit(textePlayer, (LONGUEUR * 0.1, HAUTEUR * 0.2))
    elif player == 1:
        textePlayer = pygame.font.Font(POLICE, 25).render("Player's turn 2", True, COLOR[3], COLOR[6])
        ecran.blit(textePlayer, (LONGUEUR * 0.8, HAUTEUR * 0.2))
    elif player == 2:
        textePlayer = pygame.font.Font(POLICE, 25).render("Player's turn 3", True, COLOR[6], COLOR[3])
        ecran.blit(textePlayer, (LONGUEUR * 0.1, HAUTEUR * 0.4))
    elif player == 3:
        textePlayer = pygame.font.Font(POLICE, 25).render("Player's turn 4", True, COLOR[3], COLOR[6])
        ecran.blit(textePlayer, (LONGUEUR * 0.8, HAUTEUR * 0.4))
    elif player == 4:
        textePlayer = pygame.font.Font(POLICE, 25).render("Player's turn 5", True, COLOR[6], COLOR[3])
        ecran.blit(textePlayer, (LONGUEUR * 0.1, HAUTEUR * 0.7))
    elif player == 5:
        textePlayer = pygame.font.Font(POLICE, 25).render("Player's turn 6", True, COLOR[3], COLOR[6])
        ecran.blit(textePlayer, (LONGUEUR * 0.8, HAUTEUR * 0.7))


def drawCell(ecran, tableau, x, y, absc, ordo):
    """
    Afficher la case et la valeur qu'elle contient (Graphiquement)
    :param ecran: fenêtre créée
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param x: abscisse de la case (int)
    :param y: ordonnée de la case (int)
    :param absc: abscisse de la case en pixel (int)
    :param ordo: ordonnée de la case en pixel (int)
    """
    case = pygame.image.load(get_image("case.png"))  # On affiche le tableau
    if tableau[x][y] == 1:
        value = pygame.font.Font(POLICE, 20).render("S", True, COLOR[8], COLOR[7])
    elif tableau[x][y] == 2:
        value = pygame.font.Font(POLICE, 20).render("O", True, COLOR[8], COLOR[7])
    else:
        value = pygame.font.Font(POLICE, 20).render(".", True, COLOR[8], COLOR[7])
    ecran.blit(case, (absc, ordo))
    ecran.blit(value, (absc + 20, ordo + 15))


def drawBoard(ecran, tableau, default):
    """
    Afficher/Dessiner le tableau avec les valeurs (Graphiquement)
    :param ecran: fenêtre créée
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param default: (int)
    """
    absc = default[0]
    ordo = default[1]
    for y in range(len(tableau)):
        for x in range(len(tableau)):
            drawCell(ecran, tableau, x, y, absc, ordo)
            absc += 43
        ordo += 43
        absc = default[0]


def drawLines(ecran, lines, mot, default, player, saveLine):
    """
    :param ecran: fenêtre créée
    :param lines: tableau à 2 dimensions des lignes d'alignement (int)
    :param mot: varible indiquant un alignement (bool)
    :param default: (int)
    :param player: joueur actuel (int)
    :param saveLine: tableau à 2 dimensions des lignes d'alignement (int)
    """
    x = 0
    for line in lines:
        if type(line) == list and len(line) != 0:
            if mot:
                while len(saveLine[x]) != 0:
                    x += 1
                saveLine[x] = [(caseToPixel(line[0][0], default[0]), caseToPixel(line[0][1], default[1]), player),
                               (caseToPixel(line[1][0], default[0]), caseToPixel(line[1][1], default[1]), player)]

    for line in saveLine:
        if type(line) == list and len(line) != 0:
            pygame.draw.line(ecran, COLOR[line[0][2]], (line[0][0], line[0][1]), (line[1][0], line[1][1]), EPAISSEUR)

    for line in lines:
        line[:] = []
    return lines


def rules(ecran):
    """
    Afficher les règles de jeu
    :param ecran: fenêtre créée
    """
    go = False
    while not go:
        print("rules")
        ecran.blit(pygame.image.load(get_image("regles.png")), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                go = True


def displayWinner(scores, maxPlayers):
    """
    Afficher le résulat de la partie
    Proposer différentes solutions ( Rejouer, Menu)
    :param scores: tableau des scores (int)
    :param maxPlayers: nombre maximal de joueurs (int)
    """
    tmp = 0
    print("winner")
    for i in range(maxPlayers):
        if scores[i] > tmp:
            tmp = scores[i]
    if scores.count(tmp) > 1:
        win = "Egalite"
    else:
        win = "Winner " + str((scores.index(tmp)) + 1)
    result = pygame.font.Font(
        POLICE, 30).render(str(win), True, COLOR[7], COLOR[8])
    ecran.blit(result, (LONGUEUR * 0.47, 20))
    ecran.blit(pygame.image.load(get_image("home.png")), (LONGUEUR * 0.84, HAUTEUR * 0.863))
    ecran.blit(pygame.image.load(get_image("replay.png")), (LONGUEUR * 0.8, HAUTEUR * 0.85))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONUP:
                posX, posY = event.pos
                if 734 < posY < 784:
                    if 1160 < posX < 1210:
                        return True
                    if 1218 < posX < 1268:
                        return False


def menu(surface):
    """
    Afficher menu
    Choisir mode de jeu
    :param surface: fenêtre créée
    """
    choice = pygame.image.load(get_image('menu1.PNG'))
    surface.blit(choice, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == MOUSEBUTTONUP:
                if 1214 < event.pos[0] < 1411:
                    if 74 < event.pos[1] < 126:
                        return 1
                    if 264 < event.pos[1] < 309:
                        return 3
                    if 172 < event.pos[1] < 215:
                        return 2
                    if 340 < event.pos[1] < 385:
                        return 4


def nbJoueurs(ecran):
    """
    Sélectionner le nombre de joueurs
    :param ecran: fenêtre créée
    """
    while True:
        ecran.blit(pygame.image.load(get_image("joueurs.png")), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONUP:
                posX, posY = event.pos
                if 395 < posY < 475:
                    if 265 < posX < 445:
                        return 3
                    if 635 < posX < 815:
                        return 4
                    if 1030 < posX < 1210:
                        return 5
                if 615 < posY < 695:
                    if 635 < posX < 815:
                        return 6


pygame.init()
ecran = pygame.display.set_mode((LONGUEUR, HAUTEUR))
pygame.display.set_caption("SOS Game")
pygame.display.set_icon(pygame.image.load(get_image("icon.png")))
