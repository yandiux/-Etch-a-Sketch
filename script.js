console.log("test");
// thid to avoid everything from crashind down and give some time to
// the DOM to load before the script is executed
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");

  createBoard(16);
  let btn_popup = document.querySelector("#popup");
  btn_popup.addEventListener("click", function () {
    let size = getSize();
    createBoard(size);
  });
});

function createBoard(size) {
  let board = document.querySelector(".container");
  board.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
  board.style.gridTemplateRows = `repeat(${size}, 1fr)`;
  let numDivs = size * size;
  for (let i = 0; i < size * size; i++) {
    let div = document.createElement("div");
    div.addEventListener("mouseover", function () {
      div.style.backgroundColor = "black";
    });
    board.insertAdjacentElement("beforeend", div);
  }
}

function getSize() {
  let input = prompt("Enter the size of the board");
  let message = document.querySelector("#message");
  if (input === null) {
    message.innerHTML = "You have to enter a number";
  } else if (input < 1 || input > 100) {
    message.innerHTML = "Enter a number between 1 and 100";
  } else {
    message.innerHTML = `The size of the board is ${input}`;
    return input;
  }
}
