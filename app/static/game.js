// read in the words in words_alpha.txt and return an array of words with length wordLength
async function getWords(wordLength) {
    // fetch words_alpha.txt
    const response = await fetch('/static/words_alpha.txt');
    // get text from file
    const wordsText = await response.text();
    // turn into array of words
    const wordsArray = wordsText.trim().split('\r\n')
    // return an array containing only words with length wordLength
    return wordsArray.filter(word => word.length === wordLength);
}

// select numWords unique words from wordsArray
function randomWords(numWords, wordsArray) {
    const wordsArrayLength = wordsArray.length;
    const toReturn = [];
    console.log(wordsArrayLength);
    for(let i = 0; i < numWords; i++) {
        toReturn.push(wordsArray[Math.floor(Math.random() * (wordsArrayLength - 1)) + 0]);
    }
    return toReturn;
}

// generate a game with numWords words of length wordLength
async function generateGame(wordLength, numWords) {
    // get words as array
    const wordsArray = await getWords(wordLength);
    console.log(wordsArray);
    // select words for the game
    const gameArray = randomWords(numWords, wordsArray);
    console.log(gameArray);
}

function main() {
    generateGame(4, 4);
}

document.addEventListener('DOMContentLoaded', main);