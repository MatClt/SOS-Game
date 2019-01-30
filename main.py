from sosAlgorithms import*

while True:
    choix = menu(ecran) # On affiche le menu et on renvoie le choix du mode
    if choix == 1:
        board = new_Board(ecran) # On crée le tableau
        SOS(1, 2, board)
    if choix == 2:
        board = new_Board(ecran) # On crée le tableau
        SOS(1, nbJoueurs(ecran), board)
    if choix == 3:
        board = new_Board(ecran) # On crée le tableau
        SOS(0, 2, board)
    if choix == 4: # On veut reprendre la dernière partie jouée
        if download() != -1: # Si l'ouverture du fichier réussi
            mode, maxPlayers, players, scores, saveLine, tableau, nbTours = download()
            SOS(mode, maxPlayers, tableau, nbTours, players, saveLine, scores)
