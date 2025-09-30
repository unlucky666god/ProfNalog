// Mobile menu toggle
document.querySelector('.mobile-menu').addEventListener('click', function() {
    document.querySelector('nav ul').classList.toggle('show');
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
        
        // Close mobile menu if open
        document.querySelector('nav ul').classList.remove('show');
    });
});

// Header scroll effect
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        header.style.background = 'rgba(255, 255, 255, 0.95)';
    } else {
        header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        header.style.background = 'white';
    }
});

// Анимация при скролле для преимуществ
function animateOnScroll() {
    const elements = document.querySelectorAll('.feature-card, .about-image');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if (elementPosition < screenPosition) {
            element.classList.add('visible');
        }
    });
}

// Инициализация анимаций при загрузке
window.addEventListener('load', function() {
    // Анимация преимуществ при загрузке, если они видны
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('visible');
        }, 300 * index);
    });
    
    // Анимация изображения "О нас", если оно видно
    const aboutImage = document.querySelector('.about-image');
    if (aboutImage && aboutImage.getBoundingClientRect().top < window.innerHeight) {
        setTimeout(() => {
            aboutImage.classList.add('visible');
        }, 500);
    }
});

// Слушатель скролла для анимаций
window.addEventListener('scroll', animateOnScroll);

// Повторная проверка при изменении размера окна
window.addEventListener('resize', animateOnScroll);

// --- Бесконечная карусель отзывов ---
document.addEventListener('DOMContentLoaded', function () {
    const carousels = document.querySelectorAll('.carousel-track');

    carousels.forEach(track => {
        const direction = track.dataset.direction; // 'left' или 'right'
        const wrapper = track.parentElement;
        // const wrapperWidth = wrapper.offsetWidth; // Не используется напрямую

        // 1. Создаем клоны всех карточек и добавляем их в DOM
        const cards = Array.from(track.children);
        cards.forEach(card => {
            const clone = card.cloneNode(true);
            track.appendChild(clone);
        });

        // 2. Получаем обновленный список карточек (включая оригиналы и клоны)
        const allCards = Array.from(track.children);
        // --- ОБНОВЛЕНИЕ РАСЧЕТА ШИРИНЫ КАРТОЧКИ ---
        // Теперь мы используем фиксированную ширину из CSS + margin-right
        // Ширина карточки 300px + отступ справа 20px
        const cardWidth = 300 + 20; // ширина карточки + margin-right
        // --- КОНЕЦ ОБНОВЛЕНИЯ ---
        const totalWidth = cardWidth * allCards.length;

        // 3. Устанавливаем ширину дорожки
        track.style.width = `${totalWidth}px`;

        // 4. Настраиваем начальную позицию для правой дорожки
        if (direction === 'right') {
            track.style.transform = `translateX(-${totalWidth / 2}px)`;
        }

        // 5. Настраиваем параметры анимации
        let position = direction === 'left' ? 0 : -totalWidth / 2; // Начальная позиция
        // Скорость прокрутки (px/ms) - можете настроить
        const speed = direction === 'left' ? -0.03 : 0.03;
        let lastTimestamp = 0;
        let animationId;

        // 6. Функция анимации
        function animate(timestamp) {
            if (!lastTimestamp) lastTimestamp = timestamp;
            const deltaTime = timestamp - lastTimestamp;
            lastTimestamp = timestamp;

            position += speed * deltaTime;

            // 7. Бесшовный сброс позиции
            if (direction === 'left' && Math.abs(position) >= totalWidth / 2) {
                position = 0; // Сброс в начало
            } else if (direction === 'right' && position >= 0) {
                position = -totalWidth / 2; // Сброс в начало
            }

            track.style.transform = `translateX(${position}px)`;

            animationId = requestAnimationFrame(animate);
        }

        // 8. Запуск анимации
        animationId = requestAnimationFrame(animate);

        // 9. (Опционально) Пауза при наведении
        wrapper.addEventListener('mouseenter', () => {
            cancelAnimationFrame(animationId);
        });

        wrapper.addEventListener('mouseleave', () => {
            lastTimestamp = 0;
            animationId = requestAnimationFrame(animate);
        });
    });
});