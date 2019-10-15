# batalha-naval

## Formatação das mensagens que o servidor deverá receber

Troca de mensagens repassada do Servidor para o Cliente:

    Formato de Arquivo: Dicionário
    
    Chaves do dicionário:
        'message': String com uma mensagem
        'type': Tipo de mensagem
        'code': Ação
        
    Tipos de mensagem:
        'connection': Conexão entre dois jogadores
        'game': Partida em execução
        'end-game': Fim de partida
        'inform': Mensagens de erro, etc.
        
    Tipo de ação:
        0: Não é necessário agir
        1: É necessário agir e responder algo ao servidor 
        
