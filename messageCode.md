ToServer:

1: {
  message: "Ainda não há oponentes para você!"
  action: Espera um oponente
}

2: {
  message: f"Você tem um oponente: {oponent['username']}"
  params: username do oponent, vez (true ou false)
  action: Se preparar para jogar ou esperar sua vez. 
}

#O servidor pode enviar o nome do oponente uma vez e daí só reutilizar.

3: {
  message: f"{oponent['username']} saiu da partida."}
  action: Avisar que a partida será descontinuada e finalizar o programa.
}

4: {
  message: f"Você acertou um navio {oponent['ships']['type']}
  params: tipo do navio (quantas peças tem)
  action: isMyTurn = True para que o usuário possa jogar.
}

5: {
  message: f"{oponent['username']} acertou um navio {ships['type']}. Aguarde mais uma jogada."
  params: tipo do navio (quantas peças tem)
  action: isMyTurn permanece falso e o usuário aguarda mais uma jogada.
} 

6: {
  message: "Água! Você errou seu tiro!"
  action: isMyTurn permanece falso e o usuário aguarda mais uma jogada.
}

7: {
  message: f"{oponent['username']} atirou na água."
  action: isMyTurn = True para que o usuário possa jogar.
}

8: {
  message: f"Você derrubou o navio {ships['type']}.
  params: tipo do navio (quantas peças tem)
  action: isMyTurn = True para que o usuário possa jogar.
}

9: {
  message: f"{oponent['username']} derrubou o seu navio {ships['type']}.
  params: tipo do navio (quantas peças tem)
  action: isMyTurn permanece falso e o usuário aguarda mais uma jogada.
}

10: {
  message: f"Você derrubou todos os navios de {oponent['username']}. Parabéns! Você venceu!"
  action: Finalizar o programa.
}

11: {
  message: f"{oponent['username']} derrubou todos os seus navios. Infelizmente, você perdeu!"
  action: Finalizar o programa.
}