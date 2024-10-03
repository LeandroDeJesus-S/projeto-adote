function get_data_cities (state){

}

var valorEstadoGlobal
const inputEstado = document.getElementById('estado');
inputEstado.addEventListener('input', function() {
    const valorEstado = inputEstado.value;
    valorEstadoGlobal = valorEstado;
    console.log(valorEstado); // Exibe o valor do campo "estado" no console
    
    const url = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${valorEstadoGlobal}/municipios`;

    // Use a API Fetch para fazer uma solicitação GET para a URL da API
    fetch(url)
    .then(response => response.json())
    .then(data => {
        document.getElementById('cidade').innerHTML = '';
        const cities = [];
        const selectCities = document.createElement('select');

        for (let i = 0; i < data.length; i++) {
            cities.push(data[i].nome);
            let optionCities = document.createElement('option');
            optionCities.setAttribute('id', data[i].nome);
            optionCities.setAttribute('value', data[i].nome);
            optionCities.textContent = data[i].nome;
            document.getElementById('cidade').appendChild(optionCities);
            cities.push(data[i].nome);
            console.log(data[i].nome);
        }
        
    })
    .catch(error => {
        // Trate o erro aqui
        console.error(error);
    });
});

var hiddenInputEstado = document.createElement('input');
hiddenInputEstado.setAttribute('type', 'hidden');
hiddenInputEstado.setAttribute('value', valorEstadoGlobal)
