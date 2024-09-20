#fase1 #classe

| conta           |                             |
| --------------- | --------------------------- |
| **numeroConta** | int AI PK                   |
| **idCliente**   | int                         |
| **idAgencia**   | int                         |
| tipoConta       | enum('corrente','poupanca') |
| saldo           | decimal(10,2)               |
| limiteCredito   | decimal(10,2)               |
| saldoDisponivel | decimal(10,2)               |
| dataAbertura    | date                        |

FOREIGN KEY (idCliente) REFERENCES [[Clientes]](idCliente),
FOREIGN KEY (idAgencia) REFERENCES [[Agências]](idAgencia)

