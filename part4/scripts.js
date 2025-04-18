document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
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
        console.error('Error during login:', error);
        alert('An error occurred. Please try again.');
      }
    });
  }

  const placeId = getPlaceIdFromURL();

  if (placeId) {
    checkAuthenticationPlaceDetails(placeId);
  } else {
    checkAuthentication();
    setupPriceFilter();
  }
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// --- Login and Main Page Logic ---

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

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      console.error('Failed to fetch places:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

let allPlaces = [];

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;

  placesList.innerHTML = '';
  allPlaces = places;

  places.forEach(place => {
    const placeDiv = document.createElement('div');
    placeDiv.className = 'place-card';
    placeDiv.dataset.price = place.price;

    placeDiv.innerHTML = `
      <h3>${place.title}</h3>
      <p>${place.description}</p>
      <p>Location: (${place.latitude}, ${place.longitude})</p>
      <p>Price: $${place.price}</p>
      <button class="view-details-btn" data-place-id="${place.id}">View Details</button>
    `;
    placesList.appendChild(placeDiv);
  });

  const viewDetailsButtons = document.querySelectorAll('.view-details-btn');
  viewDetailsButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      const placeId = event.target.dataset.placeId;
      window.location.href = `place.html?place_id=${placeId}`;
    });
  });
}

function setupPriceFilter() {
  const priceFilter = document.getElementById('max-price');
  if (priceFilter) {
    const prices = ['All', '10', '50', '100'];
    prices.forEach(price => {
      const option = document.createElement('option');
      option.value = price;
      option.textContent = price;
      priceFilter.appendChild(option);
    });

    priceFilter.addEventListener('change', handlePriceFilter);
  }
}

function handlePriceFilter(event) {
  const selectedValue = event.target.value;
  const placeCards = document.querySelectorAll('.place-card');

  placeCards.forEach(card => {
    const placePrice = parseFloat(card.dataset.price);

    if (selectedValue === 'All') {
      card.style.display = 'block';
    } else if (placePrice <= parseFloat(selectedValue)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

// --- Place Details Page Logic ---

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
}

function checkAuthenticationPlaceDetails(placeId) {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review-section');

  if (addReviewSection) {
    if (!token) {
      addReviewSection.style.display = 'none';
    } else {
      addReviewSection.style.display = 'block';
    }
  }

  fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails() {
  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    console.error('Place ID not found in URL');
    return;
  }

  try {
    const token = getCookie('token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });

    if (response.ok) {
      const placeData = await response.json();
      displayPlaceDetails(placeData);
    } else {
      console.error('Failed to fetch place details', await response.json());
    }
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

function displayPlaceDetails(placeData) {
  const placeName = document.getElementById('place-name');
  const placeDetailsSection = document.getElementById('place-details');
  const reviewsContainer = document.getElementById('reviews-container');

  if (!placeName || !placeDetailsSection || !reviewsContainer) return;

  // Since your backend sends flat structure
  placeName.textContent = placeData.title || 'Untitled Place';
  placeDetailsSection.innerHTML = '';
  reviewsContainer.innerHTML = '';

  const description = document.createElement('p');
  description.textContent = placeData.description || 'No description provided.';

  const price = document.createElement('p');
  price.innerHTML = `<strong>Price per night:</strong> $${placeData.price ?? 'N/A'}`;

  const location = document.createElement('p');
  if (placeData.latitude !== undefined && placeData.longitude !== undefined) {
    location.innerHTML = `<strong>Location:</strong> (${placeData.latitude}, ${placeData.longitude})`;
  } else {
    location.innerHTML = `<strong>Location:</strong> Not specified`;
  }

  const amenitiesTitle = document.createElement('h3');
  amenitiesTitle.textContent = 'Amenities:';

  const amenitiesList = document.createElement('ul');
  if (placeData.associated_amenities && placeData.associated_amenities.length > 0) {
    placeData.associated_amenities.forEach(amenityName => {
      const li = document.createElement('li');
      li.textContent = amenityName;
      amenitiesList.appendChild(li);
    });
  } else {
    const li = document.createElement('li');
    li.textContent = 'No amenities listed.';
    amenitiesList.appendChild(li);
  }

  placeDetailsSection.appendChild(description);
  placeDetailsSection.appendChild(price);
  placeDetailsSection.appendChild(location);
  placeDetailsSection.appendChild(amenitiesTitle);
  placeDetailsSection.appendChild(amenitiesList);

  // No reviews because your backend does not return them
  const noReviews = document.createElement('p');
  noReviews.textContent = 'Reviews are not available.';
  reviewsContainer.appendChild(noReviews);
}
