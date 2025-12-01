// BigMart Analytics - Main JavaScript File
// Funcionalidades adicionales y efectos de interactividad

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar efectos y animaciones
    initializeAnimations();
    initializeScrollEffects();
    initializeInteractiveElements();
    
    console.log('BigMart Analytics - Sistema inicializado correctamente');
});

// Función para inicializar animaciones
function initializeAnimations() {
    // Animación de fade-in para elementos con la clase correspondiente
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    fadeElements.forEach(el => {
        observer.observe(el);
    });
    
    // Animación de números para KPI cards
    animateKPINumbers();
}

// Función para animar números en KPI cards
function animateKPINumbers() {
    const kpiCards = document.querySelectorAll('.kpi-card .text-3xl, .metric-card .text-3xl, .info-card .text-3xl');
    
    kpiCards.forEach(card => {
        const finalValue = card.textContent;
        const numericValue = parseFloat(finalValue.replace(/[^0-9.]/g, ''));
        
        if (!isNaN(numericValue)) {
            let currentValue = 0;
            const increment = numericValue / 50;
            
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= numericValue) {
                    currentValue = numericValue;
                    clearInterval(timer);
                }
                
                // Formatear el número según el tipo original
                if (finalValue.includes('$')) {
                    card.textContent = '$' + Math.round(currentValue).toLocaleString();
                } else if (finalValue.includes('%')) {
                    card.textContent = currentValue.toFixed(1) + '%';
                } else if (finalValue.includes('M')) {
                    card.textContent = '$' + (currentValue / 1000000).toFixed(1) + 'M';
                } else if (finalValue.includes('K')) {
                    card.textContent = '$' + Math.round(currentValue / 1000) + 'K';
                } else {
                    card.textContent = Math.round(currentValue).toLocaleString();
                }
            }, 30);
        }
    });
}

// Función para inicializar efectos de scroll
function initializeScrollEffects() {
    // Efecto de parallax suave para el header
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        const header = document.querySelector('header');
        
        if (header && scrolled > 0) {
            header.style.transform = `translateY(-${scrolled * 0.1}px)`;
            header.style.background = `rgba(255, 255, 255, ${0.95 - scrolled * 0.0005})`;
        }
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

// Función para inicializar elementos interactivos
function initializeInteractiveElements() {
    // Mejorar la interactividad de las cards
    const cards = document.querySelectorAll('.card-hover, .kpi-card, .metric-card, .info-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            anime({
                targets: this,
                scale: 1.02,
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
        
        card.addEventListener('mouseleave', function() {
            anime({
                targets: this,
                scale: 1,
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
    });
    
    // Efecto de ripple para botones
    const buttons = document.querySelectorAll('button, .btn, a[class*="bg-"]');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Agregar estilo para la animación ripple
    if (!document.querySelector('#ripple-styles')) {
        const style = document.createElement('style');
        style.id = 'ripple-styles';
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Función para mejorar la navegación del carrusel
function enhanceCarouselNavigation() {
    // Agregar navegación por teclado
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            const prevBtn = document.querySelector('.carousel-btn.prev');
            if (prevBtn) prevBtn.click();
        } else if (e.key === 'ArrowRight') {
            const nextBtn = document.querySelector('.carousel-btn.next');
            if (nextBtn) nextBtn.click();
        }
    });
    
    // Agregar swipe para dispositivos móviles
    let startX = 0;
    let endX = 0;
    
    const carousels = document.querySelectorAll('.carousel-container');
    
    carousels.forEach(carousel => {
        carousel.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
        });
        
        carousel.addEventListener('touchend', function(e) {
            endX = e.changedTouches[0].clientX;
            handleSwipe();
        });
        
        function handleSwipe() {
            const threshold = 50;
            const diff = startX - endX;
            
            if (Math.abs(diff) > threshold) {
                if (diff > 0) {
                    // Swipe left - next slide
                    const nextBtn = carousel.querySelector('.carousel-btn.next');
                    if (nextBtn) nextBtn.click();
                } else {
                    // Swipe right - prev slide
                    const prevBtn = carousel.querySelector('.carousel-btn.prev');
                    if (prevBtn) prevBtn.click();
                }
            }
        }
    });
}

// Función para manejar errores de carga de gráficos
function handleChartErrors() {
    const chartContainers = document.querySelectorAll('[id$="Chart"]');
    
    chartContainers.forEach(container => {
        // Verificar si el gráfico se cargó correctamente
        if (!container.hasChildNodes() || container.innerHTML === '') {
            // Mostrar mensaje de error o gráfico de respaldo
            const errorMsg = document.createElement('div');
            errorMsg.className = 'flex items-center justify-center h-full text-gray-500';
            errorMsg.innerHTML = `
                <div class="text-center">
                    <i class="fas fa-chart-bar text-4xl mb-4 opacity-50"></i>
                    <p class="text-sm">Gráfico no disponible temporalmente</p>
                    <p class="text-xs mt-2">Intentando recargar...</p>
                </div>
            `;
            container.appendChild(errorMsg);
            
            // Intentar recargar después de 3 segundos
            setTimeout(() => {
                location.reload();
            }, 3000);
        }
    });
}

// Función para agregar tooltips personalizados
function addCustomTooltips() {
    const elementsWithTooltips = document.querySelectorAll('[data-tooltip]');
    
    elementsWithTooltips.forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');
        
        const tooltip = document.createElement('div');
        tooltip.className = 'absolute z-50 px-2 py-1 text-xs text-white bg-gray-900 rounded opacity-0 pointer-events-none transition-opacity duration-200';
        tooltip.textContent = tooltipText;
        
        element.addEventListener('mouseenter', function() {
            document.body.appendChild(tooltip);
            const rect = element.getBoundingClientRect();
            tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
            tooltip.style.opacity = '1';
        });
        
        element.addEventListener('mouseleave', function() {
            tooltip.style.opacity = '0';
            setTimeout(() => {
                if (tooltip.parentNode) {
                    tooltip.parentNode.removeChild(tooltip);
                }
            }, 200);
        });
    });
}

// Función para manejar el estado de carga
function handleLoadingState() {
    // Agregar indicador de carga para gráficos
    const chartContainers = document.querySelectorAll('[id$="Chart"]');
    
    chartContainers.forEach(container => {
        const loader = document.createElement('div');
        loader.className = 'absolute inset-0 flex items-center justify-center bg-white bg-opacity-75';
        loader.innerHTML = `
            <div class="flex flex-col items-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mb-2"></div>
                <p class="text-sm text-gray-600">Cargando gráfico...</p>
            </div>
        `;
        
        container.style.position = 'relative';
        container.appendChild(loader);
        
        // Remover loader después de 2 segundos (simulando carga)
        setTimeout(() => {
            if (loader.parentNode) {
                loader.remove();
            }
        }, 2000);
    });
}

// Función para agregar analytics básicos
function addBasicAnalytics() {
    // Tracking de navegación entre páginas
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const pageName = this.textContent.trim();
            console.log(`Navegando a: ${pageName}`);
            
            // Aquí podrías enviar datos a un servicio de analytics
            // gtag('event', 'page_view', { page_title: pageName });
        });
    });
    
    // Tracking de interacciones con carrusel
    const carouselButtons = document.querySelectorAll('.carousel-btn');
    
    carouselButtons.forEach(button => {
        button.addEventListener('click', function() {
            const direction = this.classList.contains('next') ? 'siguiente' : 'anterior';
            console.log(`Carrusel - slide ${direction}`);
        });
    });
}

// Función principal de inicialización
function initializeApp() {
    try {
        // Inicializar todas las funcionalidades
        initializeAnimations();
        initializeScrollEffects();
        initializeInteractiveElements();
        enhanceCarouselNavigation();
        addCustomTooltips();
        handleLoadingState();
        addBasicAnalytics();
        
        // Verificar gráficos después de 3 segundos
        setTimeout(handleChartErrors, 3000);
        
        console.log('✅ BigMart Analytics - Todas las funcionalidades inicializadas');
        
    } catch (error) {
        console.error('❌ Error durante la inicialización:', error);
    }
}

// Inicializar la aplicación cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Exportar funciones para uso externo
window.BigMartAnalytics = {
    initializeApp,
    handleChartErrors,
    animateKPINumbers,
    addCustomTooltips
};