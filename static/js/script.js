document.addEventListener('DOMContentLoaded', function() {
    // File input handling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const label = this.nextElementSibling;
            const fileName = this.files[0]?.name;
            
            if (fileName) {
                label.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    <span>${fileName}</span>
                `;
                label.style.background = 'linear-gradient(135deg, #48bb78, #38a169)';
            }
        });
    });
    
    // Form submission handling
    const form = document.querySelector('.upload-form');
    const submitBtn = document.querySelector('.submit-btn');
    
    if (form && submitBtn) {
        form.addEventListener('submit', function() {
            submitBtn.innerHTML = `
                <i class="fas fa-spinner fa-spin"></i>
                <span>Processing...</span>
            `;
            submitBtn.disabled = true;
        });
    }
    
    // Add smooth scrolling for better UX
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Add loading animation to cards
    const cards = document.querySelectorAll('.upload-card, .info-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Particle background animation
const particlesBg = document.getElementById('particles-bg');
if (particlesBg) {
    const canvas = document.createElement('canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '0';
    particlesBg.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    let particles = [];
    const colors = ['#3a86ff', '#8338ec', '#ffbe0b', '#ff006e', '#fb5607'];
    const numParticles = Math.floor(window.innerWidth / 16);
    for (let i = 0; i < numParticles; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            r: Math.random() * 2.5 + 1.5,
            dx: (Math.random() - 0.5) * 0.7,
            dy: (Math.random() - 0.5) * 0.7,
            color: colors[Math.floor(Math.random() * colors.length)]
        });
    }
    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let p of particles) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, 2 * Math.PI);
            ctx.fillStyle = p.color + '99';
            ctx.shadowColor = p.color;
            ctx.shadowBlur = 8;
            ctx.fill();
            p.x += p.dx;
            p.y += p.dy;
            if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
        }
        requestAnimationFrame(animateParticles);
    }
    animateParticles();
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// Smooth page transitions
window.addEventListener('DOMContentLoaded', () => {
    document.body.style.opacity = 0;
    document.body.style.transition = 'opacity 0.7s cubic-bezier(.4,2,.3,1)';
    setTimeout(() => { document.body.style.opacity = 1; }, 50);
});

// 3D hover effect for cards
function add3DHover(selector) {
    document.querySelectorAll(selector).forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const xc = rect.width / 2;
            const yc = rect.height / 2;
            const dx = (x - xc) / xc;
            const dy = (y - yc) / yc;
            card.style.transform = `perspective(800px) scale(1.05) rotateY(${dx*8}deg) rotateX(${-dy*8}deg)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(800px) scale(1) rotateY(0deg) rotateX(0deg)';
        });
    });
}
add3DHover('.glass-card');
add3DHover('.upload-3d-card');
add3DHover('.info-card');

// File input drag-and-drop and progress
function setupFileInput(cardId, inputId, progressId) {
    const card = document.getElementById(cardId);
    const input = document.getElementById(inputId);
    const progress = document.getElementById(progressId);
    if (!card || !input || !progress) return;
    card.addEventListener('dragover', e => {
        e.preventDefault();
        card.classList.add('dragover');
    });
    card.addEventListener('dragleave', e => {
        e.preventDefault();
        card.classList.remove('dragover');
    });
    card.addEventListener('drop', e => {
        e.preventDefault();
        card.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;
            input.dispatchEvent(new Event('change'));
        }
    });
    input.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            let label = this.nextElementSibling;
            label.innerHTML = `<i class="fas fa-check-circle"></i> <span>${file.name}</span>`;
            label.style.background = 'linear-gradient(135deg, #3a86ff, #8338ec)';
        }
    });
}
setupFileInput('license-drop', 'license_file', 'license-progress');
setupFileInput('insurance-drop', 'insurance_file', 'insurance-progress');

// Form validation and animated progress
const form = document.getElementById('upload-form');
if (form) {
    form.addEventListener('submit', function(e) {
        let valid = true;
        ['license_file', 'insurance_file'].forEach(id => {
            const input = document.getElementById(id);
            if (!input.files.length) {
                valid = false;
                input.parentElement.classList.add('input-error');
                setTimeout(() => input.parentElement.classList.remove('input-error'), 1200);
            }
        });
        if (!valid) {
            e.preventDefault();
            return;
        }
        // Animate progress bars
        ['license-progress', 'insurance-progress'].forEach(pid => {
            const bar = document.getElementById(pid);
            if (bar) {
                bar.style.width = '100%';
            }
        });
        // Animate button
        const btn = form.querySelector('.submit-btn-3d');
        if (btn) {
            btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> <span>Processing...</span>`;
            btn.disabled = true;
        }
    });
} 