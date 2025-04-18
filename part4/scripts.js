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
      `;
      placesList.appendChild(placeDiv);
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