let allRecords = [];
const grid = document.getElementById('productGrid');
const searchInput = document.getElementById('searchInput');
const recGrid = document.getElementById('recommendationGrid');

function renderProducts(data) {
    grid.innerHTML = ""; 
    if (data.length === 0) {
        grid.innerHTML = "<p>Нічого не знайдено :(</p>";
        return;
    }

    data.forEach(item => {
        const card = document.createElement('div');
        card.className = 'record-card';
        
        card.innerHTML = `
            <a href="album.html?id=${item.id}" style="display: block; text-decoration: none; color: inherit;">
            <div class="image-container" style="background-image: url('${item.image_url}'); width: 100%; height: 250px; background-size: cover; background-position: center;"></div>
            <div class="info" style="padding: 15px;">
                <span class="genre-tag">${item.genre || 'Vinyl'}</span>
                <h3 class="card-title" style="margin: 10px 0;">${item.title}</h3>
                <p class="card-artist" style="margin: 0 0 15px 0;">${item.artist}</p>
            </div>
            </a>
            <div class="card-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 0 15px 15px 15px;">
                <span class="price" style="font-weight: bold; font-size: 1.2em;">$${item.price}</span>
                <button class="add-btn" onclick="addToCart(${item.id})">У кошик</button>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderRecommendations(data) {
    if (!recGrid) return;
    
    recGrid.innerHTML = "";
    const recommended = data.slice(0, 2); 

    recommended.forEach(item => {
        const card = document.createElement('div');
        card.className = 'record-card';
        card.innerHTML = `
            <a href="album.html?id=${item.id}" style="display: block; text-decoration: none; color: inherit;">
                <div class="image-container" style="background-image: url('${item.image_url}'); width: 100%; height: 200px; background-size: cover; background-position: center; transition: opacity 0.3s;" onmouseover="this.style.opacity=0.8" onmouseout="this.style.opacity=1"></div>
                <div class="info" style="padding: 15px;">
                    <span class="genre-tag" style="background: gold; padding: 2px 5px; border-radius: 3px; font-size: 0.8em; color: black; font-weight: bold;">Top Pick</span>
                    <h3 class="card-title" style="margin: 10px 0;">${item.title}</h3>
                    <p class="card-artist" style="margin: 0;">${item.artist}</p>
                </div>
            </a>
        `;
        recGrid.appendChild(card);
    });
}

async function fetchVinyls() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/records');
        allRecords = await response.json();
        renderProducts(allRecords);
        renderRecommendations(allRecords);

    } catch (error) {
        console.error('Помилка завантаження:', error);
        grid.innerHTML = "<p>Помилка з'єднання з сервером.</p>";
    }
}

const catalogSection = document.querySelector('.catalog');
const recSection = document.querySelector('.recommendations');

if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase().trim();
        const filteredProducts = allRecords.filter(item => {
            return (
                item.title.toLowerCase().includes(searchTerm) ||
                item.artist.toLowerCase().includes(searchTerm) ||
                (item.genre && item.genre.toLowerCase().includes(searchTerm))
            );
        });

        renderProducts(filteredProducts);
        if (catalogSection && recSection) {
            if (searchTerm !== "") {
                catalogSection.style.order = "-1";
                if (filteredProducts.length === 0) {
                    recSection.style.display = "none";
                } else {
                    recSection.style.display = "block";
                }
            } else {
                catalogSection.style.order = "0";
                recSection.style.display = "block"; 
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', fetchVinyls);