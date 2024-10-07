import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [contas, setContas] = useState([]);

  useEffect(() => {
    // Fazendo a requisição à API para buscar as contas
    axios.get('http://127.0.0.1:8000/api/contas/')
      .then((response) => {
        setContas(response.data);
      })
      .catch((error) => {
        console.error("Erro ao buscar contas:", error);
      });
  }, []);

  return (
    <div>
      <h1>Lista de Contas</h1>
      {contas.map((conta) => (
        <p key={conta.numeroConta}>
          Cliente: {conta.cliente_nome} - Saldo: R$ {parseFloat(conta.saldo).toFixed(2)}
        </p>
      ))}
    </div>
  );
}

export default App;