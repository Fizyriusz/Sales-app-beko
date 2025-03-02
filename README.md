# Sales-app-beko
source ~/env/bin/activate
python manage.py runserver

sadsa
/* Resetowanie i ogólne style */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    background-color: #f4f4f4;
}

/* Nagłówek */
.header {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    background-color: #2c3e50;
    color: #ffffff;
    height: 60px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.header h1 {
    font-size: 32px;
    margin: 0;
    font-weight: bold;
    text-align: center;
    flex-grow: 1;
}

.hamburger {
    position: absolute;
    left: 10px;
    font-size: 20px;
    background: none;
    border: none;
    color: white;
    cursor: pointer;
}

/* Sidebar */
.sidebar {
    position: fixed;
    left: 0;
    top: 60px;
    width: 250px;
    height: calc(100vh - 60px);
    background-color: #2c3e50;
    color: white;
    padding: 15px;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
    overflow-y: auto;
    z-index: 1001;
}

.sidebar.open {
    transform: translateX(0);
}

.sidebar ul {
    list-style-type: none;
    padding: 0;
}

.sidebar ul li {
    margin: 10px 0;
}

.sidebar ul li a {
    color: white;
    text-decoration: none;
    display: block;
    padding: 10px;
    background-color: #34495e;
    border-radius: 5px;
    text-align: center;
}

.sidebar ul li a:hover {
    background-color: #1abc9c;
}

/* Overlay dla sidebaru */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: none;
}

.overlay.active {
    display: block;
}

/* Główna zawartość */
.main-content {
    margin-top: 60px;
    padding: 20px;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    max-width: 800px;
    margin: 50px auto;
}

/* Linki w głównej zawartości */
.main-content ul li a {
    color: #2c3e50;
    font-weight: bold;
    text-decoration: none;
    transition: color 0.3s ease, background-color 0.3s ease;
    display: inline-block;
    padding: 5px 10px;
    border-radius: 5px;
}

.main-content ul li a:hover {
    background-color: #1abc9c;
    color: white;
}

/* Linki główne */
.main-links ul {
    list-style: none;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 20px; /* Odstęp między przyciskami */
    justify-content: center; /* Wyśrodkowanie przycisków */
    margin-top: 20px; /* Dodatkowy odstęp od góry */
}

.main-links ul li {
    flex: 1 1 calc(33.333% - 20px); /* Trzy przyciski w rzędzie */
    display: flex;
    justify-content: center;
}

.main-links ul li a {
    display: block;
    padding: 15px 20px;
    text-align: center;
    text-decoration: none;
    font-weight: bold;
    font-size: 1rem;
    color: #ffffff; /* Biały tekst */
    background-color: #1abc9c; /* Zielony kolor przycisków */
    border-radius: 10px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); /* Subtelny cień */
    transition: all 0.3s ease;
}

.main-links ul li a:hover {
    background-color: #16a085; /* Ciemniejszy zielony przy najechaniu */
    transform: translateY(-2px); /* Subtelne uniesienie */
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Mocniejszy cień */
}


/* Sales Summary Section */
.sales-summary {
    margin-top: 20px;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

.sales-summary h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #34495e;
}

/* Cards Layout */
.cards-container {
    display: flex;
    justify-content: space-around;
    gap: 20px;
}

.card {
    flex: 1;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card h3 {
    margin-bottom: 10px;
    color: #2c3e50;
}

.card .amount {
    font-size: 2rem;
    font-weight: bold;
    color: #1abc9c;
}

/* Responsive Design */
@media (max-width: 768px) {
    .cards-container {
        flex-direction: column;
        align-items: center;
    }
    .main-links ul {
        flex-direction: column; /* Przyciski w jednej kolumnie */
        gap: 10px; /* Mniejsze odstępy */
    }

    .main-links ul li {
        flex: 1 1 100%; /* Przyciski zajmują całą szerokość */
    }

    .main-links ul li a {
        font-size: 0.9rem; /* Mniejszy tekst */
        padding: 12px; /* Mniejsze marginesy wewnętrzne */
    }

    .card {
        width: 90%;
        margin-bottom: 20px;
    }

    .sidebar.open {
        width: 80%;
        height: 100%;
        top: 0;
        background-color: rgba(44, 62, 80, 0.95);
    }

    .overlay.active {
        display: block;
    }
}
