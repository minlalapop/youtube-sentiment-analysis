
const API_URL = "http://127.0.0.1:8000/predict_batch";

const analyzeBtn = document.getElementById("analyzeBtn");
const themeBtn = document.getElementById("themeBtn");
const copyBtn = document.getElementById("copyBtn");
const filterSelect = document.getElementById("filterSelect");

const status = document.getElementById("status");
const results = document.getElementById("results");
const stats = document.getElementById("stats");
const chartBar = document.getElementById("chartBar");
const commentList = document.getElementById("commentList");
const totalCount = document.getElementById("totalCount");

const sentimentNames = {
    positive: "Positif",
    neutral: "Neutre",
    negative: "Négatif"
};

let predictions = [];
let analysisData = null;


// Analyse des commentaires
async function analyzeComments() {
    analyzeBtn.disabled = true;
    results.hidden = true;
    status.textContent = "Analyse en cours...";

    try {
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        if (!tab?.url?.startsWith("https://www.youtube.com/watch")) {
            throw new Error("Ouvrez une vidéo YouTube.");
        }

        const response = await chrome.tabs.sendMessage(tab.id, {
            action: "EXTRACT_COMMENTS"
        });

        const comments = response?.comments || [];

        if (comments.length === 0) {
            throw new Error(
                "Aucun commentaire trouvé. Faites défiler la page."
            );
        }

        const apiResponse = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ comments })
        });

        if (!apiResponse.ok) {
            throw new Error(`Erreur API : ${apiResponse.status}`);
        }

        analysisData = await apiResponse.json();
        predictions = analysisData.predictions;

        filterSelect.value = "all";
        displayResults(analysisData);

        status.textContent =
            `${analysisData.total} commentaires analysés`;

    } catch (error) {
        status.textContent = error.message;
    } finally {
        analyzeBtn.disabled = false;
    }
}


// Affichage des résultats
function displayResults(data) {
    results.hidden = false;
    totalCount.textContent = `${data.total} commentaires`;

    displayStats(data.statistics.percentages);
    displayChart(data.statistics.percentages);
    displayComments();
}


// Cartes statistiques
function displayStats(percentages) {
    stats.replaceChildren();

    for (const [key, label] of Object.entries(sentimentNames)) {
        const card = document.createElement("div");
        card.className = "stat";

        const value = document.createElement("strong");
        value.textContent = `${percentages[key]}%`;

        const name = document.createElement("span");
        name.textContent = label;

        card.append(value, name);
        stats.appendChild(card);
    }
}


// Graphique de répartition
function displayChart(percentages) {
    chartBar.replaceChildren();

    for (const sentiment of Object.keys(sentimentNames)) {
        const bar = document.createElement("div");
        bar.className = `bar-${sentiment}`;
        bar.style.width = `${percentages[sentiment]}%`;

        chartBar.appendChild(bar);
    }
}


// Liste et filtres
function displayComments() {
    commentList.replaceChildren();

    const selected = filterSelect.value;

    const filtered = predictions.filter(prediction =>
        selected === "all" || prediction.sentiment === selected
    );

    filtered.forEach(prediction => {
        const item = document.createElement("div");
        item.className = `comment ${prediction.sentiment}`;

        const text = document.createElement("p");
        text.textContent = prediction.text;

        const sentiment = document.createElement("small");
        sentiment.textContent =
            `${sentimentNames[prediction.sentiment]} · ` +
            `${(prediction.confidence * 100).toFixed(1)}%`;

        item.append(text, sentiment);
        commentList.appendChild(item);
    });

    if (filtered.length === 0) {
        const empty = document.createElement("p");
        empty.textContent = "Aucun commentaire pour ce filtre.";
        commentList.appendChild(empty);
    }
}


// Mode sombre / clair
function toggleTheme() {
    document.body.classList.toggle("dark");
}


// Copier les résultats
async function copyResults() {
    if (!analysisData) return;

    const text = predictions.map(prediction =>
        `[${sentimentNames[prediction.sentiment]}] ` +
        `${prediction.text} ` +
        `(${(prediction.confidence * 100).toFixed(1)}%)`
    ).join("\n\n");

    try {
        await navigator.clipboard.writeText(text);
        status.textContent = "Résultats copiés !";
    } catch {
        status.textContent = "Impossible de copier les résultats.";
    }
}


// Événements
analyzeBtn.addEventListener("click", analyzeComments);
filterSelect.addEventListener("change", displayComments);
themeBtn.addEventListener("click", toggleTheme);
copyBtn.addEventListener("click", copyResults);
