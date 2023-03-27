
function updateCidades() {
    // Obtém o valor selecionado no primeiro <select>
        const estado = document.getElementById("estados").value;
        const = new Request('https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado}/municipios', {'method': 'GET'});
        for (var = i)
    // Define as cidades disponíveis para o estado selecionado
let cidades;
    if (estado === "SP") {
        cidades = ["São Paulo", "Campinas", "Santos"];
    } else if (estado === "RJ") {
        cidades = ["Rio de Janeiro", "Niterói", "Belford Roxo"];
    } else if (estado === "MG") {
        cidades = ["Belo Horizonte", "Juiz de Fora", "Uberlândia"];
    }
  
    // Atualiza o segundo <select> com as cidades disponíveis
    const cidadesSelect = document.getElementById("cidades");
    cidadesSelect.innerHTML = "";
    for (const cidade of cidades) {
        const option = document.createElement("option");
        option.value = cidade;
        option.text = cidade;
        cidadesSelect.add(option);
    }
}
