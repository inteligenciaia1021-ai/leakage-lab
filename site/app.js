const NS = "http://www.w3.org/2000/svg";
const COR_COM = "#F87171";
const COR_SEM = "#4ADE80";
const COR_TEXTO = "#94A3B8";
const COR_FORTE = "#F8FAFC";

function pct(valor) {
  return (valor * 100).toFixed(1).replace(".", ",") + "%";
}

function el(nome, atributos = {}, texto) {
  const elemento = document.createElementNS(NS, nome);
  for (const [chave, valor] of Object.entries(atributos)) {
    elemento.setAttribute(chave, valor);
  }
  if (texto !== undefined) elemento.textContent = texto;
  return elemento;
}

function preencherCartoes(dados) {
  const com = dados.com_vazamento.media;
  const sem = dados.sem_vazamento.media;
  const diferenca = ((com - sem) * 100).toFixed(1).replace(".", ",");

  document.getElementById("valor-errado").textContent = pct(com);
  document.getElementById("valor-certo").textContent = pct(sem);
  document.getElementById("valor-diferenca").textContent = diferenca + " p.p.";
}

function desenharGrafico(dados, alvo) {
  const LARGURA = 640;
  const ALTURA = 320;
  const margem = { esq: 52, dir: 16, topo: 16, base: 44 };
  const larguraPlot = LARGURA - margem.esq - margem.dir;
  const alturaPlot = ALTURA - margem.topo - margem.base;
  const MIN = 0.3;
  const MAX = 1.0;

  const y = (valor) =>
    margem.topo + ((MAX - valor) / (MAX - MIN)) * alturaPlot;

  const svg = el("svg", {
    viewBox: `0 0 ${LARGURA} ${ALTURA}`,
    width: "100%",
    "aria-hidden": "true",
  });

  for (let i = 3; i <= 10; i++) {
    const v = i / 10;
    const eMeio = i === 5;
    svg.appendChild(el("line", {
      x1: margem.esq, x2: LARGURA - margem.dir,
      y1: y(v), y2: y(v),
      stroke: eMeio ? COR_TEXTO : "#334155",
      "stroke-width": 1,
      "stroke-dasharray": eMeio ? "5 4" : "0",
    }));
    svg.appendChild(el("text", {
      x: margem.esq - 8, y: y(v) + 4,
      "text-anchor": "end", "font-size": 12, fill: COR_TEXTO,
    }, `${i * 10}%`));
  }

  svg.appendChild(el("text", {
    x: margem.esq + 6, y: y(0.5) - 6,
    "font-size": 12, fill: COR_TEXTO,
  }, "50% = palpite"));

  const grupos = [
    { chave: "com_vazamento", rotulo: "Com vazamento", cor: COR_COM, posicao: 0.25 },
    { chave: "sem_vazamento", rotulo: "Sem vazamento", cor: COR_SEM, posicao: 0.75 },
  ];

  for (const grupo of grupos) {
    const centro = margem.esq + larguraPlot * grupo.posicao;
    const info = dados[grupo.chave];

    info.notas.forEach((nota, i) => {
      const deslocamento = (((i * 37) % 21) - 10) * 5;
      svg.appendChild(el("circle", {
        cx: centro + deslocamento, cy: y(nota), r: 4,
        fill: grupo.cor, "fill-opacity": 0.7,
      }));
    });

    svg.appendChild(el("line", {
      x1: centro - 90, x2: centro + 90,
      y1: y(info.media), y2: y(info.media),
      stroke: COR_FORTE, "stroke-width": 2,
    }));
    svg.appendChild(el("text", {
      x: centro + 96, y: y(info.media) + 4,
      "font-size": 13, "font-weight": 700, fill: COR_FORTE,
    }, pct(info.media)));

    svg.appendChild(el("text", {
      x: centro, y: ALTURA - margem.base + 26,
      "text-anchor": "middle", "font-size": 14, fill: COR_FORTE,
    }, grupo.rotulo));
  }

  alvo.replaceChildren(svg);
  alvo.setAttribute(
    "aria-label",
    `Com vazamento, a acurácia média foi ${pct(dados.com_vazamento.media)}. ` +
    `Sem vazamento, ${pct(dados.sem_vazamento.media)}, em ${dados.configuracao.repeticoes} repetições.`
  );
}

async function iniciar() {
  const alvo = document.getElementById("grafico");
  try {
    const resposta = await fetch("resultados.json");
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
    const dados = await resposta.json();
    preencherCartoes(dados);
    desenharGrafico(dados, alvo);
  } catch (erro) {
    alvo.textContent =
      "Não foi possível carregar os resultados. Abra a página por um servidor local.";
    console.error(erro);
  }
}

iniciar();