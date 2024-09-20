#fase1 #classe

| extrato         |              |
| --------------- | ------------ |
| **idExtrato**   | int AI PK    |
| **idCliente**   | int          |
| **numeroConta** | int          |
| acao            | varchar(255) |
| dataHora        | datetime     |
| detalhes        | text         |

FOREIGN KEY (idCliente) REFERENCES [[Clientes]](idCliente),
FOREIGN KEY (numeroConta) REFERENCES [[Contas]](numeroConta)