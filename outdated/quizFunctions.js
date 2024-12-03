// quizFunctions.js
import { data, genericHobbies, genericFoods, genericMemories  } from './quizData.js';

let currentGroup = Math.random() > 0.5 ? "grandchildren" : "children";
let currentQuestionIndex = Math.floor(Math.random() * data[currentGroup].length);

function getRandomQuestionType() {
    const types = ["name", "hobbies", "favorite_food", "favorite_memory"];
    return types[Math.floor(Math.random() * types.length)];
}

function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

function getUniqueOptions(correctOptions, genericOptions) {
    const allOptions = [...new Set([...correctOptions, ...genericOptions])];
    return shuffleArray(allOptions).slice(0, 6);
}

function handleAnswer(button, isCorrect) {
    if (isCorrect) {
        button.style.backgroundColor = "green";
        setTimeout(() => {
            currentQuestionIndex = Math.floor(Math.random() * data[currentGroup].length);
            loadQuestion();
        }, 1000);
    } else {
        button.style.backgroundColor = "red";
    }
}

function switchGroup(group) {
    currentGroup = group;
    currentQuestionIndex = Math.floor(Math.random() * data[currentGroup].length);
    loadQuestion();
}

function loadQuestion() {
    const photo = document.getElementById("photo");
    const question = document.getElementById("question");
    const options = document.getElementById("options");
    const feedback = document.getElementById("feedback");

    const group = data[currentGroup];
    const person = group[currentQuestionIndex];
    const questionType = getRandomQuestionType();

    photo.src = person.images[Math.floor(Math.random() * person.images.length)];
    feedback.innerText = "";
    options.innerHTML = "";

    if (questionType === "name") {
        question.innerText = "Who is this?";
        group.forEach(p => {
            const btn = document.createElement("button");
            btn.innerText = p.name;
            btn.onclick = () => handleAnswer(btn, p.name === person.name);
            options.appendChild(btn);
        });
    } else if (questionType === "hobbies") {
        question.innerText = `What are ${person.name}'s hobbies?`;
        const correctHobbies = person.info.hobbies;
        const uniqueHobbies = getUniqueOptions(correctHobbies, genericHobbies);
        uniqueHobbies.forEach(hobby => {
            const btn = document.createElement("button");
            btn.innerText = hobby;
            btn.onclick = () => handleAnswer(btn, correctHobbies.includes(hobby));
            options.appendChild(btn);
        });
    } else if (questionType === "favorite_food") {
        question.innerText = `What is ${person.name}'s favorite food?`;
        const correctFoods = person.info.favorite_food;
        const uniqueFoods = getUniqueOptions(correctFoods, genericFoods);
        uniqueFoods.forEach(food => {
            const btn = document.createElement("button");
            btn.innerText = food;
            btn.onclick = () => handleAnswer(btn, correctFoods.includes(food));
            options.appendChild(btn);
        });
    } else if (questionType === "favorite_memory") {
        question.innerText = `What is ${person.name}'s favorite memory?`;
        const correctMemories = person.info.memories;
        const uniqueMemories = getUniqueOptions(correctMemories, genericMemories);
        uniqueMemories.forEach(memory => {
            const btn = document.createElement("button");
            btn.innerText = memory;
            btn.onclick = () => handleAnswer(btn, correctMemories.includes(memory));
            options.appendChild(btn);
        });
    }
}

export { switchGroup, loadQuestion };
