#jogo palavra secreta

#jogo de adivinhação sobre palavra secreta, onde 
#da pra jogar sozinho ou com várias pessoas no terminal.
import os
import random

class Jogador: #classe jogadores e seus atributos
    def __init__(self, nome, palavra_secreta, dica):
        self.nome = nome
        self.palavra_secreta = palavra_secreta
        self.dica = dica
        self.tentativas = len(palavra_secreta) + 3
        self.adivinhadas = set()
        self.tentativas_usadas = 0
        self.pontos = 0

class JogoPalavraSecreta: #lista de palavras e suas dicas associadas
    def __init__(self):
        self.library = [
            ('melancia', 'Fruta grande e verde por fora, vermelha por dentro'),
            ('computador', 'Máquina usada para processar informações'),
            ('python', 'Linguagem de programação popular'),
            ('tamarindo', 'Fruta tropical usada em sucos e doces'),
            ('otorrinolaringologista', 'Médico especialista em ouvido, nariz e garganta'),
            ('paralelepipedo', 'Bloco de pedra usado em pavimentação'),
            ('samambaia', 'Tipo de planta com folhas longas e finas'),
            ('teclado', 'Dispositivo usado para digitar em um computador'),
            ('brasil', 'País na América do Sul'),
            ('macaco', 'Animal primata que vive em árvores'),
            ('argentina', 'País vizinho ao Brasil'),
            ('baleia', 'Grande mamífero marinho'),
            ('ornitorrinco', 'Animal que põe ovos e tem bico de pato'),
            ('banana', 'Fruta amarela e curva'),
            ('maracuja', 'Fruta tropical usada em sucos e sobremesas'),
            ('china', 'País mais populoso do mundo'),
            ('orquidea', 'Tipo de flor ornamental'),
            ('videogame', 'Dispositivo usado para jogar jogos eletrônicos'),
            ('professor', 'Pessoa que ensina em escolas e universidades'),
            ('carteiro', 'Pessoa que entrega cartas e pacotes')
        ]
        self.players = {} #dicionário que armazena os jogadores e suas palavras secretas.
        self.tentativas_por_jogador = {}#Dicionário que armazena o número de tentativas usadas por 
        #cada jogador para adivinhar as palavras dos outros jogadores.

    def limpar(self): #função de limpar o sistema dependendo do sistema operacional
        os.system('cls' if os.name == 'nt' else 'clear')

    def word_display(self, word, guess):#Mostra as letras adivinhadas na palavra secreta, 
        #substituindo as letras não adivinhadas por asteriscos.
        return " ".join([letter if letter in guess else "*" for letter in word])

    def validate_word(self, word): #valida se a palavra contém apenas letras.
        return word.isalpha()

    def calcular_pontos(self, tentativas_usadas): #função para calcular pontos dos jogadores
        return max(0, 10 - tentativas_usadas) * 10  #pontuação baseada apenas nas tentativas usadas

    def adivinhar_palavra(self, player, secret_word, dica):#Função principal para adivinhar a palavra secreta. 
        #Pode ser usada tanto para um jogador quanto para múltiplos jogadores
        jogador = self.players[player]
        tries = len(secret_word) + 3
        guess = set()
        tries2 = 0
        while tries > 0:
            print(f'{player} adivinhe a palavra secreta!')
            print('Palavra:', self.word_display(secret_word, guess))
            print('Tentativas restantes:', tries)
            print('Letras já adivinhadas:', ' '.join(sorted(guess)))
            print('Dica:', dica)

            letter = input('Adivinhe uma letra ou a palavra completa: \n').lower()

            if len(letter) > 1:
                if letter == secret_word:
                    self.limpar()
                    pontos = self.calcular_pontos(tries2)
                    jogador.pontos += pontos
                    print(f'\nParabéns! Jogador {player} adivinhou a palavra secreta em {tries2} tentativas e ganhou {pontos} pontos.')
                    self.tentativas_por_jogador[(player, secret_word)] = tries2
                    return True
                else:
                    tries -= 1
                    tries2 += 1
                    print('Que pena! A palavra completa está incorreta.')
            elif letter in guess:
                tries2 += 1
                print('Você já adivinhou essa letra. Tente outra!')
            elif letter in secret_word:
                guess.add(letter)
                tries2 += 1
                print(f'Boa tentativa! A letra {letter} está na palavra.')
            else:
                guess.add(letter)
                tries -= 1
                tries2 += 1
                print(f'Que pena! A letra {letter} não está na palavra.')

            if all(letter in guess for letter in secret_word):
                self.limpar()
                pontos = self.calcular_pontos(tries2)
                jogador.pontos += pontos
                print(f'\nParabéns! Jogador {player} adivinhou a palavra secreta em {tries2} tentativas e ganhou {pontos} pontos.')
                self.tentativas_por_jogador[(player, secret_word)] = tries2
                return True
        return False

    def game_start(self): #inicia o jogo, configurando os jogadores e suas palavras secretas.
        print('Jogador(es) bem-vindos ao jogo Palavra Secreta! \n')
        while True:
            try:#gera uma exceçao, se caso ocorra, a execuçao do cod
            #dentro do try é interrompida e é passado para o except
                num_players = int(input('Quantos jogadores irão participar? \n'))
                if num_players <= 0:
                    raise ValueError('O número de jogadores deve ser positivo.')#valueError valida se números digitados são positivos
            #raise é usado para sinalizar que aconteceu um erro no cod e
            #fornecer a informaçao do erro
                break
            except ValueError as e: #O ValueError é uma exceção em Python que é levantada quando uma função 
            #recebe um argumento com o tipo correto, mas com um valor inadequado.
                print(e)

        if num_players == 1:
            player = input('\nJogador 1, digite seu nome: ').lower()
            secret_word, dica = random.choice(self.library) #escolha aleatória da lista de palavras da livraria
            self.players[player] = Jogador(player, secret_word, dica)
            print(f'\n{player}, sua palavra secreta foi escolhida aleatoriamente.')
            self.adivinhar_palavra(player, secret_word, dica)
        else:
            for i in range(1, num_players + 1):
                player = input(f'\nJogador {i}, digite seu nome: ').lower()
                while True:
                    secret_word = input(f'\n{player}, digite sua palavra secreta: ').lower()
                    dica = input(f'\n{player}, digite uma dica para a palavra secreta: ').lower()
                    if self.validate_word(secret_word):
                        break
                    else:
                        print('A palavra secreta deve conter apenas letras.')
                self.players[player] = Jogador(player, secret_word, dica)
                self.limpar()
            all_guessed = True
            for player_now in self.players.keys():
                for challenger_name in self.players.keys():
                    if player_now != challenger_name:
                        secret_word, dica = self.players[challenger_name].palavra_secreta, self.players[challenger_name].dica
                        print(f'\nÉ a vez de {player_now} adivinhar a palavra secreta de {challenger_name}!')
                        guessed = self.adivinhar_palavra(player_now, secret_word, dica)
                        if not guessed:
                            all_guessed = False

            if not all_guessed:
                print('\nQue pena! Todos os jogadores perderam. As palavras secretas eram:')
                for player in self.players.values():
                    print(f"{player.nome}: {player.palavra_secreta}")

            print('\nTentativas usadas por cada jogador:') #mostra em quantas tentativas cada jogador acertou a palavra
            for (player_now, secret_word), tries2 in self.tentativas_por_jogador.items():
                print(f'{player_now} adivinhou a palavra {secret_word} em {tries2} tentativas.')

            print('\nPontuação final:') #mostra a pontuação final de cada jogador
            for player in self.players.values():
                print(f'{player.nome}: {player.pontos} pontos')

        self.jogar_novamente()

    def jogar_novamente(self): #Pergunta aos jogadores se eles querem jogar novamente 
        #e reinicia o jogo se a resposta for "sim".
        while True:
            resposta = input('\nDeseja jogar novamente? (s/n): ').lower()
            if resposta == 's':
                self.players = {}
                self.tentativas_por_jogador = {}
                self.game_start()
                break
            elif resposta == 'n':
                print('Obrigado por jogar! Até a próxima.')
                exit()
            else:
                print('Resposta inválida. Digite "s" para sim ou "n" para não.')

if __name__ == "__main__":
    #criação da instância do jogo e do inicio do jogo
    jogo = JogoPalavraSecreta()
    jogo.game_start()




