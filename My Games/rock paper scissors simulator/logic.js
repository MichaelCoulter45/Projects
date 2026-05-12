
// Weapon functions
function bot_weapon() {
    return Math.floor(Math.random() * 3);
}
function rock() {
    document.getElementById("player_choice").textContent = "And You Chose Rock!";
    player = '0';
    bot = bot_weapon();
    battle(player, bot)
}
function paper() {
    document.getElementById("player_choice").textContent = "And You Chose Paper!";
    player = '1';
    bot = bot_weapon();
    battle(player, bot)
}

function scissors() {
    document.getElementById("player_choice").textContent = "And You Chose Scissors!";
    player = '2';
    bot = bot_weapon();
    battle(player, bot)
}










// rock = 0
// paper = 1
// scissors = 2
function battle(player, bot) {
    // setting the image to what the bot chose.
    if (bot == '0') {
        img_rock()
    }
    if (bot == '1') {
        img_paper()
    }
    if (bot == '2') {
        img_scissors()
    }

    // Determining the winner
    if (player == bot) { // Tie
        tie()
    }
    else if  (player == '0') { // Player chose Rock
        if (bot == 1) { // and the Bot chose Paper
            bot_win()
        }
        else {
            player_win()
        }
    }
    else if (player == '1') { // Player chose Paper
        if (bot == 0) { // and the bot chose Rock
            player_win()
        }
        else {
            bot_win()
        }
    }
    else if (player == '2') { // Player chose Scissors
        if (bot == 1) { // and the Bot chose Paper
            player_win()
        }
        else {
            bot_win()
        }
    }
}

// Winner handling
function tie() {
    document.getElementById("winner").textContent = "IT'S A TIE!!!";
}
function player_win() {
    document.getElementById("winner").textContent = "YOU WON! NICE!";
}
function bot_win() {
    document.getElementById("winner").textContent = "So, you lost.. The bot wins!";
}




// Image handling
function img_rock() {
    clear_img("bot-choice")
    document.getElementById("opponent").textContent = "Your Opponent Chose Rock!";
    var img = document.createElement("img");
    img.src = "./images/rock.png";
    var src = document.getElementById("bot-choice");
    src.appendChild(img);
}
function img_paper() {
    clear_img("bot-choice")
    document.getElementById("opponent").textContent = "Your Opponent Chose Paper!";
    var img = document.createElement("img");
    img.src = "./images/paper.png";
    var src = document.getElementById("bot-choice");
    src.appendChild(img);
}
function img_scissors() {
    clear_img("bot-choice")
    document.getElementById("opponent").textContent = "Your Opponent Chose Scissors!";
    var img = document.createElement("img");
    img.src = "./images/scissors.png";
    var src = document.getElementById("bot-choice");
    src.appendChild(img);
}
function clear_img(ID) {
    document.getElementById(ID).innerHTML = "";
}

/* References:
-- Clearing Images so they don't stack and over populate the screen --
// Source - https://stackoverflow.com/a/3450609
// Posted by Tom Gullen, modified by community. See post 'Timeline' for change history
// Retrieved 2026-05-08, License - CC BY-SA 4.0

function clearBox(elementID)
{
    document.getElementById(elementID).innerHTML = "";
}


-- Changing text with Javascript -- 
https://www.shecodes.io/athena/42622-how-to-show-text-with-a-link-on-button-click-using-javascript
*/

