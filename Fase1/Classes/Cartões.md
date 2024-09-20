#fase1 #classe

| cartao           |              |
| ---------------- | ------------ |
| **numeroCartao** | bigint AI PK |
| **numeroConta**  | int          |
| dataExpiracao    | date         |
| cvv              | int          |
| bandeira         | varchar(40)  |
FOREIGN KEY (numeroConta) REFERENCES [[Contas]](numeroConta) 