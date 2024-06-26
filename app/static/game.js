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

async function win() {
    // clear game
    document.querySelector('div.game').remove();

    // display win message
    body = document.querySelector('div.content')
    const winMessage = document.createElement('h1');
    winMessage.appendChild(document.createTextNode('You won!'));
    body.appendChild(winMessage);

    // button that starts a new game
    const newGame = document.createElement('button');
    newGame.appendChild(document.createTextNode('New Game'));
    newGame.addEventListener('click', function() {
        window.location.href = '/game';
    });
    body.appendChild(newGame);

    try {
        await fetch('/scored', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: 'snail' }) // sending 'winner' as the message
        });
    } catch (error) {
        console.error('Error updating score:', error);
        // Handle error if needed
    }
}

async function checkWord(gameArray) {
    gameArray = await gameArray;
    if((await gameArray).includes(input)) {
        // if word is correct
        document.querySelectorAll('span.tile.toggled').forEach(tile => {
            // unselect tiles
            tile.classList.remove('toggled');
            // clear tiles
            tile.classList.add('blank');
        });
        // take word out of options
        gameArray = gameArray.filter(function(word) {
            return word != input;
        });
        if(gameArray.length === 0) {
            win();
        }
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
    document.querySelectorAll('span.tile.input').forEach(inputTile => {
        inputTile.classList.add('blank');
    });
    return gameArray;
}

async function selectTile(gameArray) {
    if(!this.classList.contains('toggled') && !this.classList.contains('blank')) {
        this.classList.add('toggled');
        const inputTile = document.querySelector(`span.tile.input[position="${input.length}"]`);
        inputTile.textContent = this.textContent;
        inputTile.classList.remove('blank');
        input = input.concat(this.textContent);
        if(input.length == wordLength) {
            gameArray = checkWord(gameArray);
        }
    }
    return gameArray;
}

async function drawGame(gameArray) {
    // flatten gameArray into an array of its component letters
    const letterArray = gameArray.reduce((letters, word) => letters.concat(word.split('')), []);

    // shuffle letterArray for displaying in the grid
    shuffleArray(letterArray)

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
                gameArray = selectTile.call(this, gameArray);
            });
            row.appendChild(tile);
        }
        tileGrid.appendChild(row);
    }
    document.querySelector('div.game').appendChild(tileGrid);

    // draw row for displaying selected tiles
    const inputRow = document.createElement('div');
    inputRow.classList.add('row');
    inputRow.classList.add('input')
    for(let i = 0; i < wordLength; i++) {
        const tile = document.createElement('span');
        tile.classList.add('tile');
        tile.classList.add('input');
        tile.classList.add('blank');
        tile.setAttribute('position', i);
        tile.appendChild(document.createTextNode('*'));

        // TODO: allow deletion by clicking
        //tile.addEventListener('click', deleteTile);

        inputRow.appendChild(tile);
        document.querySelector('div.game').appendChild(inputRow);
    }


    // for testing
    /*const instaWin = document.createElement('button');
    instaWin.appendChild(document.createTextNode('Win'));
    instaWin.addEventListener('click', win);
    document.querySelector('div.game').appendChild(instaWin);*/
}

async function main() {
    let gameArray = await generateGame();
    console.log(gameArray);
    drawGame(gameArray);
}

document.addEventListener('DOMContentLoaded', main);