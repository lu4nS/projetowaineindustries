document.addEventListener('DOMContentLoaded', () => {

    console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    // Modal de relatórios
    const reportsModal = document.getElementById('reports-modal');
    const imagesModal = document.getElementById('images-modal');
    const closeBtns = document.querySelectorAll('.close-btn');
    // Modal de relatórios
    const reportContentModal = document.getElementById('report-content-modal');
    const reportContent = document.getElementById('report-content');

    document.querySelectorAll('.reports-btn').forEach(button => {
        button.addEventListener('click', () => {
            reportsModal.classList.add('active');
        });
    });

    document.querySelectorAll('.images-btn').forEach(button => {
        button.addEventListener('click', () => {
            imagesModal.classList.add('active');
        });
    });


    // Lógica do carrossel de imagens
    const carouselImages = [
        "/static/images/image1.jpg",
        "/static/images/image2.jpg",
        "/static/images/image3.jpg"
    ];
    let currentImageIndex = 0;

    const carouselImage = document.getElementById('carousel-image');
    const prevImageBtn = document.getElementById('prev-image');
    const nextImageBtn = document.getElementById('next-image');

    prevImageBtn.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex - 1 + carouselImages.length) % carouselImages.length;
        carouselImage.src = carouselImages[currentImageIndex];
    });

    nextImageBtn.addEventListener('click', () => {
        currentImageIndex = (currentImageIndex + 1) % carouselImages.length;
        carouselImage.src = carouselImages[currentImageIndex];
    });

    // Fecha o modal de imagens ao clicar fora
    imagesModal.addEventListener('click', (e) => {
        if (e.target === imagesModal) imagesModal.classList.remove('active');
    });



    document.querySelectorAll('.document-item').forEach(item => {
        item.addEventListener('click', async () => {
            try {
                const response = await fetch('/static/text/loremipsum.txt');
                const text = await response.text();
                const reportContent = document.getElementById('report-content');
                reportContent.textContent = text;
                const reportContentModal = document.getElementById('report-content-modal');
                reportContentModal.classList.add('active');
            } catch (error) {
                console.error('Erro ao carregar o texto:', error);
            }
        });
    });

    // Fechar modais ao clicar fora
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });


    // Fechar modais
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            reportsModal.classList.remove('active');
            reportContentModal.classList.remove('active');
        });
    });
});

