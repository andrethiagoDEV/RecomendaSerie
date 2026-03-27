// Função principal de busca
async function buscar() {
    console.log("Botão clicado");

    const input = document.getElementById("input");
    const valor = input.value.trim();

    const container = document.getElementById("resultado");
    const carrossel = document.getElementById("carrossel-busca");

    //  evita busca vazia
    if (valor === "") {
        container.innerHTML = "<p>Digite algo para buscar</p>";
        carrossel.style.display = "block";
        return;
    }

    try {
        const resposta = await fetch("/recomendar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ favoritas: valor })
        });

        const dados = await resposta.json();

        console.log(dados);

        container.innerHTML = "";

        // nenhum resultado
        if (!dados || dados.length === 0) {
            container.innerHTML = "<p>Nenhum resultado encontrado</p>";
            carrossel.style.display = "block";
            return;
        }

        // renderiza resultados
        dados.forEach(item => {
            const div = document.createElement("div");

            div.classList.add("card");

            div.innerHTML = `
                <img src="${item.imagem || 'https://via.placeholder.com/150'}" width="150">
                <h3>${item.titulo}</h3>
                <p>⭐ ${item.rating}</p>
            `;

            container.appendChild(div);
        });

        // mostra carrossel só depois da busca
        carrossel.style.display = "block";

    } catch (erro) {
        console.error("Erro na busca:", erro);
        container.innerHTML = "<p>Erro ao buscar dados</p>";
        carrossel.style.display = "block";
    }
}


// ENTER para buscar
document.getElementById("input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        buscar();
    }
});

async function carregarTop2025() {

    console.log("Chamando /top2025...");

    const resposta = await fetch("/top2025");
    const dados = await resposta.json();

    console.log("Dados recebidos:", dados); 

    const container = document.getElementById("top2025");
    container.innerHTML = "";

    dados.forEach(item => {
        const div = document.createElement("div");
        
        div.classList.add("card");

        div.innerHTML = `
            <img src="${item.imagem || 'https://via.placeholder.com/150'}" width="150">
            <h3>${item.titulo}</h3>
            <p>⭐ ${item.rating}</p>
        `;

        container.appendChild(div);
    });

    // Iniciar autoplay do carrossel
    iniciarAutoplay();
}

let indiceCarrossel = 0;
let autoplayInterval;

function moverCarrossel(direcao) {
    const container = document.querySelector('#top2025');
    const itens = container.children.length;
    const itensPorVisao = 4; 
    indiceCarrossel += direcao;

    if (indiceCarrossel < 0) indiceCarrossel = 0;
    if (indiceCarrossel > itens - itensPorVisao) indiceCarrossel = itens - itensPorVisao;

    const translateX = -indiceCarrossel * 210; 
    container.style.transform = `translateX(${translateX}px)`;
}

function iniciarAutoplay() {
    autoplayInterval = setInterval(() => {
        const container = document.querySelector('#top2025');
        const itens = container.children.length;
        const itensPorVisao = 4;
        indiceCarrossel += 1;

        if (indiceCarrossel > itens - itensPorVisao) {
            indiceCarrossel = 0; 
        }

        const translateX = -indiceCarrossel * 210;
        container.style.transform = `translateX(${translateX}px)`;
    }, 3000); // Muda a cada 3 segundos
}

// Pausar autoplay no hover
document.querySelector('#carrossel').addEventListener('mouseenter', () => {
    clearInterval(autoplayInterval);
});

// Retomar autoplay ao sair do hover
document.querySelector('#carrossel').addEventListener('mouseleave', () => {
    iniciarAutoplay();
});

async function carregarHorror() {

    const resposta = await fetch("/horror");
    const dados = await resposta.json();

    const container = document.getElementById("horror");
    container.innerHTML = "";

    dados.forEach(item => {
        const div = document.createElement("div");

        div.classList.add("card");

        div.innerHTML = `
            <img src="${item.imagem || 'https://via.placeholder.com/150'}" width="150">
            <h3>${item.titulo}</h3>
            <p>⭐ ${item.rating}</p>
        `;

        container.appendChild(div);
    });
}

async function carregarAcao() {

    const resposta = await fetch("/action");
    const dados = await resposta.json();

    const container = document.getElementById("action");
    container.innerHTML = "";

    // Cria uma div para cada série
    //Percorre os dados recebidos
    dados.forEach(item => {
        const div = document.createElement("div");

        // Adiciona classe CSS
        div.classList.add("card");

        div.innerHTML = `
            <img src="${item.imagem || 'https://via.placeholder.com/150'}" width="150">
            <h3>${item.titulo}</h3>
            <p>⭐ ${item.rating}</p>
        `;

        container.appendChild(div);
    });
}

// Quando a página terminar de carregar
window.onload = function() {
    carregarTop2025();
    carregarHorror();
    carregarAcao();
};
