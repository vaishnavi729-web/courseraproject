const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3000; // Standard Express port for the Capstone Project

app.use(cors());
app.use(express.json());
app.use(require('body-parser').urlencoded({ extended: false }));

// Load local JSON data
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'))['reviews'] || [];
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'))['dealerships'] || [];

// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Dealership API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
    res.json(reviews_data);
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    const dealerReviews = reviews_data.filter(r => r.dealership == req.params.id);
    res.json(dealerReviews.length > 0 ? dealerReviews : reviews_data);
});

// Express route to fetch all dealerships (Task 9)
app.get('/fetchDealers', async (req, res) => {
    res.json(dealerships_data);
});

// Express route to fetch Dealers by a particular state (Task 11)
app.get('/fetchDealers/:state', async (req, res) => {
    const stateDealers = dealerships_data.filter(d => d.state.toLowerCase() === req.params.state.toLowerCase());
    res.json(stateDealers.length > 0 ? stateDealers : dealerships_data);
});

// Express route to fetch dealer by a particular id (Task 10)
app.get('/fetchDealer/:id', async (req, res) => {
    const dealer = dealerships_data.find(d => d.id == req.params.id);
    if (dealer) {
        res.json(dealer);
    } else {
        res.status(404).json({ error: 'Dealer not found' });
    }
});
// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
    try {
        const data = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
        const new_id = reviews_data.length > 0 ? Math.max(...reviews_data.map(r => r.id)) + 1 : 1;

        const newReview = {
            id: new_id,
            name: data.name,
            dealership: data.dealership,
            review: data.review,
            purchase: data.purchase,
            purchase_date: data.purchase_date,
            car_make: data.car_make,
            car_model: data.car_model,
            car_year: data.car_year,
        };

        reviews_data.push(newReview);
        res.json(newReview);
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: 'Error inserting review' });
    }
});

app.get('/analyze/:text', async (req, res) => {
    try {
        const text = encodeURIComponent(req.params.text);
        const response = await fetch(
            `http://127.0.0.1:5050/analyze/${text}`
        );

        const result = await response.json();
        res.status(response.status).json(result);
    } catch (error) {
        console.error('Sentiment analysis failed:', error.message);
        res.status(502).json({
            error: 'Sentiment analyzer unavailable'
        });
    }
});

// Start the Express server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});