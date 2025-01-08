console.log("test");
// thid to avoid everything from crashind down and give some time to
// the DOM to load before the script is executed
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");
  let inputSize = document.querySelector("#input-size");
  createBoard(16);
});

function createBoard(size) {
  let board = document.querySelector(".container");
  board.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
  board.style.gridTemplateRows = `repeat(${size}, 1fr)`;
  let numDivs = size * size;
  for (let i = 0; i < size * size; i++) {
    let div = document.createElement("div");
    div.style.backgroundColor = "yellow";
    board.insertAdjacentElement("beforeend", div);
  }
}
