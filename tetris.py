import pygame
import random
import sys


# === Configurações ===
LARGURA, ALTURA = 300, 600
TAMANHO = 30
COLUNAS = LARGURA // TAMANHO
LINHAS = ALTURA // TAMANHO
FPS = 5

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CORES = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),   # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

# Peças (Tetrominos)
TETROMINOS = {
    "I": [[1, 1, 1, 1]],
    "J": [[1, 0, 0],
          [1, 1, 1]],
    "L": [[0, 0, 1],
          [1, 1, 1]],
    "O": [[1, 1],
          [1, 1]],
    "S": [[0, 1, 1],
          [1, 1, 0]],
    "T": [[0, 1, 0],
          [1, 1, 1]],
    "Z": [[1, 1, 0],
          [0, 1, 1]]
}


# === Classe do jogo ===
class Tetris:
    def __init__(self):
        self.tabuleiro = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]
        self.peca = self.nova_peca()
        self.x = COLUNAS // 2 - len(self.peca[0]) // 2
        self.y = 0
        self.pontos = 0

    def nova_peca(self):
        nome, forma = random.choice(list(TETROMINOS.items()))
        cor = CORES[list(TETROMINOS.keys()).index(nome)]
        return [[(celula * (CORES.index(cor)+1)) for celula in linha] for linha in forma]

    def mover(self, dx, dy):
        if not self.colisao(self.x + dx, self.y + dy, self.peca):
            self.x += dx
            self.y += dy
        elif dy:  # Se não puder descer mais
            self.fixar()

    def colisao(self, x, y, peca):
        for i, linha in enumerate(peca):
            for j, valor in enumerate(linha):
                if valor:
                    if j + x < 0 or j + x >= COLUNAS or i + y >= LINHAS:
                        return True
                    if self.tabuleiro[i + y][j + x]:
                        return True
        return False

    def fixar(self):
        for i, linha in enumerate(self.peca):
            for j, valor in enumerate(linha):
                if valor:
                    self.tabuleiro[i + self.y][j + self.x] = valor
        self.limpar_linhas()
        self.peca = self.nova_peca()
        self.x = COLUNAS // 2 - len(self.peca[0]) // 2
        self.y = 0
        if self.colisao(self.x, self.y, self.peca):
            print(f"Gamme over! Pontos: {self.pontos}")
            pygame.quit()
            sys.exit()

    def limpar_linhas(self):
        linhas_removidas = 0
        nova_grade = []
        for linha in self.tabuleiro:
            if all(linha):
                linhas_removidas += 1
            else:
                nova_grade.append(linha)
        for _ in range(linhas_removidas):
            nova_grade.insert(0, [0 for _ in range(COLUNAS)])
        self.tabuleiro = nova_grade
        self.pontos += linhas_removidas * 100
        if linhas_removidas > 0:
            pygame.mixer.Sound("sons/linha.wav").play()  # Toca som

    def girar(self):
        peca_rotacionada = list(zip(*self.peca[::-1]))
        peca_rotacionada = [list(linha) for linha in peca_rotacionada]
        if not self.colisao(self.x, self.y, peca_rotacionada):
            self.peca = peca_rotacionada

    def desenhar(self, tela, fonte):
        tela.fill(PRETO)
        # Tabuleiro
        for i in range(LINHAS):
            for j in range(COLUNAS):
                if self.tabuleiro[i][j]:
                    pygame.draw.rect(tela, CORES[self.tabuleiro[i][j] - 1],
                 (j * TAMANHO, i * TAMANHO, TAMANHO, TAMANHO))
        # Peça Atual
        for i, linha in enumerate(self.peca):
            for j, valor in enumerate(linha):
                if valor:
                    pygame.draw.rect(tela, CORES[valor-1],
                                     ((self.x+j)*TAMANHO, (self.y+i)*TAMANHO, TAMANHO, TAMANHO))

        # Pontos
        texto = fonte.render(f"Pontos: {self.pontos}", True, BRANCO)
        tela.blit(texto, (10, 10))


#  === Loop Principal ===


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("🎮 Tetris")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("consolas", 25)
    jogo = Tetris()

    pygame.mixer.music.load("sons/musica.wav")
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jogo.mover(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    jogo.mover(1, 0)
                elif event.key == pygame.K_DOWN:
                    jogo.mover(0, 1)
                elif event.key == pygame.K_UP:
                    jogo.girar()

        jogo.mover(0, 1)  # cair automaticamente
        jogo.desenhar(tela, fonte)

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
