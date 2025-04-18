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
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({ email, password })
              });

              if (response.ok) {
                  const data = await response.json();
                  // Save token in a cookie
                  document.cookie = `token=${data.access_token}; path=/;`;

                  // Redirect to main page
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

  checkAuthentication();

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
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
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

async function fetchPlaces(token) {
  try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
          method: 'GET',
          headers: {
              'Authorization': `Bearer ${token}`
          }
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

let allPlaces = []; // store all places globally for filtering later

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;

  placesList.innerHTML = ''; // clear previous
  allPlaces = places; // store for filtering

  places.forEach(place => {
      const placeDiv = document.createElement('div');
      placeDiv.className = 'place-card';
      placeDiv.dataset.price = place.price; // for filtering

      placeDiv.innerHTML = `
          <h3>${place.title}</h3>
          <p>${place.description}</p>
          <p>Location: (${place.latitude}, ${place.longitude})</p>
          <p>Price: $${place.price}</p>
          <button class="view-details-btn" data-place-id="${place.id}">View Details</button>
      `;
      placesList.appendChild(placeDiv);
  });

  // Add click event listeners after the places are added
  const viewDetailsButtons = document.querySelectorAll('.view-details-btn');
  viewDetailsButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      const placeId = event.target.dataset.placeId;
      // Redirect to place.html with the place id as query param
      window.location.href = `place.html?place_id=${placeId}`;
    });
  });
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

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function checkAuthentication(placeId) {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review-section');

  if (!token) {
      addReviewSection.style.display = 'none';
  } else {
      addReviewSection.style.display = 'block';
  }
  fetchPlaceDetails(token, placeId); // Always fetch place details
}

async function fetchPlaceDetails(token, placeId) {
  try {
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
          method: 'GET',
          headers: headers
      });

      if (!response.ok) {
          throw new Error('Failed to fetch place details');
      }

      const place = await response.json();
      displayPlaceDetails(place);
  } catch (error) {
      console.error('Error fetching place details:', error);
  }
}

function displayPlaceDetails(place) {
  const placeName = document.getElementById('place-name');
  const placeDetailsSection = document.getElementById('place-details');
  const reviewsContainer = document.getElementById('reviews-container');

  // Update place name
  placeName.textContent = place.title;

  // Clear old content
  placeDetailsSection.innerHTML = '';
  reviewsContainer.innerHTML = '';

  // Create elements for place details
  const description = document.createElement('p');
  description.textContent = place.description;

  const price = document.createElement('p');
  price.innerHTML = `<strong>Price per night:</strong> $${place.price}`;

  const location = document.createElement('p');
  location.innerHTML = `<strong>Location:</strong> (${place.latitude}, ${place.longitude})`;

  const amenitiesTitle = document.createElement('h3');
  amenitiesTitle.textContent = 'Amenities:';

  const amenitiesList = document.createElement('ul');
  if (place.amenities && place.amenities.length > 0) {
      place.amenities.forEach(amenity => {
          const li = document.createElement('li');
          li.textContent = amenity.name;
          amenitiesList.appendChild(li);
      });
  } else {
      const li = document.createElement('li');
      li.textContent = 'No amenities listed.';
      amenitiesList.appendChild(li);
  }

  // Append to place details section
  placeDetailsSection.appendChild(description);
  placeDetailsSection.appendChild(price);
  placeDetailsSection.appendChild(location);
  placeDetailsSection.appendChild(amenitiesTitle);
  placeDetailsSection.appendChild(amenitiesList);

  // Display Reviews
  if (place.reviews && place.reviews.length > 0) {
      place.reviews.forEach(review => {
          const reviewDiv = document.createElement('div');
          reviewDiv.classList.add('review-item');

          const reviewText = document.createElement('p');
          reviewText.textContent = `"${review.text}"`;

          const reviewer = document.createElement('small');
          reviewer.textContent = `by ${review.user_email || "Anonymous"}`;

          reviewDiv.appendChild(reviewText);
          reviewDiv.appendChild(reviewer);

          reviewsContainer.appendChild(reviewDiv);
      });
  } else {
      const noReviews = document.createElement('p');
      noReviews.textContent = 'No reviews yet.';
      reviewsContainer.appendChild(noReviews);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  if (placeId) {
      checkAuthentication(placeId);
  } else {
      console.error('No place ID found in URL');
  }
});