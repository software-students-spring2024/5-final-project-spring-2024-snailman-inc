const wordLength = 4;
const numWords = 4;
let input = '';

// read in the words in words_alpha.txt and return an array of words with length wordLength
async function getWords() {
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
async function randomWords(wordsArray) {
    const wordsArrayLength = wordsArray.length;
    const toReturn = [];
    for(let i = 0; i < numWords; i++) {
        toReturn.push(wordsArray[Math.floor(Math.random() * (wordsArrayLength - 1)) + 0]);
    }
    return toReturn;
}

// generate a game with numWords words of length wordLength
async function generateGame() {
    // get words as array
    const wordsArray = await getWords();

    // select words for the game
    const gameArray = randomWords(wordsArray);

    return gameArray;
}

async function shuffleArray(letterArray) {
    for (let i = letterArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [letterArray[i], letterArray[j]] = [letterArray[j], letterArray[i]];
    }
}

async function checkWord(gameArray) {
    if(gameArray.includes(input)) {
        // if word is correct
        document.querySelectorAll('span.tile.toggled').forEach(tile => {
            // take letter out of options
            tile.removeChild(tile.firstChild);
            tile.classList.remove('toggled');
            tile.classList.add('used');
        });
    }
    else {
        // if word is incorrect
        document.querySelectorAll('span.tile.toggled').forEach(tile => {
            // untoggle tile
            tile.classList.remove('toggled');
        });
    }
    // clear input
    input = '';
    document.querySelectorAll('span.inputTile').forEach(inputTile => {
        inputTile.removeChild(inputTile.firstChild);
    });
}

async function selectTile(gameArray) {
    if(!this.classList.contains('toggled') && !this.classList.contains('used')) {
        this.classList.add('toggled');
        const inputTile = document.querySelector(`span.inputTile[position="${input.length}"]`);
        inputTile.appendChild(document.createTextNode(this.textContent))
        input = input.concat(this.textContent);
        if(input.length == wordLength) {
            checkWord(gameArray);
        }
    }
}

async function drawGame(gameArray) {
    // flatten gameArray into an array of its component letters
    const letterArray = gameArray.reduce((letters, word) => letters.concat(word.split('')), []);

    // shuffle letterArray for displaying in the grid
    shuffleArray(letterArray)
    console.log(letterArray);

    // draw grid of letter tiles
    const tileGrid = document.createElement('div');
    tileGrid.classList.add('tileGrid');
    for(let i = 0; i < numWords; i++) {
        const row = document.createElement('div');
        row.classList.add('row');
        for(let j = 0; j < wordLength; j++) {
            const tile = document.createElement('span');
            tile.appendChild(document.createTextNode(letterArray[i * wordLength + j]))
            tile.classList.add('tile');
            tile.addEventListener('click', function() {
                selectTile.call(this, gameArray);
            });

            row.appendChild(tile);
        }
        tileGrid.appendChild(row);
    }
    document.querySelector('div.game').appendChild(tileGrid);

    // draw row for displaying selected tiles
    const inputRow = document.createElement('div');
    inputRow.classList.add('inputRow');
    for(let i = 0; i < wordLength; i++) {
        const tile = document.createElement('span');
        tile.classList.add('inputTile');
        tile.setAttribute('position', i);

        // TODO: allow deletion by clicking
        //tile.addEventListener('click', deleteTile);

        inputRow.appendChild(tile);
        document.querySelector('div.game').appendChild(inputRow);
    }
}

async function main() {
    const gameArray = await generateGame();
    console.log(gameArray);
    drawGame(gameArray);
}

document.addEventListener('DOMContentLoaded', main);