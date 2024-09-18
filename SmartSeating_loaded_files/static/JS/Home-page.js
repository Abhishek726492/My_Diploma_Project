let menu = document.querySelector('#menu-icon');
      let navbar = document.querySelector('.navbar');
      console.log('Js loaded')
      menu.onclick = () => {
      menu.classList.toggle('bx-x');
      navbar.classList.toggle('open');
    }