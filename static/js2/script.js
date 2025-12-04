// Liste simple de questions/choix/réponses
const quiz = [
    {
        intro: "Commençons doucement !",
        question: "Ton ordinateur fonctionne encore parfaitement, mais on te dit qu'il est 'trop vieux'. Comment appelle-t-on ça ?",
        answers: ["Une sieste", "L’obsolescence numérique", "Une tempête solaire", "Un caprice du Wi-Fi"],
        correct: 1
    },
    {
        intro: "Continuons !",
        question: "Quand une seule grande entreprise décide pour tout le monde, on parle de :",
        answers: ["Liberté totale", "Dépendance aux Big Tech", "Danse synchronisée", "Effet papillon"],
        correct: 1
    },
    {
        intro: "Toujours avec moi ?",
        question: "La démarche NIRD propose souvent :",
        answers: ["De jeter plus vite", "D’installer Linux", "De peindre son PC en bleu", "D’acheter 12 écrans"],
        correct: 1
    }
];

let index = 0;

// Sélection des zones HTML
const avatarText = document.getElementById("avatar-text");
const questionBox = document.getElementById("question-box");
const answersBox = document.getElementById("answers");

// Fonction d'affichage
function showQuestion() {
    const q = quiz[index];

    avatarText.innerText = q.intro;
    questionBox.innerText = q.question;

    answersBox.innerHTML = "";
    q.answers.forEach((ans, i) => {
        const btn = document.createElement("button");
        btn.innerText = ans;
        btn.onclick = () => checkAnswer(i);
        answersBox.appendChild(btn);
    });
}

// Vérification des réponses
function checkAnswer(i) {
    const q = quiz[index];

    if (i === q.correct) {
        avatarText.innerText = "Bonne réponse ! 🎉";
    } else {
        avatarText.innerText = "Oups ! Réessaie ! 😅";
        return;
    }

    // Passage à la question suivante
    index++;
    if (index < quiz.length) {
        setTimeout(showQuestion, 1200);
    } else {
        setTimeout(() => {
            avatarText.innerText = "Bravo ! Tu as terminé le quiz NIRD ! 🌿✨";
            questionBox.innerText = "";
            answersBox.innerHTML = "";
        }, 1200);
    }
}

// Démarrage
showQuestion();
