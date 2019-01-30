from sosGUI import *


def download():
    """
    Charger les données d'une partie sauvegardée contenu dans un fichier Json
    """
    try:
        # On tente d'ouvrir et de charger les données de jeu
        fichier = open("texte.json", "r")
        nbTours = int(fichier.readline())
        mode = int(fichier.readline())
        maxPlayers = int(fichier.readline())
        joueur = int(fichier.readline())
        scores = json.loads(fichier.readline())
        saveLine = json.loads(fichier.readline())
        tableau = json.loads(fichier.readline())
        fichier.close()
        return mode, maxPlayers, joueur, scores, saveLine, tableau, nbTours
    except:
        # Echec de la lecture du fichier
        return -1


def saveGame(maxPlayers, player, scores, saveLine, tab, mode, nbTours):
    """
    Sauvegarder la partie
    :param maxPlayers: nombre de joueurs max (int)
    :param player: joueur actuel (int)
    :param scores: tableau des scores (int)
    :param saveLine: tableau à 2 dimensions des lignes d'alignement (int)
    :param tab: tableau de jeu à 2 dimensions (int)
    :param mode: mode de jeu (int)
    :param nbTours: nombre de tours (int)
    """
    # On sauvegarde de manière ordonnée les données dans un fichier
    fichier = open('texte.json', "w")
    fichier.write(str(nbTours))
    fichier.write("\n")
    fichier.write(str(mode))
    fichier.write("\n")
    fichier.write(str(maxPlayers))
    fichier.write("\n")
    fichier.write(str(player))
    fichier.write("\n")
    fichier.write(json.dumps(scores))
    fichier.write("\n")
    fichier.write(json.dumps(saveLine))
    fichier.write("\n")
    fichier.write(json.dumps(tab))
    fichier.close()


def PixelToCase(nbPix, default=0.0):
    """
    Convertir les pixels en numéro de case
    :param nbPix: Coordonnées en pixel (int)
    :param default: Indique l'endroit de départ (int)
    """
    return math.floor((nbPix - default) // 43)


def inversePlayer(player, maxPlayers):
    """
    Changer le tour du joueur
    :param player: joueur actuel (int)
    :param maxPlayers: nombre maximum de joueurs (int)
    """
    if player == maxPlayers - 1:
        return 0
    player += 1
    return player


def new_Board(ecran):
    """
    Créer le tableau (non-graphique) de jeu
    qui va contenir les données("lettres")
    et que nous pourrons utiliser
    :param ecran: Fenêtre créée
    :return:
    """
    menu_dimension = pygame.image.load(get_image("dimension.png"))
    pygame.transform.scale(menu_dimension, (LONGUEUR, HAUTEUR))
    ecran.blit(menu_dimension, (0, 0))
    pygame.display.update()
    dimension = 0
    while dimension == 0:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == MOUSEBUTTONUP:
                posX, posY = event.pos
                if 330 < posY < 410:
                    if 510 < posX < 685:
                        dimension = 3
                    if 730 < posX < 910:
                        dimension = 4
                    if 950 < posX < 1130:
                        dimension = 5
                    if 1170 < posX < 1355:
                        dimension = 6
                if 495 < posY < 570:
                    if 65 < posX < 245:
                        dimension = 7
                    if 285 < posX < 495:
                        dimension = 8
                    if 510 < posX < 685:
                        dimension = 9
                    if 730 < posX < 910:
                        dimension = 10
                    if 950 < posX < 1130:
                        dimension = 11
                    if 1170 < posX < 1355:
                        dimension = 12
                if 655 < posY < 740:
                    if 625 < posX < 735:
                        dimension = 13
    tableau = [[0] * dimension for i in range(dimension)]
    return tableau


def display(ecran, tableau, points, mot, lines, player, maxPlayers, default, saveLine=[[] * 0 for i in range(0)]):
    """
    Afficher l'interface graphique (scores, joueurs, plateau de jeu, boutons,...)
    :param ecran: fenêtre créée
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param points: tableau des scores (int)
    :param mot: variable indiquant un alignement (bool)
    :param lines: tableau à 2 dimensions des lignes d'alignement (int)
    :param player: joueur actuel (int)
    :param maxPlayers: nombre maximal de joueurs (int)
    :param default: (int)
    :param saveLine: tableau à 2 dimensions des lignes d'alignement (int)
    """
    pygame.draw.rect(ecran, COLOR[3], (0, 0, LONGUEUR // 2, HAUTEUR))  # On dessine les 2 zones de couleur
    pygame.draw.rect(ecran, COLOR[6], (LONGUEUR // 2, 0, LONGUEUR, HAUTEUR))

    logo = pygame.image.load(get_image("logo.PNG"))  # On affiche le Logo
    ecran.blit(logo, (LONGUEUR * 0.35, HAUTEUR * 0.78))

    ecran.blit(pygame.image.load(get_image("help.png")), (LONGUEUR * 0.9, HAUTEUR * 0.895))

    save = pygame.font.Font(POLICE, 25).render("Save Game", True, COLOR[8], COLOR[6])
    ecran.blit(save, (LONGUEUR * 0.05, HAUTEUR * 0.9))

    save = pygame.font.Font(POLICE, 25).render("Back", True, COLOR[8], COLOR[6])
    ecran.blit(save, (LONGUEUR * 0.05, HAUTEUR * 0.85))

    drawBoard(ecran, tableau, default)
    displayScore(maxPlayers, points)
    lines = drawLines(ecran, lines, mot, default, player, saveLine)
    displayPlayer(ecran, player)

    pygame.display.update()
    return lines


def selectSquare(tableau, default, points, mot, lines, player, maxPlayers, nbTours, saveLine, mode=1):
    """
    Sélectionner une case, un bouton
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param default: (int)
    :param points: tableau des scores (int)
    :param mot: variable indiquant un alignement (bool)
    :param lines: tableau à 2 dimensions des lignes d'alignement (int)
    :param player: joueur actuel (int)
    :param maxPlayers: nombre maximal de joueurs (int)
    :param nbTours: nombre de tours (int)
    :param saveLine: tableau à 2 dimensions des lignes d'alignement (int)
    :param mode: indique le mode (int)
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == MOUSEBUTTONDOWN:
                if 70 < event.pos[0] < 330:
                    if 735 < event.pos[1] < 760:
                        saveGame(maxPlayers, player, points, saveLine, tableau, mode, nbTours)
                        return -1, -1, -1
                if 70 < event.pos[0] < 130:
                    if 690 < event.pos[1] < 720:
                        return -1, -1, -1
                if 1305 < event.pos[0] < 1355:
                    if 734 < event.pos[1] < 784:
                        rules(ecran)
                        display(ecran, tableau, points, mot, lines, player, maxPlayers, default, saveLine)
                typeOfMouse = pygame.mouse.get_pressed()
                if possibleSquare(tableau, event.pos[0], event.pos[1], default):
                    return PixelToCase(event.pos[0], default[0]), PixelToCase(event.pos[1], default[1]), typeOfMouse


def possibleSquare(tableau, posX, posY, default):
    """
    Vérifier que les coordonnées de la case choisie
    sont valides
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param posX: abscisse du clique (int)
    :param posY: ordonnée du clique (int)
    :param default: (int)
    """
    if default[0] < posX < default[0] + 43 * len(tableau):
        if default[1] < posY < default[1] + 43 * len(tableau):
            if tableau[PixelToCase(posX, default[0])][PixelToCase(posY, default[1])] == 0:
                return True
    return False


def update(tableau, x, y, joueur, points, lines, nbMot, maxPlayers, choice):
    """
    Vérifier les possibles alignements,
    inverser les joueurs
    et mettre a jour le tableau de jeu
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param x: abscisse de la case (int)
    :param y: ordonnée de la case (int)
    :param points: tableau des scores (int)
    :param joueur: joueur actuel (int)
    :param lines: tableau à 2 dimensions des lignes d'alignement (int)
    :param nbMot: variable indiquant un alignement (bool)
    :param maxPlayers: nombre de joueurs maximum (int)
    :param choice: tableau indiquant le type de clique réalisé (int)
    """
    if choice[0]:  # Si clique droit, alors valeur S
        tableau[x][y] = 1
        points, nbMot, lines = updateScoreS(tableau, x, y, points, joueur, lines)
    elif choice[2]:  # Si clique gauche alors valeur O
        tableau[x][y] = 2
        points, nbMot, lines = updateScoreO(tableau, x, y, points, joueur, lines)
    if not nbMot:
        joueur = inversePlayer(joueur, maxPlayers)
    return tableau, points, joueur, nbMot, lines


def updateScoreO(tableau, x, y, points, joueur, lines):
    """Vérifier les divers alignements possible
    en partant de la lettre "O" que l'utilisateur a posé
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param x: abscisse de la case (int)
    :param y: ordonnée de la case (int)
    :param points: tableau des scores (int)
    :param joueur: joueur actuel (int)
    :param lines: tableau à 2 dimensions des lignes d'alignement (int)
    """
    # On vérifie SOS en diagonale (on cherche les 2 S autour de O)
    nbSegment = 0
    check = False
    if x - 1 >= 0 and y - 1 >= 0 and tableau[x - 1][y - 1] == 1:  # On vérifie si on a SOS en diagonale
        if x + 1 < len(tableau) and y + 1 < len(tableau) and tableau[x + 1][y + 1] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x - 1, y - 1), (x + 1, y + 1)]
            nbSegment += 1
            check = True
            print("O diagonale")
    if x + 1 < len(tableau) and y - 1 >= 0 and tableau[x + 1][y - 1] == 1:  # On vérifie si on a SOS en diagonale
        if x - 1 >= 0 and y + 1 < len(tableau) and tableau[x - 1][y + 1] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x + 1, y - 1), (x - 1, y + 1)]
            nbSegment += 1
            check = True
            print("O diagonale")
    if y - 1 >= 0 and tableau[x][y - 1] == 1:  # On vérifie si on a SOS en verticale
        if y + 1 < len(tableau) and tableau[x][y + 1] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y - 1), (x, y + 1)]
            nbSegment += 1
            check = True
            print("O verticale")
    if x + 1 < len(tableau) and tableau[x + 1][y] == 1:  # On vérifie si on a SOS en horizontale
        if x - 1 >= 0 and tableau[x - 1][y] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x + 1, y), (x - 1, y)]
            nbSegment += 1
            check = True
            print("O horizontale")
    return points, check, lines


def updateScoreS(tableau, x, y, points, joueur, lines):
    """
    Vérifier les divers alignements possible
    en partant de la lettre "S" que l'utilisateur a posé
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param x: abscisse de la case (int)
    :param y: ordonnée de la case (int)
    :param points: tableau des scores (int)
    :param joueur: joueur actuel (int)
    :param lines: tableau à 2 dimensions des lignes d'alignement (int)
    """
    nbSegment = 0
    check = False
    if x - 1 >= 0 and y - 1 >= 0 and tableau[x - 1][y - 1] == 2:
        if x - 2 >= 0 and y - 2 >= 0 and tableau[x - 2][y - 2] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y), (x - 2, y - 2)]
            nbSegment += 1
            check = True
            print("S diagonale haut gauche")
    if x + 1 < len(tableau) and y - 1 >= 0 and tableau[x + 1][y - 1] == 2:
        if x + 2 < len(tableau) and y - 2 >= 0 and tableau[x + 2][y - 2] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y), (x + 2, y - 2)]
            nbSegment += 1
            check = True
            print("S diagonale haut droite")
    if x - 1 >= 0 and y + 1 < len(tableau) and tableau[x - 1][y + 1] == 2:
        if x - 2 >= 0 and y + 2 < len(tableau) and tableau[x - 2][y + 2] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y), (x - 2, y + 2)]
            nbSegment += 1
            check = True
            print("S diagonale bas gauche")
    if x + 1 < len(tableau) and y + 1 < len(tableau) and tableau[x + 1][y + 1] == 2:
        if x + 2 < len(tableau) and y + 2 < len(tableau) and tableau[x + 2][y + 2] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y), (x + 2, y + 2)]
            nbSegment += 1
            check = True
            print("S diagonale bas droite")
    if y - 1 >= 0 and tableau[x][y - 1] == 2:
        if y - 2 >= 0 and tableau[x][y - 2] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y), (x, y - 2)]
            nbSegment += 1
            check = True
            print("S verticale haut")
    if y + 1 < len(tableau) and tableau[x][y + 1] == 2:
        if y + 2 < len(tableau) and tableau[x][y + 2] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y), (x, y + 2)]
            nbSegment += 1
            check = True
            print("S verticale bas")
    if x + 1 < len(tableau) and tableau[x + 1][y] == 2:
        if x + 2 < len(tableau) and tableau[x + 2][y] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y), (x + 2, y)]
            nbSegment += 1
            check = True
            print("S horizontale droite")
    if x - 1 >= 0 and tableau[x - 1][y] == 2:
        if x - 2 >= 0 and tableau[x - 2][y] == 1:
            points[joueur] += 1
            lines[nbSegment] = [(x, y), (x - 2, y)]
            nbSegment += 1
            check = True
            print("S horizontale gauche")
    return points, check, lines


def selectSquareIA(tableau):
    """
    Sélectionner une case pour l'IA
    :param tableau: tableau de jeu à 2 dimensions (int)
    """
    lettre = random.randint(0, 1)
    if lettre == 1:
        typeOfMouse = (1, 0, 0)
    elif lettre == 0:
        typeOfMouse = (0, 0, 1)
    while True:
        x = random.randint(0, len(tableau) - 1)
        y = random.randint(0, len(tableau) - 1)
        if possibleSquareIA(tableau, x, y):
            return x, y, typeOfMouse


def possibleSquareIA(tableau, x, y):
    """
    Vérifier si la case choisie est disponible
    :param tableau: tableau de jeu à 2 dimensions (int)
    :param x: abscisse de la case (int)
    :param y: ordonnée de la case (int)
    """
    if tableau[x][y] == 0:
        return True
    return False


def SOS(mode, maxPlayers, board, nbTours=0, player=0, saveLine=[], scores=[]):
    """
    Gérer une partie complète
    :param mode: indique le mode (int)
    :param maxPlayers: nombre de joueurs maximum (int)
    :param board: tableau de jeu à 2 dimensions (int)
    :param nbTours: nombre de tours (int)
    :param player: joueur actuel (int)
    :param saveLine: tableau à 2 dimensions des lignes d'alignement (int)
    :param scores: tableau des scores (int)
    :return:
    """
    default = [(LONGUEUR * 0.5) - (44 * (len(board) / 2)), HAUTEUR * 0.1]
    winner = 0
    while True:
        if len(scores) == 0:
            nbTours, player, scores, saveLine = 0, 0, [0] * maxPlayers, [[] * 2 for i in range(200)]
        elif winner == 1:
            board = new_Board(ecran)
            nbTours, winner, player, scores, saveLine = 0, 0, 0, [0] * maxPlayers, [[] * 2 for i in range(200)]
        mot = False
        lines = [[] * 2 for i in range(8)]
        while nbTours != len(board) * len(board):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit(0)
            lines = display(ecran, board, scores, mot, lines, player, maxPlayers, default, saveLine)
            if mode == 0 and player == 1:
                i, j, typeMouse = selectSquareIA(board)
            else:
                i, j, typeMouse = selectSquare(board, default, scores, mot, lines, player, maxPlayers, nbTours,
                                               saveLine)
                if i == -1 and j == -1 and typeMouse == -1:
                    return
            board, scores, player, mot, lines = update(board, i, j, player, scores, lines, mot, maxPlayers, typeMouse)
            lines = display(ecran, board, scores, mot, lines, player, maxPlayers, default, saveLine)
            nbTours += 1
        if not displayWinner(scores, maxPlayers):
            break
        winner = 1
