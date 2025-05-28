document.addEventListener('DOMContentLoaded', () => {
    // Three.js 3D Background Animation
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.domElement.style.position = 'fixed';
    renderer.domElement.style.top = '0';
    renderer.domElement.style.left = '0';
    renderer.domElement.style.zIndex = '-1';
    document.body.appendChild(renderer.domElement);

    // Create a particle system with 3D spheres
    const particles = new THREE.Group();
    const particleCount = 100;
    const geometry = new THREE.SphereGeometry(0.2, 16, 16);
    const material = new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.5 });

    for (let i = 0; i < particleCount; i++) {
        const particle = new THREE.Mesh(geometry, material);
        particle.position.set(
            (Math.random() - 0.5) * 50,
            (Math.random() - 0.5) * 50,
            (Math.random() - 0.5) * 50
        );
        particle.velocity = new THREE.Vector3(
            (Math.random() - 0.5) * 0.02,
            (Math.random() - 0.5) * 0.02,
            (Math.random() - 0.5) * 0.02
        );
        particles.add(particle);
    }

    scene.add(particles);
    camera.position.z = 30;

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);

        particles.children.forEach(particle => {
            particle.position.add(particle.velocity);
            if (particle.position.x > 25 || particle.position.x < -25) particle.velocity.x *= -1;
            if (particle.position.y > 25 || particle.position.y < -25) particle.velocity.y *= -1;
            if (particle.position.z > 25 || particle.position.z < -25) particle.velocity.z *= -1;
            particle.rotation.x += 0.01;
            particle.rotation.y += 0.01;
        });

        particles.rotation.y += 0.002;
        renderer.render(scene, camera);
    }

    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Dark mode toggle
    const toggleButton = document.getElementById('darkModeToggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
            material.color.set(document.documentElement.classList.contains('dark') ? 0x60a5fa : 0xa855f7);
        });
        // Load saved theme
        if (localStorage.getItem('theme') === 'dark') {
            document.documentElement.classList.add('dark');
            material.color.set(0x60a5fa);
        } else {
            material.color.set(0xa855f7);
        }
    }

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const inputs = form.querySelectorAll('input[required], select[required]');
            let valid = true;
            inputs.forEach(input => {
                if (!input.value) {
                    valid = false;
                    input.classList.add('border-red-500');
                } else {
                    input.classList.remove('border-red-500');
                }
            });
            if (!valid) {
                e.preventDefault();
                showToast('Please fill in all required fields', 'error');
            }
        });
    });

    // Email validation for signup
    const signupForm = document.querySelector('#signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            const email = signupForm.querySelector('input[name="email"]').value;
            const password = signupForm.querySelector('input[name="password"]').value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                showToast('Please enter a valid email address', 'error');
            }
            if (password.length < 8) {
                e.preventDefault();
                showToast('Password must be at least 8 characters long', 'error');
            }
        });
    }

    // Delete confirmation modal logic (only run if user is logged in)
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.style.display = 'none';
        const deleteLinks = document.querySelectorAll('.delete-link');
        const confirmDelete = document.getElementById('confirmDelete');
        const cancelDelete = document.getElementById('cancelDelete');

        if (deleteLinks.length > 0) {
            deleteLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    modal.style.display = 'flex';
                    confirmDelete.href = link.href;
                });
            });
        }

        if (cancelDelete) {
            cancelDelete.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }
    }

    // Toast notification
    function showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `fixed bottom-6 right-6 p-4 rounded-lg shadow-lg text-white z-50 ${type === 'success' ? 'bg-green-600' : 'bg-red-600'}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('opacity-0');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Apply fade-in animation
    document.querySelectorAll('.fade-in').forEach(el => {
        el.style.opacity = 0;
        setTimeout(() => {
            el.style.opacity = 1;
        }, 100);
    });
});