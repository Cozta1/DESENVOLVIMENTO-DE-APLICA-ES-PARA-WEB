#fase1 #classe

| transacao        |                                                      |
| ---------------- | ---------------------------------------------------- |
| **idTransacao**  | int AI PK                                            |
| **numeroConta**  | int                                                  |
| tipoTransacao    | enum('deposito','saque','transferencia','pagamento') |
| valor            | decimal(10,2)                                        |
| dataHora         | datetime                                             |
| dataAgendamento  | datetime                                             |
| descricao        | varchar(255)                                         |
| status           | enum('pendente','concluida','cancelada')             |
| **contaDestino** | int                                                  |
FOREIGN KEY (numeroConta) REFERENCES [[Contas]](numeroConta),
FOREIGN KEY (contaDestino) REFERENCES [[Contas]](numeroConta)