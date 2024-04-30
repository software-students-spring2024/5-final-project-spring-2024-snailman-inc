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
async function randomWords(numWords, wordsArray) {
    const wordsArrayLength = wordsArray.length;
    const toReturn = [];
    for(let i = 0; i < numWords; i++) {
        toReturn.push(wordsArray[Math.floor(Math.random() * (wordsArrayLength - 1)) + 0]);
    }
    return toReturn;
}

// generate a game with numWords words of length wordLength
async function generateGame(wordLength, numWords) {
    // get words as array
    const wordsArray = await getWords(wordLength);
    // select words for the game
    const gameArray = randomWords(numWords, wordsArray);
    console.log(gameArray);
    return gameArray;
}

async function shuffleArray(letterArray) {
    for (let i = letterArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [letterArray[i], letterArray[j]] = [letterArray[j], letterArray[i]];
      }
}

async function selectTile() {
    console.log(this.textContent);
}

async function drawGame(wordLength, numWords, gameArray) {
    console.log(gameArray);
    // flatten gameArray into an array of its component letters
    const letterArray = gameArray.reduce((letters, word) => letters.concat(word.split('')), []);
    // shuffle letterArray for displaying in the grid
    shuffleArray(letterArray)
    console.log(letterArray);
    const tileGrid = document.createElement('div');
    tileGrid.classList.add('tileGrid');
    for(let i = 0; i < numWords; i++) {
        const row = document.createElement('div');
        row.classList.add('row');
        for(let j = 0; j < wordLength; j++) {
            const tile = document.createElement('span');
            tile.appendChild(document.createTextNode(letterArray[i + j]))
            tile.classList.add('tile');
            tile.addEventListener('click', selectTile);
            row.appendChild(tile);
        }
        tileGrid.appendChild(row);
    }
    document.querySelector('div.game').appendChild(tileGrid);
    const inputRow = document.createElement('div');
    inputRow.classList.add('inputRow');
    for(let i = 0; i < wordLength; i++) {
        const tile = document.createElement('span');
        tile.classList.add('inputTile');
        tile.addEventListener('click', selectTile);
        inputRow.appendChild(tile);
        document.querySelector('div.game').appendChild(inputRow);
    }
}

async function main() {
    const wordLength = 4;
    const numWords = 4;
    const gameArray = await generateGame(wordLength, numWords);
    console.log(gameArray);
    drawGame(wordLength, numWords, gameArray);
}

document.addEventListener('DOMContentLoaded', main);