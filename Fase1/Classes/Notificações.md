#fase1 #classe

| notificacao       |                                             |
| ----------------- | ------------------------------------------- |
| **idNotificacao** | int AI PK                                   |
| **idCliente**     | int                                         |
| tipoNotificacao   | enum('transacao','seguranca','informativo') |
| mensagem          | text                                        |
| dataEnvio         | datetime                                    |

FOREIGN KEY (idCliente) REFERENCES [[Clientes]](idCliente) 