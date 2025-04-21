function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// Helper to extract place_id from URL (works for both ?place_id and ?id)
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id') || params.get('id');
}

// Logout: clear token and redirect
function logout() {
  document.cookie = 'token=; Max-Age=0; path=/';
  window.location.href = 'index.html';
}

// Main entry
document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');

  // LOGIN PAGE
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async event => {
      event.preventDefault();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      if (!email || !password) {
        alert('Please enter both email and password.');
        return;
      }
      try {
        const resp = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        if (!resp.ok) {
          const err = await resp.json();
          throw new Error(err.message || resp.statusText);
        }
        const data = await resp.json();
        document.cookie = `token=${data.access_token}; path=/;`;
        window.location.href = 'index.html';
      } catch (err) {
        console.error('Login error:', err);
        alert('Login failed: ' + err.message);
      }
    });
    return; // skip other pages
  }

  // COMMON: toggle login/logout links if present
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  if (loginLink) loginLink.style.display = token ? 'none' : 'block';
  if (logoutLink) {
    logoutLink.style.display = token ? 'block' : 'none';
    logoutLink.addEventListener('click', logout);
  }

  // ADD REVIEW PAGE
  const addReviewForm = document.getElementById('review-form');
  if (addReviewForm) {
    if (!token) {
      window.location.href = 'index.html';
      return;
    }
    const placeId = getPlaceIdFromURL();
    addReviewForm.addEventListener('submit', async e => {
      e.preventDefault();
      const text = document.getElementById('review-text').value.trim();
      const rating = parseInt(document.getElementById('rating').value);
      if (!text) { alert('Please enter a review.'); return; }
      try {
        const resp = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ text, rating, place_id: placeId })
        });
        if (!resp.ok) {
          const err = await resp.json();
          throw new Error(err.error || resp.statusText);
        }
        alert('Review submitted successfully!');
        addReviewForm.reset();
      } catch (err) {
        console.error('Review submit error:', err);
        alert('Failed to submit review: ' + err.message);
      }
    });
    return;
  }

  // PLACE DETAILS PAGE
  const placeDetailsSection = document.getElementById('place-details');
  if (placeDetailsSection) {
    const placeId = getPlaceIdFromURL();
    if (!placeId) return;

    // Inline "Add Review" form toggle
    const inlineFormSection = document.getElementById('add-review-section');
    if (inlineFormSection) inlineFormSection.style.display = token ? 'block' : 'none';

    // "Add Your Review" button link
    const addLink = document.querySelector('.add-review-button');
    if (addLink) addLink.href = `add_review.html?place_id=${placeId}`;

    // Fetch and display place + reviews
    fetchPlaceDetails(placeId, token);
    fetchReviews(placeId, token);
    return;
  }

  // INDEX PAGE
  // Price filter setup
  const priceFilter = document.getElementById('max-price');
  if (priceFilter) {
    ['All','10','50','100'].forEach(val => {
      const opt = document.createElement('option'); opt.value = val; opt.textContent = val;
      priceFilter.appendChild(opt);
    });
    priceFilter.addEventListener('change', () => {
      const max = priceFilter.value;
      document.querySelectorAll('.place-card').forEach(card => {
        const price = parseFloat(card.dataset.price);
        card.style.display = (max==='All'||price<=parseFloat(max))?'block':'none';
      });
    });
  }

  // Fetch and display places
  if (token) fetchPlaces(token);
});

// ===== API calls & renderers =====

async function fetchPlaces(token) {
  try {
    const resp = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!resp.ok) throw new Error(resp.statusText);
    const places = await resp.json();
    displayPlaces(places);
  } catch (err) {
    console.error('Fetch places error:', err);
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = '';
  places.forEach(p => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.dataset.price = p.price;
    div.innerHTML = `
      <h3>${p.title}</h3>
      <p>${p.description}</p>
      <p>Location: (${p.latitude}, ${p.longitude})</p>
      <p>Price: $${p.price}</p>
      <button data-place-id="${p.id}" class="view-details-btn">View Details</button>
    `;
    container.appendChild(div);
  });
  document.querySelectorAll('.view-details-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      window.location.href = `place.html?place_id=${btn.dataset.placeId}`;
    });
  });
}

async function fetchPlaceDetails(placeId, token) {
  try {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const resp = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });
    if (!resp.ok) throw new Error(resp.statusText);
    const data = await resp.json();
    
    // We need to fetch the user separately using the user_id from the place data
    if (token && data.place.user_id) {
      try {
        const userResp = await fetch(`http://127.0.0.1:5000/api/v1/users/${data.place.user_id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (userResp.ok) {
          const userData = await userResp.json();
          const hostName = `${userData.first_name} ${userData.last_name}`;
          renderPlaceDetails(data.place, data.associated_amenities, hostName);
          return;
        }
      } catch (userErr) {
        console.error('Failed to fetch host details:', userErr);
      }
    }
    
    // If we couldn't get the user data or don't have a token
    renderPlaceDetails(data.place, data.associated_amenities, "Unknown Host");
  } catch (err) {
    console.error('Fetch place details error:', err);
  }
}

function renderPlaceDetails(place, amenities, hostName) {
  document.getElementById('place-name').textContent = place.title;
  const sec = document.getElementById('place-details');
  sec.innerHTML = `
    <p><strong>Host:</strong> ${hostName}</p>
    <p>${place.description}</p>
    <p><strong>Price:</strong> $${place.price}</p>
    <p><strong>Location:</strong> (${place.latitude}, ${place.longitude})</p>
    <h3>Amenities:</h3>
    <ul>${amenities.map(a => `<li>${a}</li>`).join('')}</ul>
  `;
}

async function fetchReviews(placeId, token) {
  try {
    const resp = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });
    if (!resp.ok) throw new Error(resp.statusText);
    const reviews = await resp.json();
    renderReviews(reviews);
  } catch (err) {
    console.error('Fetch reviews error:', err);
  }
}

function renderReviews(reviews) {
  const cont = document.getElementById('reviews-container');
  if (!cont) return;
  cont.innerHTML = '';
  if (!reviews.length) {
    cont.textContent = 'No reviews yet.';
    return;
  }
  reviews.forEach(r => {
    const div = document.createElement('div');
    div.className = 'review';
    const stars = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
    div.innerHTML = `<p><strong>${stars}</strong> ${r.text}</p>`;
    cont.appendChild(div);
  });
}