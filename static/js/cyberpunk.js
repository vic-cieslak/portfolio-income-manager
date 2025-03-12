
// Cyberpunk Terminal Type Effect
function terminalTypeEffect(element, text, speed = 50) {
  let i = 0;
  element.innerHTML = '';
  function typeWriter() {
    if (i < text.length) {
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(typeWriter, speed);
    }
  }
  typeWriter();
}

// Add glitchy effects to elements
function addGlitchEffect() {
  const glitchElements = document.querySelectorAll('.glitch-text');
  glitchElements.forEach(el => {
    if (!el.getAttribute('data-text')) {
      el.setAttribute('data-text', el.textContent);
    }
  });
}

// Random flicker effect for elements with .flicker class
function flickerEffect() {
  const flickerElements = document.querySelectorAll('.flicker');
  flickerElements.forEach(el => {
    if (Math.random() > 0.99) {
      el.style.opacity = Math.random() * 0.5 + 0.5;
      setTimeout(() => {
        el.style.opacity = 1;
      }, 100);
    }
  });
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
  addGlitchEffect();
  
  // Apply terminal type effect to titles
  const pageTitles = document.querySelectorAll('.page-title:not(.glitch-text)');
  pageTitles.forEach(el => {
    const originalText = el.textContent;
    terminalTypeEffect(el, originalText, 70);
  });
  
  // Flicker effect interval
  setInterval(flickerEffect, 100);
  
  // Add data-terminal attribute to table cells for styling
  const tableCells = document.querySelectorAll('td');
  tableCells.forEach(cell => {
    const originalText = cell.textContent;
    if (originalText.trim() !== '') {
      cell.setAttribute('data-terminal', '>_');
    }
  });
});
