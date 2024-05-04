const savedCards = document.getElementById('saved-cards');
const newCardForm = document.getElementById('new-card-form');
const newCardForm2 = document.getElementById('new-card-form-2');
const texto = document.getElementById('texto');
const cantidad = document.getElementById('textuser');


var numClases = 0;
//var divs = document.getElementsByClassName("card-option");
bdchange();

async function bdchange() {
  const llamada = await fetch('https://pentagonal-noiseless-evergreen.glitch.me/devolver_tarjeta?'); //dato de la base de datos
  const tarjetas = await llamada.json();
  if (tarjetas.length !== 0) {
    newCardForm.classList.add('hidden'); 
    savedCards.classList.remove('hidden'); 
    texto.classList.add('hidden'); 
    for ( numClases = 0; numClases < tarjetas.length; numClases++) {
      var numerotarjeta = tarjetas[numClases][2];
      const divTarjeta = document.createElement('div');
      const imgtarjeta = document.createElement('img');
      const textotarjeta = document.createElement('p');
      //const botontarjeta = document.createElement('button');
      divTarjeta.className = 'card-option';//https://pentagonal-noiseless-evergreen.glitch.me/devolver_tarjeta?email=emirpuente31@gmail.com&contraseña=password123
      savedCards.appendChild(divTarjeta);

      imgtarjeta.src = 'https://cdn.glitch.global/eb1848c4-7902-4754-863f-353b190f8da4/tarjeta.png?v=1713567974648';
      textotarjeta.textContent = '●●●● ●●●● ●●●● ' + numerotarjeta[12] + numerotarjeta[13] + numerotarjeta[14] + numerotarjeta[15];
      //botontarjeta.textContent = 'BORRAR';
      divTarjeta.appendChild(imgtarjeta);
      divTarjeta.appendChild(textotarjeta);
      //divTarjeta.appendChild(botontarjeta);
      imgtarjeta.addEventListener("click", showNewCard);
      //botontarjeta.addEventListener("click", Borrar);
    }
  }
  else {
    numClases == 0;
  }
}

function showNewCardForm(event) {
  event.preventDefault(); 
  

  savedCards.classList.add('hidden'); 
  newCardForm.classList.remove('hidden'); 
}
function hideNewCardForm(event) {
  event.preventDefault(); 
  

  savedCards.classList.remove('hidden'); 
  newCardForm.classList.add('hidden'); 
}
function showNewCard(event) {
  event.preventDefault();
  
  savedCards.classList.add('hidden'); 
  newCardForm2.classList.remove('hidden'); 

}
function hideNewCard(event) {
  event.preventDefault();
  
  savedCards.classList.remove('hidden'); 
  newCardForm2.classList.add('hidden'); 

}

function Borrar(event) {
  event.preventDefault();
  const elemento = event.target.parentNode;
  savedCards.removeChild(elemento);
  numClases -= 1;
  if (numClases === 0) {
    texto.classList.remove('hidden'); 
  }
}
  
function change(event) {
  event.preventDefault(); 

  const imgtarjeta = document.createElement('img');
  const textotarjeta = document.createElement('p');
  //const botontarjeta = document.createElement('button');
  const numerotarjeta = document.querySelector('#NumTarjeta');
  
  if (numerotarjeta.value !== '' || numerotarjeta.length === 18) {
    newCardForm.classList.add('hidden'); 
    savedCards.classList.remove('hidden'); 
    texto.classList.add('hidden'); 
    const divTarjeta = document.createElement('div');
    divTarjeta.className = 'card-option';
    savedCards.appendChild(divTarjeta);

    imgtarjeta.src = 'https://cdn.glitch.global/eb1848c4-7902-4754-863f-353b190f8da4/tarjeta.png?v=1713567974648';
    textotarjeta.textContent = '●●●● ●●●● ●●●● ' + numerotarjeta.value[15] + numerotarjeta.value[16] + numerotarjeta.value[17] + numerotarjeta.value[18];
    //botontarjeta.textContent = 'BORRAR';
    divTarjeta.appendChild(imgtarjeta);
    divTarjeta.appendChild(textotarjeta);
    //divTarjeta.appendChild(botontarjeta);
    //numerotarjeta.value = '';
    //divs[numClases].addEventListener("click", showNewCard);
    imgtarjeta.addEventListener("click", showNewCard);
    //botontarjeta.addEventListener("click", Borrar);
    numClases += 1;
  }
  else if (cantidad.value !== '') {
    newCardForm2.classList.add('hidden'); 
    savedCards.classList.remove('hidden'); 
    //cantidad.value = '';
  }
  
}


document.getElementById('payWithCardButton').addEventListener('click', showNewCardForm);
document.querySelector('#agregarlista').addEventListener('submit', change); 
//cuando se implemente la base de datos cambiare el "click" a "submit"
document.querySelector('#salir').addEventListener('click', hideNewCardForm);
document.querySelector('#salir2').addEventListener('click', hideNewCard);

