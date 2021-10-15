import pygame
import math

# Código Exemplo - Pixel Collider

class Player():
    x = 0
    y = 0

    last_x = 0 
    last_y = 0

    dir_x = 0
    dir_y = 0

    r = 0

class Game():
    '''
        Classe responsável por gerenciar o jogo
    '''
    def __init__(self, screenSize : (int, int), fps=60, title='Game', icon=None):
        '''
            Construtor da Classe Game, possui como parâmetro
                screenSize  ->  tupla contendo de dois valores inteiros (int, int) 
                                que corresponde a largura e altura, ex (800, 600)
                fps         ->  contendo da taxa de atualização da tela
                title       ->  contendo o titulo do jogo
                icon        ->  contendo uma surface (imagem) com o icone a ser exibido na tela
        '''
        # inicializa as variáveis da classe
        self.gameRunning = True
        self.screenSize = screenSize

        self.title = title
        self.icon = icon
        self.fps = fps

        # inicializa o game
        self.initGame()

        self.player = Player()
        self.player.x = self.screenSize[0] / 2
        self.player.y = (self.screenSize[1] / 2) + 70

        self.player.r = 10
        
    def initGame(self):
        '''
            Função responsável por inicializar e configurar a tela do jogo,
            essa função não possui parâmetros
        '''
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption(self.title)

        if(self.icon != None):
            pygame.display.set_icon(self.icon)

        self.gameClock = pygame.time.Clock()

    # função principal do jogo
    def gameMain(self):
        '''
            Loop principal do jogo, essa função não possui parâmetros
        '''
        while self.gameRunning:
            deltaTime = self.gameClock.tick(self.fps)

            for event in pygame.event.get():
                self.gameEvent(event)

            self.gameUpdate(deltaTime)
            self.gameRender()

            pygame.display.update()

        pygame.quit()
        
    # função de eventos
    def gameEvent(self, event):
        '''
            Função responsável por gerenciar os eventos do display
            event -> contém a estrutura do evento (veja a documentação do pygame para mais detalhes)
        '''
        if(event.type == pygame.QUIT):
            self.gameRunning = False
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                self.gameRunning = False

    # função de atualização
    def gameUpdate(self, deltaTime):
        '''
            Função responsável por atualizar a lógica do jogo
            deltaTime -> váriaveis que guarda o tempo que se passou entre dois frames
        '''
        keys = pygame.key.get_pressed()

        # salva a direção que o player está indo
        self.player.dir_x = 0
        self.player.dir_y = 0

        if(keys[pygame.K_d]):
            self.player.dir_x += 1

        if(keys[pygame.K_a]):
            self.player.dir_x -= 1

        if(keys[pygame.K_w]):
            self.player.dir_y -= 1

        if(keys[pygame.K_s]):
            self.player.dir_y += 1


        # normalização do vetor direção
        if(self.player.dir_x != 0 and self.player.dir_y != 0):
            tmp_normal = math.sqrt(math.pow(self.player.dir_x, 2) + math.pow(self.player.dir_y, 2))

            self.player.dir_x = self.player.dir_x / tmp_normal
            self.player.dir_y = self.player.dir_y / tmp_normal



        # pega um pixel de color na direção de movimentação (200% a frente do raio)
        color = self.screen.get_at(
                            (
                                int(self.player.x + self.player.dir_x * self.player.r * 2.0),
                                int(self.player.y + self.player.dir_y * self.player.r * 2.0)
                            ))

        # verifica 200% a frente de se raio se é um pixel proibido!
        # se não for proibido, move o jogador
        # coloquei a cor preta e a vermelha como proibido
        if(color != (0, 0, 0) and color != (255, 0, 0)):
            # salva a ultima coordenada x e y do player
            self.player.last_x = self.player.x
            self.player.last_y = self.player.y

            # atualiza a coordenada x e y do player
            self.player.x += self.player.dir_x
            self.player.y += self.player.dir_y

    # função de renderização
    def gameRender(self):
        '''
            Função responsável por desenhar na tela do jogo
            deltaTime -> váriaveis que guarda o tempo que se passou entre dois frames
        '''

        # OBSERVAÇÂO: É NECESSÁRIO MOVER O FILL PARA ESSE LOCAL (O UPDATE TEM QUE TER A SCREEN DESENHADA PARA VERIFICAR OS PIXELS)
        self.screen.fill((0, 0, 0))

        pygame.draw.rect(self.screen, (255, 255, 255), ((self.screenSize[0] / 2) - 200, (self.screenSize[1] / 2) - 200, 400, 400))

        pygame.draw.rect(self.screen, (255, 0, 0), ((self.screenSize[0] / 2) - 50, (self.screenSize[1] / 2) - 50, 100, 100))

        # desenha uma linha indicando a direção
        pygame.draw.line( 
                            self.screen, 
                            (0, 0, 255), 
                            (self.player.x, self.player.y), 
                            (
                                (self.player.x + self.player.dir_x * self.player.r * 1.5), 
                                (self.player.y + self.player.dir_y * self.player.r * 1.5))
                            )

        # desenha o jogador
        pygame.draw.circle(self.screen, (255, 255, 0), (self.player.x, self.player.y), self.player.r)

game = Game((800, 600), title='Pixel Collider')
game.gameMain()
