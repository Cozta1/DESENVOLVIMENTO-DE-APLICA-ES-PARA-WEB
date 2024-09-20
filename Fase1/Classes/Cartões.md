#fase1 #classe

| cartao           |              |
| ---------------- | ------------ |
| **numeroCartao** | bigint AI PK |
| **numeroConta**  | int          |
| dataExpiracao    | date         |
| cvv              | int          |
FOREIGN KEY (numeroConta) REFERENCES [[Contas]](numeroConta) 