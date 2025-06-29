class GraduacionesApp {
    constructor() {
        this.facesData = {};
        this.currentModalPhoto = null;
        this.zoomLevel = 1;
        this.isDragging = false;
        this.dragStart = { x: 0, y: 0 };
        this.imagePosition = { x: 0, y: 0 };
        this.init();
    }

    async init() {
        try {
            await this.loadFacesData();
            this.displayGallery();
            this.hideLoading();
            this.setupModalEvents();
        } catch (error) {
            console.error('Error al inicializar la aplicación:', error);
            this.showError();
        }
    }

    async loadFacesData() {
        try {
            const response = await fetch('faces-numbered.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.facesData = await response.json();
        } catch (error) {
            console.error('Error al cargar faces-numbered.json:', error);
            throw error;
        }
    }

    displayGallery() {
        const gallery = document.getElementById('gallery');
        const photos = Object.keys(this.facesData).sort(); // Ordenar por año
        
        photos.forEach(photo => {
            const photoContainer = this.createPhotoContainer(photo);
            gallery.appendChild(photoContainer);
        });
        
        gallery.style.display = 'grid';
    }

    createPhotoContainer(photoName) {
        const container = document.createElement('div');
        container.className = 'photo-container';
        
        const year = photoName.replace(/\.[^/.]+$/, ""); // Remover extensión
        
        // Mostrar "Foto" para 2000 y 2001, "Graduación" para el resto
        let titlePrefix = "Graduación";
        if (year === "2000" || year === "2001") {
            titlePrefix = "Foto";
        }
        
        const caras = this.facesData[photoName];
        
        container.innerHTML = `
            <div class="photo-title">${titlePrefix} ${year}</div>
            <div class="photo-wrapper" onclick="app.openModal('${photoName}')">
                <img src="public/${photoName}" alt="${titlePrefix} ${year}" class="photo" 
                     onload="app.onImageLoad(this, '${photoName}')">
                ${this.createFaceBoxes(caras)}
            </div>
        `;
        
        return container;
    }

    createFaceBoxes(caras) {
        return caras.map(cara => {
            // Solo mostrar tooltip si hay nombre, sino no crear la caja
            if (!cara.nombre || cara.nombre.trim() === '') {
                return '';
            }
            
            return `
                <div class="face-box" 
                     style="left: ${cara.x}px; top: ${cara.y}px; width: ${cara.w}px; height: ${cara.h}px;">
                    <div class="face-tooltip">${cara.nombre}</div>
                </div>
            `;
        }).join('');
    }

    onImageLoad(img, photoName) {
        // Ajustar las posiciones de las caras según el tamaño real de la imagen
        const caras = this.facesData[photoName];
        const container = img.parentElement;
        const faceBoxes = container.querySelectorAll('.face-box');
        
        // Esperar a que la imagen se cargue completamente
        if (img.complete) {
            this.scaleGalleryFaces(img, photoName, faceBoxes);
        } else {
            img.onload = () => {
                this.scaleGalleryFaces(img, photoName, faceBoxes);
            };
        }
    }

    scaleGalleryFaces(img, photoName, faceBoxes) {
        const caras = this.facesData[photoName];
        
        // Obtener las dimensiones reales de la imagen
        const imgRect = img.getBoundingClientRect();
        const containerRect = img.parentElement.getBoundingClientRect();
        
        // Calcular las coordenadas relativas al contenedor
        const imgLeft = imgRect.left - containerRect.left;
        const imgTop = imgRect.top - containerRect.top;
        
        const originalWidth = img.naturalWidth;
        const originalHeight = img.naturalHeight;
        const displayWidth = imgRect.width;
        const displayHeight = imgRect.height;
        
        const scaleX = displayWidth / originalWidth;
        const scaleY = displayHeight / originalHeight;
        
        // Solo procesar caras que tienen nombre (que son las que tienen cajas)
        const carasConNombre = caras.filter(cara => cara.nombre && cara.nombre.trim() !== '');
        
        faceBoxes.forEach((box, index) => {
            const cara = carasConNombre[index];
            if (cara) {
                // Calcular las coordenadas escaladas relativas al contenedor
                const scaledX = (cara.x * scaleX) + imgLeft;
                const scaledY = (cara.y * scaleY) + imgTop;
                const scaledW = cara.w * scaleX;
                const scaledH = cara.h * scaleY;
                
                box.style.left = `${scaledX}px`;
                box.style.top = `${scaledY}px`;
                box.style.width = `${scaledW}px`;
                box.style.height = `${scaledH}px`;
            }
        });
    }

    setupModalEvents() {
        // Cerrar modal con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
            
            // Navegación con flechas solo si el modal está abierto
            if (this.currentModalPhoto) {
                if (e.key === 'ArrowLeft') {
                    this.previousPhoto();
                } else if (e.key === 'ArrowRight') {
                    this.nextPhoto();
                }
            }
        });

        // Cerrar modal haciendo clic fuera de la imagen
        document.getElementById('modal').addEventListener('click', (e) => {
            if (e.target.id === 'modal') {
                this.closeModal();
            }
        });

        // Zoom con rueda del mouse
        document.addEventListener('wheel', (e) => {
            if (this.currentModalPhoto && e.target.closest('.modal-image-container')) {
                e.preventDefault();
                if (e.deltaY < 0) {
                    this.zoomIn();
                } else {
                    this.zoomOut();
                }
            }
        });

        // Arrastrar imagen cuando está zoomada
        document.addEventListener('mousedown', (e) => {
            if (this.currentModalPhoto && e.target.classList.contains('modal-image') && this.zoomLevel > 1) {
                this.isDragging = true;
                this.dragStart = { x: e.clientX - this.imagePosition.x, y: e.clientY - this.imagePosition.y };
                e.preventDefault();
            }
        });

        document.addEventListener('mousemove', (e) => {
            if (this.isDragging && this.currentModalPhoto) {
                this.imagePosition = {
                    x: e.clientX - this.dragStart.x,
                    y: e.clientY - this.dragStart.y
                };
                this.applyZoom();
            }
        });

        document.addEventListener('mouseup', () => {
            this.isDragging = false;
        });

        // Soporte para gestos táctiles
        let initialDistance = 0;
        let initialZoom = 1;

        document.addEventListener('touchstart', (e) => {
            if (this.currentModalPhoto && e.target.classList.contains('modal-image')) {
                if (e.touches.length === 2) {
                    // Zoom con dos dedos
                    initialDistance = Math.hypot(
                        e.touches[0].clientX - e.touches[1].clientX,
                        e.touches[0].clientY - e.touches[1].clientY
                    );
                    initialZoom = this.zoomLevel;
                } else if (e.touches.length === 1 && this.zoomLevel > 1) {
                    // Arrastrar con un dedo
                    this.isDragging = true;
                    this.dragStart = { 
                        x: e.touches[0].clientX - this.imagePosition.x, 
                        y: e.touches[0].clientY - this.imagePosition.y 
                    };
                }
            }
        });

        document.addEventListener('touchmove', (e) => {
            if (this.currentModalPhoto && e.target.classList.contains('modal-image')) {
                e.preventDefault();
                
                if (e.touches.length === 2) {
                    // Zoom con dos dedos
                    const currentDistance = Math.hypot(
                        e.touches[0].clientX - e.touches[1].clientX,
                        e.touches[0].clientY - e.touches[1].clientY
                    );
                    
                    const scale = currentDistance / initialDistance;
                    this.zoomLevel = Math.max(0.5, Math.min(3, initialZoom * scale));
                    this.applyZoom();
                    this.updateZoomButtons();
                } else if (e.touches.length === 1 && this.isDragging) {
                    // Arrastrar con un dedo
                    this.imagePosition = {
                        x: e.touches[0].clientX - this.dragStart.x,
                        y: e.touches[0].clientY - this.dragStart.y
                    };
                    this.applyZoom();
                }
            }
        });

        document.addEventListener('touchend', () => {
            this.isDragging = false;
            initialDistance = 0;
        });
    }

    openModal(photoName) {
        this.currentModalPhoto = photoName;
        this.resetZoom(); // Resetear zoom al abrir nueva foto
        const year = photoName.replace(/\.[^/.]+$/, "");
        
        // Mostrar "Foto" para 2000 y 2001, "Graduación" para el resto
        let titlePrefix = "Graduación";
        if (year === "2000" || year === "2001") {
            titlePrefix = "Foto";
        }
        
        const caras = this.facesData[photoName];
        
        // Configurar título
        document.getElementById('modal-title').textContent = `${titlePrefix} ${year}`;
        
        // Configurar imagen y caras
        const modalContainer = document.getElementById('modal-image-container');
        modalContainer.innerHTML = `
            <img src="public/${photoName}" alt="${titlePrefix} ${year}" class="modal-image" 
                 onload="app.onModalImageLoad(this, '${photoName}')">
            ${this.createModalFaceBoxes(caras)}
        `;
        
        // Actualizar estado de botones de navegación
        this.updateNavigationButtons();
        
        // Mostrar modal
        document.getElementById('modal').style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
    }

    updateNavigationButtons() {
        const photos = Object.keys(this.facesData).sort();
        const currentIndex = photos.indexOf(this.currentModalPhoto);
        
        const prevButton = document.querySelector('.nav-prev');
        const nextButton = document.querySelector('.nav-next');
        
        // Deshabilitar botón anterior si estamos en la primera foto
        if (currentIndex <= 0) {
            prevButton.classList.add('disabled');
        } else {
            prevButton.classList.remove('disabled');
        }
        
        // Deshabilitar botón siguiente si estamos en la última foto
        if (currentIndex >= photos.length - 1) {
            nextButton.classList.add('disabled');
        } else {
            nextButton.classList.remove('disabled');
        }
    }

    createModalFaceBoxes(caras) {
        return caras.map(cara => {
            // Solo mostrar tooltip si hay nombre, sino no crear la caja
            if (!cara.nombre || cara.nombre.trim() === '') {
                return '';
            }
            // Las coordenadas serán escaladas en scaleModalFaces
            return `
                <div class="modal-face-box" 
                     style="left: ${cara.x}px; top: ${cara.y}px; width: ${cara.w}px; height: ${cara.h}px; display: flex; align-items: flex-start; justify-content: center;">
                    <div class="modal-face-tooltip" style="left: 50%; top: -60px; transform: translateX(-50%); white-space: nowrap;">${cara.nombre}</div>
                </div>
            `;
        }).join('');
    }

    onModalImageLoad(img, photoName) {
        // Ajustar las posiciones de las caras en el modal
        const caras = this.facesData[photoName];
        const container = img.parentElement;
        const faceBoxes = container.querySelectorAll('.modal-face-box');
        
        // Esperar a que la imagen se cargue completamente
        if (img.complete) {
            this.scaleModalFaces(img, photoName, faceBoxes);
        } else {
            img.onload = () => {
                this.scaleModalFaces(img, photoName, faceBoxes);
            };
        }
    }

    scaleModalFaces(img, photoName, faceBoxes) {
        const caras = this.facesData[photoName];
        // Obtener las dimensiones reales de la imagen en el modal
        const imgRect = img.getBoundingClientRect();
        const containerRect = img.parentElement.getBoundingClientRect();
        // Calcular las coordenadas relativas al contenedor del modal
        const imgLeft = imgRect.left - containerRect.left;
        const imgTop = imgRect.top - containerRect.top;
        const originalWidth = img.naturalWidth;
        const originalHeight = img.naturalHeight;
        const displayWidth = imgRect.width;
        const displayHeight = imgRect.height;
        const scaleX = displayWidth / originalWidth;
        const scaleY = displayHeight / originalHeight;
        // Solo procesar caras que tienen nombre
        const carasConNombre = caras.filter(cara => cara.nombre && cara.nombre.trim() !== '');
        faceBoxes.forEach((box, index) => {
            const cara = carasConNombre[index];
            if (cara) {
                // Calcular las coordenadas escaladas relativas al contenedor
                const scaledX = (cara.x * scaleX) + imgLeft;
                const scaledY = (cara.y * scaleY) + imgTop;
                const scaledW = cara.w * scaleX;
                const scaledH = cara.h * scaleY;
                box.style.left = `${scaledX}px`;
                box.style.top = `${scaledY}px`;
                box.style.width = `${scaledW}px`;
                box.style.height = `${scaledH}px`;
                // Aplicar transformación inicial si hay zoom activo
                if (this.zoomLevel !== 1 || this.imagePosition.x !== 0 || this.imagePosition.y !== 0) {
                    const transform = `translate(${this.imagePosition.x}px, ${this.imagePosition.y}px) scale(${this.zoomLevel})`;
                    box.style.transform = transform;
                    // También aplicar el mismo transform al tooltip
                    const tooltip = box.querySelector('.modal-face-tooltip');
                    if (tooltip) {
                        tooltip.style.transform = `translateX(-50%) scale(${1/this.zoomLevel})`;
                    }
                } else {
                    // Resetear el transform del tooltip si no hay zoom
                    const tooltip = box.querySelector('.modal-face-tooltip');
                    if (tooltip) {
                        tooltip.style.transform = 'translateX(-50%)';
                    }
                }
            }
        });
    }

    closeModal() {
        document.getElementById('modal').style.display = 'none';
        document.body.style.overflow = 'auto'; // Restaurar scroll
        this.currentModalPhoto = null;
        this.resetZoom();
    }

    previousPhoto() {
        if (!this.currentModalPhoto) return;
        
        const photos = Object.keys(this.facesData).sort();
        const currentIndex = photos.indexOf(this.currentModalPhoto);
        
        if (currentIndex > 0) {
            const previousPhoto = photos[currentIndex - 1];
            this.openModal(previousPhoto);
        }
    }

    nextPhoto() {
        if (!this.currentModalPhoto) return;
        
        const photos = Object.keys(this.facesData).sort();
        const currentIndex = photos.indexOf(this.currentModalPhoto);
        
        if (currentIndex < photos.length - 1) {
            const nextPhoto = photos[currentIndex + 1];
            this.openModal(nextPhoto);
        }
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showError() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').style.display = 'block';
    }

    zoomIn() {
        if (this.zoomLevel < 3) {
            this.zoomLevel += 0.5;
            this.applyZoom();
        }
        this.updateZoomButtons();
    }

    zoomOut() {
        if (this.zoomLevel > 0.5) {
            this.zoomLevel -= 0.5;
            this.applyZoom();
        }
        this.updateZoomButtons();
    }

    resetZoom() {
        this.zoomLevel = 1;
        this.imagePosition = { x: 0, y: 0 };
        this.applyZoom();
        this.updateZoomButtons();
        
        // Resetear completamente las transformaciones de las cajas de caras
        const faceBoxes = document.querySelectorAll('.modal-face-box');
        faceBoxes.forEach(box => {
            box.style.transform = 'none';
        });
    }

    applyZoom() {
        const modalImage = document.querySelector('.modal-image');
        const faceBoxes = document.querySelectorAll('.modal-face-box');
        
        if (modalImage) {
            const transform = `translate(${this.imagePosition.x}px, ${this.imagePosition.y}px) scale(${this.zoomLevel})`;
            modalImage.style.transform = transform;
            
            // Ocultar cajas de caras cuando hay zoom
            faceBoxes.forEach((box, index) => {
                if (this.zoomLevel !== 1) {
                    box.style.display = 'none';
                } else {
                    box.style.display = '';
                    box.style.transform = 'none';
                }
            });
            
            // Actualizar cursor
            if (this.zoomLevel > 1) {
                modalImage.classList.add('zoomed');
            } else {
                modalImage.classList.remove('zoomed');
            }
        }
    }

    updateZoomButtons() {
        const zoomInBtn = document.querySelector('.zoom-btn[onclick="app.zoomIn()"]');
        const zoomOutBtn = document.querySelector('.zoom-btn[onclick="app.zoomOut()"]');
        
        if (zoomInBtn) {
            zoomInBtn.disabled = this.zoomLevel >= 3;
        }
        if (zoomOutBtn) {
            zoomOutBtn.disabled = this.zoomLevel <= 0.5;
        }
    }
}

// Inicializar la aplicación cuando se cargue la página
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new GraduacionesApp();
}); 