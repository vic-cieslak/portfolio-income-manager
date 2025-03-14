document.addEventListener('DOMContentLoaded', function() {
    // Add glitch effect to the login text
    const loginText = document.querySelector('.glitch-text');
    if (loginText) {
        setInterval(() => {
            loginText.style.textShadow = `
                ${Math.random() < 0.5 ? '-' : ''}${Math.random() * 10}px 0 var(--secondary-color),
                ${Math.random() < 0.5 ? '-' : ''}${Math.random() * 10}px 0 var(--info-color)
            `;
            setTimeout(() => {
                loginText.style.textShadow = '';
            }, 50);
        }, 3000);
    }

    // Add cyberpunk cursor effect to input fields
    const inputs = document.querySelectorAll('.cyberpunk-input input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.caretColor = 'var(--primary-color)';
            this.style.caretShape = 'block';
        });
        input.addEventListener('blur', function() {
            this.style.caretColor = '';
            this.style.caretShape = '';
        });
    });

    // Add hover effect to the login button
    const loginButton = document.querySelector('.btn-cyber');
    if (loginButton) {
        loginButton.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            this.style.setProperty('--x', `${x}px`);
            this.style.setProperty('--y', `${y}px`);
        });
    }
});
