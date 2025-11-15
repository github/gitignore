// Vocabulary words for the game
const vocabWords = [
    'Arbitrary', 'Catalyst', 'Facilitate', 'Incorrigible', 
    'Militant', 'Paramount', 'Rebut', 'Reprimand', 
    'Servitude', 'Slapdash'
];

// Game state
let currentSlide = 1;
const totalSlides = 17;
let spyPlayer = null;
let gameWord = null;
let timerInterval = null;
let timeLeft = 240; // 4 minutes in seconds
let currentVoter = 1;
let votes = {};
let playerRevealed = {};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateSlideCounter();
    setupNavigation();
    setupRiddleButton();
    setupGameButtons();
});

// Navigation
function setupNavigation() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    prevBtn.addEventListener('click', () => changeSlide(-1));
    nextBtn.addEventListener('click', () => changeSlide(1));
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') changeSlide(-1);
        if (e.key === 'ArrowRight') changeSlide(1);
    });
}

function changeSlide(direction) {
    const slides = document.querySelectorAll('.slide');
    const currentSlideEl = slides[currentSlide - 1];
    
    currentSlideEl.classList.remove('active');
    
    currentSlide += direction;
    
    // Boundary checks
    if (currentSlide < 1) currentSlide = 1;
    if (currentSlide > totalSlides) currentSlide = totalSlides;
    
    const newSlideEl = slides[currentSlide - 1];
    newSlideEl.classList.add('active');
    
    updateSlideCounter();
    updateNavigationButtons();
}

function updateSlideCounter() {
    const counter = document.getElementById('slideCounter');
    counter.textContent = `${currentSlide} / ${totalSlides}`;
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    prevBtn.disabled = currentSlide === 1;
    nextBtn.disabled = currentSlide === totalSlides;
}

// Riddle Button
function setupRiddleButton() {
    const riddleBtn = document.getElementById('riddleBtn');
    const riddleAnswer = document.getElementById('riddleAnswer');
    
    riddleBtn.addEventListener('click', () => {
        riddleAnswer.classList.remove('hidden');
        riddleBtn.style.display = 'none';
    });
}

// Quiz Answer Function (called from HTML)
window.showAnswer = function(button, answer) {
    const questionBox = button.parentElement;
    const answerEl = questionBox.querySelector('.answer');
    answerEl.textContent = `Answer: ${answer}`;
    answerEl.classList.remove('hidden');
    button.style.display = 'none';
};

// Game Setup
function setupGameButtons() {
    const startGameBtn = document.getElementById('startGameBtn');
    const resetGameBtn = document.getElementById('resetGameBtn');
    
    startGameBtn.addEventListener('click', startGame);
    resetGameBtn.addEventListener('click', resetGame);
}

function startGame() {
    // Reset game state
    spyPlayer = Math.floor(Math.random() * 14) + 1; // Random player 1-14
    gameWord = vocabWords[Math.floor(Math.random() * vocabWords.length)];
    playerRevealed = {};
    
    // Create player boxes
    const playerBoxes = document.getElementById('playerBoxes');
    playerBoxes.innerHTML = '';
    
    for (let i = 1; i <= 14; i++) {
        const box = document.createElement('div');
        box.className = 'player-box';
        box.innerHTML = `
            <div class="player-number">Player ${i}</div>
            <div class="player-word" style="display:none;"></div>
        `;
        
        box.addEventListener('click', () => revealPlayer(i, box));
        playerBoxes.appendChild(box);
    }
    
    // Show timer and reset button
    document.getElementById('timer').style.display = 'block';
    document.getElementById('startGameBtn').style.display = 'none';
    document.getElementById('resetGameBtn').style.display = 'inline-block';
    
    // Start timer
    startTimer();
    
    // Setup voting slide
    setupVoting();
}

function revealPlayer(playerNum, box) {
    if (playerRevealed[playerNum]) return;
    
    const wordEl = box.querySelector('.player-word');
    
    if (playerNum === spyPlayer) {
        wordEl.textContent = '🕵️ You are the SPY!';
        wordEl.style.color = '#ff0000';
        box.classList.add('spy');
    } else {
        wordEl.textContent = `Your word: ${gameWord}`;
        wordEl.style.color = '#00ff00';
    }
    
    wordEl.style.display = 'block';
    box.classList.add('revealed');
    playerRevealed[playerNum] = true;
}

function startTimer() {
    timeLeft = 240; // Reset to 4 minutes
    updateTimerDisplay();
    
    timerInterval = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert('Time is up! Proceed to voting.');
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    const timeLeftEl = document.getElementById('timeLeft');
    timeLeftEl.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    
    // Change color when time is running out
    if (timeLeft <= 60) {
        timeLeftEl.style.color = '#ff0000';
    } else {
        timeLeftEl.style.color = '#00ff00';
    }
}

function resetGame() {
    // Clear timer
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    // Reset UI
    document.getElementById('playerBoxes').innerHTML = '';
    document.getElementById('timer').style.display = 'none';
    document.getElementById('startGameBtn').style.display = 'inline-block';
    document.getElementById('resetGameBtn').style.display = 'none';
    
    // Reset game state
    spyPlayer = null;
    gameWord = null;
    playerRevealed = {};
}

// Voting System
function setupVoting() {
    votes = {};
    currentVoter = 1;
    
    const votingGrid = document.getElementById('votingGrid');
    votingGrid.innerHTML = '';
    
    for (let i = 1; i <= 14; i++) {
        votes[i] = 0;
        
        const voteBox = document.createElement('div');
        voteBox.className = 'vote-box';
        voteBox.innerHTML = `
            <div class="player-number">Player ${i}</div>
            <div class="vote-percentage">0%</div>
        `;
        
        voteBox.addEventListener('click', () => castVote(i));
        votingGrid.appendChild(voteBox);
    }
    
    updateCurrentVoter();
    
    const nextVoterBtn = document.getElementById('nextVoterBtn');
    const revealSpyBtn = document.getElementById('revealSpyBtn');
    
    nextVoterBtn.addEventListener('click', nextVoter);
    revealSpyBtn.addEventListener('click', revealSpy);
}

function castVote(playerNum) {
    votes[playerNum]++;
    updateVoteDisplay();
}

function updateVoteDisplay() {
    const totalVotes = Object.values(votes).reduce((a, b) => a + b, 0);
    const voteBoxes = document.querySelectorAll('.vote-box');
    
    voteBoxes.forEach((box, index) => {
        const playerNum = index + 1;
        const percentage = totalVotes > 0 ? Math.round((votes[playerNum] / totalVotes) * 100) : 0;
        const percentageEl = box.querySelector('.vote-percentage');
        percentageEl.textContent = `${percentage}% (${votes[playerNum]} votes)`;
        
        if (votes[playerNum] > 0) {
            box.classList.add('selected');
        }
    });
}

function updateCurrentVoter() {
    const currentVoterEl = document.getElementById('currentVoter');
    currentVoterEl.textContent = `Current Voter: Player ${currentVoter}`;
}

function nextVoter() {
    currentVoter++;
    
    if (currentVoter > 14) {
        document.getElementById('nextVoterBtn').style.display = 'none';
        document.getElementById('revealSpyBtn').style.display = 'inline-block';
        alert('All players have voted! Click "Reveal Spy" to see the result.');
    } else {
        updateCurrentVoter();
    }
}

function revealSpy() {
    // Find player with most votes
    let maxVotes = 0;
    let suspectedSpy = 1;
    
    for (let player in votes) {
        if (votes[player] > maxVotes) {
            maxVotes = votes[player];
            suspectedSpy = parseInt(player);
        }
    }
    
    // Update reveal slide
    const spyReveal = document.getElementById('spyReveal');
    
    if (suspectedSpy === spyPlayer) {
        spyReveal.innerHTML = `
            The spy was Player ${spyPlayer}! 🎭<br>
            <span style="color: #00ff00;">The group guessed correctly! 🎉</span>
        `;
    } else {
        spyReveal.innerHTML = `
            The spy was Player ${spyPlayer}! 🎭<br>
            <span style="color: #ff6b6b;">But the group voted for Player ${suspectedSpy}! The spy wins! 😈</span>
        `;
    }
    
    // Move to reveal slide
    changeSlide(1);
}

// Initialize navigation buttons state
updateNavigationButtons();
