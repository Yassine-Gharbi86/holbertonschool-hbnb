document.addEventListener('DOMContentLoaded', () => {
  // Form handlers
  const loginForm = document.getElementById('login-form');
  const addReviewForm = document.getElementById('add-review-form');
  const reviewForm = document.getElementById('review-form');

  // Initialize based on current page
  if (loginForm) loginForm.addEventListener('submit', handleLogin);
  if (addReviewForm) addReviewForm.addEventListener('submit', handleReviewSubmit);
  if (reviewForm) reviewForm.addEventListener('submit', handleReviewSubmit);

  const placeId = getPlaceIdFromURL();
  
  if (placeId) {
    checkAuthenticationPlaceDetails(placeId);
    loadReviews(placeId);
  } else {
    checkAuthentication();
    setupPriceFilter();
  }
});

// ======================
// AUTHENTICATION HANDLERS
// ======================

async function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!email || !password) {
    alert('Please enter both email and password.');
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/;`;
      window.location.href = 'index.html';
    } else {
      const errorData = await response.json();
      alert('Login failed: ' + (errorData.message || response.statusText));
    }
  } catch (error) {
    console.error('Login error:', error);
    alert('An error occurred. Please try again.');
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
  } else {
    if (loginLink) loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

// ======================
// REVIEW FUNCTIONALITY
// ======================

async function handleReviewSubmit(event) {
  event.preventDefault();
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();

  if (!token) {
    alert('Please login to submit a review.');
    window.location.href = `login.html?redirect=${encodeURIComponent(window.location.href)}`;
    return;
  }

  const reviewText = document.getElementById('review-text').value.trim();
  const rating = document.getElementById('rating').value;

  if (!reviewText || !rating) {
    alert('Please fill in all review fields.');
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        text: reviewText,
        rating: parseInt(rating),
        place_id: placeId
      })
    });

    if (response.ok) {
      window.location.href = `place.html?place_id=${placeId}`;
    } else {
      const errorData = await response.json();
      alert('Review submission failed: ' + (errorData.message || response.statusText));
    }
  } catch (error) {
    console.error('Review error:', error);
    alert('Failed to submit review. Please try again.');
  }
}

async function loadReviews(placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`);
    
    if (response.ok) {
      const reviews = await response.json();
      displayReviews(reviews);
    }
  } catch (error) {
    console.error('Error loading reviews:', error);
  }
}

function displayReviews(reviews) {
  const container = document.getElementById('reviews-container');
  if (!container) return;

  container.innerHTML = '';

  if (reviews.length === 0) {
    container.innerHTML = '<p>No reviews yet. Be the first to write one!</p>';
    return;
  }

  reviews.forEach(review => {
    const reviewElement = document.createElement('div');
    reviewElement.className = 'review-card';
    reviewElement.innerHTML = `
      <div class="review-header">
        <span class="review-rating">${'★'.repeat(review.rating)}</span>
        <span class="review-date">${new Date().toLocaleDateString()}</span>
      </div>
      <p class="review-text">${review.text}</p>
    `;
    container.appendChild(reviewElement);
  });
}

// ======================
// PLACE FUNCTIONALITY
// ======================

async function fetchPlaceDetails(token, placeId) {
  try {
    const [placeResponse, reviewsResponse] = await Promise.all([
      fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
      }),
      fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`)
    ]);

    const placeData = await placeResponse.json();
    const reviews = await reviewsResponse.json();

    displayPlaceDetails(placeData, token);
    displayReviews(reviews);
  } catch (error) {
    console.error('Error loading place details:', error);
  }
}

async function displayPlaceDetails(placeData, token) {
  const place = placeData.place;
  const amenities = placeData.associated_amenities || [];
  const container = document.getElementById('place-details');

  if (!container) return;

  const ownerName = await fetchUserName(place.user_id, token);
  
  container.innerHTML = `
    <div class="place-detail-card">
      <h2>${place.title}</h2>
      <p class="owner"><strong>Owner:</strong> ${ownerName}</p>
      <p class="description">${place.description}</p>
      <div class="details-grid">
        <div class="detail-item">
          <span class="label">Price:</span>
          <span class="value">$${place.price}/night</span>
        </div>
        <div class="detail-item">
          <span class="label">Location:</span>
          <span class="value">${place.latitude}, ${place.longitude}</span>
        </div>
      </div>
      <div class="amenities-section">
        <h3>Amenities</h3>
        <ul class="amenities-list">
          ${amenities.map(amenity => `<li>${amenity}</li>`).join('') || '<li>No amenities listed</li>'}
        </ul>
      </div>
    </div>
  `;
}

// ======================
// HELPER FUNCTIONS
// ======================

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(';').shift() : null;
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
}

async function fetchUserName(userId, token) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const user = await response.json();
    return `${user.first_name} ${user.last_name}`;
  } catch (error) {
    console.error('Error fetching user:', error);
    return 'Unknown Owner';
  }
}

// ======================
// PLACE LISTING FUNCTIONALITY
// ======================

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;

  container.innerHTML = '';
  allPlaces = places;

  places.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    placeCard.dataset.price = place.price;
    placeCard.innerHTML = `
      <h3>${place.title}</h3>
      <p>${place.description}</p>
      <div class="place-meta">
        <span class="price">$${place.price}/night</span>
        <button class="view-details-btn" data-place-id="${place.id}">View Details</button>
      </div>
    `;
    container.appendChild(placeCard);
  });

  document.querySelectorAll('.view-details-btn').forEach(button => {
    button.addEventListener('click', (e) => {
      window.location.href = `place.html?place_id=${e.target.dataset.placeId}`;
    });
  });
}

// ======================
// PRICE FILTER FUNCTIONALITY
// ======================

function setupPriceFilter() {
  const filter = document.getElementById('max-price');
  if (!filter) return;

  const prices = ['All', '50', '100', '150', '200', '250'];
  prices.forEach(price => {
    const option = document.createElement('option');
    option.value = price;
    option.textContent = `$${price}+`;
    filter.appendChild(option);
  });

  filter.addEventListener('change', filterPlaces);
}

function filterPlaces(event) {
  const maxPrice = event.target.value;
  const places = document.querySelectorAll('.place-card');

  places.forEach(place => {
    const price = parseFloat(place.dataset.price);
    if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
      place.style.display = 'block';
    } else {
      place.style.display = 'none';
    }
  });
}