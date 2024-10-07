import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [contas, setContas] = useState([]); // Estado para armazenar as contas
    const [error, setError] = useState(null); // Estado para armazenar erros

    useEffect(() => {
        // Função para buscar as contas
        const fetchContas = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/contas/');
                setContas(response.data); // Atualiza o estado com os dados recebidos
            } catch (err) {
                setError(err.message); // Armazena a mensagem de erro se houver
            }
        };

        fetchContas(); // Chama a função para buscar as contas
    }, []); // O array vazio indica que o efeito roda apenas uma vez, como componentDidMount

    return (
        <div>
            <h1>Contas</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>} {/* Exibe mensagem de erro se houver */}
            <ul>
                {contas.map(conta => (
                    <li key={conta.numeroConta}>
                        {conta.cliente.nome} - Saldo: {conta.saldo}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
