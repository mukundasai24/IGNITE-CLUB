document.addEventListener('DOMContentLoaded', () => {
    // 1. Staggered Entrance Animation
    const staggerItems = document.querySelectorAll('.stagger-item');
    staggerItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.transition = 'opacity 0.6s ease, transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
    });

    // 2. Select Input floating label logic
    const select = document.getElementById('department');
    select.addEventListener('change', () => {
        if(select.value) {
            select.nextElementSibling.classList.add('active-label');
        }
    });

    // Strict Number Validation for Roll Number
    const rollNumberInput = document.getElementById('rollNumber');
    rollNumberInput.addEventListener('input', function(e) {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 8);
    });

    // 3. Form Submit Logic with FormSubmit API
    const form = document.getElementById('registrationForm');
    const successMessage = document.getElementById('successMessage');
    const resetBtn = document.getElementById('resetBtn');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const btn = form.querySelector('.glow-button');
        const btnText = btn.querySelector('.btn-text');
        const originalText = btnText.innerText;
        
        // Loading State
        btnText.innerText = 'Transmitting...';
        btn.style.opacity = '0.9';
        btn.disabled = true;

        const formData = new FormData(form);
        const formEntries = Object.fromEntries(formData.entries());

        fetch("https://formsubmit.co/ajax/mukundeswarasai2007@gmail.com", {
            method: "POST",
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                _subject: "✨ New Premium Student Registration: " + formEntries.name,
                "Full Name": formEntries.name,
                "Roll Number": formEntries.rollNumber,
                "Department": formEntries.department,
                "Interested Domain": formEntries.domain,
                "Email Address": formEntries.email,
                "Events & Workshops of Interest": formEntries.events
            })
        })
        .then(response => response.json())
        .then(data => {
            // Also send data to local SQL Database API quietly in background
            return fetch("/api/register", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formEntries)
            });
        })
        .then(() => {
            // Hide form and show animated success message
            form.classList.add('hidden');
            document.querySelector('.form-header').classList.add('hidden');
            successMessage.classList.remove('hidden');
            
            // Reset button state
            btnText.innerText = originalText;
            btn.style.opacity = '1';
            btn.disabled = false;
        })
        .catch(error => {
            console.error(error);
            alert("Connection error. Please try submitting again.");
            
            btnText.innerText = originalText;
            btn.style.opacity = '1';
            btn.disabled = false;
        });
    });

    // 4. Reset Button
    resetBtn.addEventListener('click', () => {
        form.reset();
        successMessage.classList.add('hidden');
        document.querySelector('.form-header').classList.remove('hidden');
        form.classList.remove('hidden');
        
        // Reset staggered animation so it plays nicely
        staggerItems.forEach(item => {
            item.style.transition = 'none';
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
        });
        setTimeout(() => {
            staggerItems.forEach((item, index) => {
                setTimeout(() => {
                    item.style.transition = 'opacity 0.6s ease, transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 100 * (index + 1));
            });
        }, 50);

        // Keep label active because of placeholder setup
        select.nextElementSibling.classList.add('active-label');
    });

    // 5. 3D Tilt Effect on the Glass Panel
    const panel = document.querySelector('.glass-panel');
    const container = document.querySelector('.main-container');

    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        // Mouse position relative to the center of the container
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        // Max tilt of 6 degrees for a subtle, premium feel
        const tiltX = (y / rect.height) * -6; 
        const tiltY = (x / rect.width) * 6;
        
        panel.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateZ(0)`;
    });

    container.addEventListener('mouseleave', () => {
        panel.style.transform = `rotateX(0) rotateY(0) translateZ(0)`;
        panel.style.transition = 'transform 0.6s cubic-bezier(0.23, 1, 0.32, 1)';
    });
    
    container.addEventListener('mouseenter', () => {
        // Remove transition to snap to mouse quickly while moving
        panel.style.transition = 'transform 0.1s linear';
    });
});
// OLD CODE (lines 46-61):
fetch("https://formsubmit.co/ajax/mukundeswarasai2007@gmail.com", {
    method: "POST",
    headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    body: JSON.stringify({...})
})

// NEW CODE:
fetch("http://localhost:3000/api/register", {  // Or your deployed server URL
    method: "POST",
    headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    body: JSON.stringify({
        name: formEntries.name,
        rollNumber: formEntries.rollNumber,
        department: formEntries.department,
        domain: formEntries.domain,
        email: formEntries.email,
        events: formEntries.events
    })
})
