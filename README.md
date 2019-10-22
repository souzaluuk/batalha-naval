## Utilização do programa

### Execução do servidor
```bash
[batalha-naval]$ python server.py
```

### Execução dos clientes
```bash
[batalha-naval]$ python client.py
```

#### Observações
- O endereço `IP` padrão do servidor é em `127.0.0.1` (localhost);
- Se o cliente for executado em uma máquina remota, deve-se, no arquivo [client.py](client.py), informar o `IP` da máquina do servidor;
- Um arquivo modelo ([ships.json](ships.json)) indica a disposição do tabuleiro de cada jogador, caso queira customizar novas disposições você pode editá-lo diretamente ou criar uma customização e substituir o padrãono arquivo [client.py](client.py).
- As instruções de jogo se darão na execução do mesmo;
- O tabuleiro possui as dimensões `10x10`.