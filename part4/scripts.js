/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
  
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const maxPrice = event.target.value;
            const places = document.querySelectorAll('.place');
            
            places.forEach(place => {
                const placePrice = parseInt(place.dataset.price);
                
                if (maxPrice === 'all' || placePrice <= parseInt(maxPrice)) {
                    place.style.display = 'block';
                } else {
                    place.style.display = 'none';
                }
            });
        });
    }
  
    const loginForm = document.getElementById('login-form');
  
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(loginForm);
            const data = {
                email: formData.get('email'),
                password: formData.get('password')
            };
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
                credentials: 'include'
            });
            if (response.ok) {
                const result = await response.json();
                if (result.access_token) {
                    document.cookie = `token=${result.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed: ' + (result.message || 'Invalid credentials'));
                }
            } else {
                alert('Network error: ' + response.statusText);
            }
          });
    }
  });
  
  
  // Function to fetch places data
  function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
  
    if (loginLink) {
      if (!token) {
          loginLink.style.display = 'block';
      } else {
          loginLink.style.display = 'none';
          // Fetch places data if the user is authenticated
      }
    }
    
    // Only fetch places if we're on the index page (with places-list)
    const placesContainer = document.getElementById('places-list');
    if (placesContainer) {
      fetchPlaces(token);
    } else if (window.location.pathname.includes('place.html')) {
      // If we're on the place details page
      const placeId = getPlaceIdFromURL();
      if (placeId) {
        checkAuthenticationForPlaceDetails();
      }
    }
  }
  function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
  }
  
  async function fetchPlaces(token) {
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
  
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
          method: 'GET',
          headers: headers,
          credentials: 'include'
      });
  
      if (response.ok) {
          const places = await response.json(); // Tu as correctement défini places ici
          displayPlaces(places); // Et tu passes places à displayPlaces
      } else {
          console.error('Erreur lors de la récupération des logements:', response.statusText);
      }
    } catch (error) {
        console.error('Erreur lors de la récupération des logements:', error);
    }
  }
  
  
  function displayPlaces(places) {
    const placesContainer = document.getElementById('places-list');
    
    if (!placesContainer) {
      console.error('Places container not found');
      return;
    }
    
    // Clear the current container
    placesContainer.innerHTML = '';
    
    // Create a place card for each place
    places.forEach(place => {
      const placeElement = document.createElement('div');
      placeElement.className = 'place';
      placeElement.dataset.price = place.price; // Store price for filtering
      
      placeElement.innerHTML = `
        <div class="place-card">
          <h2>${place.title}</h2>
          <div class="place-details">
            <p class="description">${place.description}</p>
            <p class="location"><strong>Location:</strong> ${place.location}</p>
            <p class="price"><strong>Price:</strong> €${place.price}/night</p>
            ${place.rooms ? `<p class="rooms"><strong>Rooms:</strong> ${place.rooms}</p>` : ''}
            ${place.bathrooms ? `<p class="bathrooms"><strong>Bathrooms:</strong> ${place.bathrooms}</p>` : ''}
          </div>
          <a class="details-button" href="place.html?id=${place.id}">View Details</a>
        </div>
      `;
      
      placesContainer.appendChild(placeElement);
    });
  }
  
  function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
  }
  
  function checkAuthenticationForPlaceDetails() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const placeId = getPlaceIdFromURL();
  
    if (addReviewSection) {
        fetchPlaceDetails(token, placeId);
    }
  }
  
  function getCookie(name) {
    // Function to get a cookie value by its name
    // Your code here
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
  }
  
  async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
  
      const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
        method: 'GET',
        headers: headers,
        credentials: 'include'
      });
      
      if (response.ok) {
        const placeData = await response.json();
        displayPlaceDetails(placeData);
      } else {
        console.error('Error fetching place details:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching place details:', error);
    }
  }
  
  function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section
    const placeDetailsContainer = document.getElementById('place-details');
    if (!placeDetailsContainer) {
      console.error('Place details container not found');
      return;
    }
    placeDetailsContainer.innerHTML = `
      <h1>${place.title}</h1>
      <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
      <p><strong>Price:</strong> €${place.price}/night</p>
      <p><strong>Description:</strong> ${place.description}</p>
      <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
    `;
  
    const placeInfoContainer = document.getElementById('place-info');
    if (!placeInfoContainer) {
      console.error('Place details container not found');
      return;
    }
  
    placeInfoContainer.innerHTML = `
    <h1>Location</h1>
    <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
  
  `;
  
    const reviewsContainer = document.getElementById('reviews');
    if (!reviewsContainer) {
      console.error('Reviews container not found');
      return;
    }
    reviewsContainer.innerHTML = '';
  }
  
  function checkAuthenticationForReview() {
    const token = getCookie('token');
  
    const reviewForm = document.getElementById('add-review');
  
    if (reviewForm) {
      if (!token) {
        reviewForm.style.display = 'none';
      } else {
        reviewForm.style.display = 'block';
      }
    }
    // Don't redirect, just return the token
    return token;
  }
  
  function getCookie(name) {
    // Function to get a cookie value by its name
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
      const token = checkAuthenticationForReview();
      const placeId = getPlaceIdFromURL();
      reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Get review text from form
            // Make AJAX request to submit review
            // Handle the response
            const formData = new FormData(reviewForm);
            const reviewText = formData.get('review-text');
            const response = await submitReview(token, placeId, reviewText);
            if (response.ok) {
                await response.json(); // Parse response without storing unused variable
                alert('Review submitted successfully!');
                // Optionally, you can refresh the reviews section
                fetchPlaceDetails(token, placeId);
            } else {
                alert('Failed to submit review: ' + response.statusText);
  
                element
            }
        });
    }
  });
  
  async function submitReview(token, placeId, reviewText) {
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
  
      if (!token) {
        throw new Error('Authentication token is required');
      }
  
      headers['Authorization'] = `Bearer ${token}`;
      
      // More robust token decoding
      const decodeJWT = JSON.parse(atob(token.split('.')[1]));
      const userId = decodeJWT.sub;
  
      const rating = document.getElementById('rating').value;
      
      
      
      console.log('User ID:', userId.id);
      console.log('Place ID:', placeId);
      console.log('Review Text:', reviewText);
      console.log('Rating:', rating);
      
      if (!userId) {
        throw new Error('User ID not found');
      }
      if (!placeId) {
        throw new Error('Place ID not found');
      }
      if (!reviewText) {
        throw new Error('Review text is required');
      }
      if (!rating) {
        throw new Error('Rating is required');
      }
      if (rating < 1 || rating > 5) {
        throw new Error('Rating must be between 1 and 5');
      }
  
      const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ 
          text: reviewText,
          rating: parseInt(rating),
          user_id: userId.id,
          place_id: placeId
        }),
        credentials: 'include'
      });
      
      return response;
    }
    catch (error) {
      console.error('Error submitting review:', error);
      return { ok: false, statusText: error.message };
    }
  }
  
  function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        // Clear the form
        document.getElementById('review-text').value = '';
    } else {
        alert('Failed to submit review');
    }
  }
  
  async function fetchReviews(placeId) {
    try {
      const token = getCookie('token');
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
  
      const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`, {
        method: 'GET',
        headers: headers,
        credentials: 'include'
      });
      
      if (response.ok) {
        const reviews = await response.json();
        displayReviews(reviews);
      } else {
        console.error('Error fetching reviews:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  }
  
  function displayReviews(reviews) {
  
    const reviewsContainer = document.getElementById('reviews');
    if (!reviewsContainer) {
      console.error('Reviews container not found');
      return;
    }
  
    reviewsContainer.innerHTML = '<h2>Reviews</h2>';
    
    if (reviews.length === 0) {
      reviewsContainer.innerHTML += '<p>No reviews yet.</p>';
      return;
    }
    
    reviews.forEach(review => {
      const reviewElement = document.createElement('div');
      reviewElement.className = 'review';
      
      const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
      
      reviewElement.innerHTML = `
      <div class="review-user">
        <div class="review-header">
          <span class="review-author">${review.user.first_name} ${review.user.last_name}</span>
        </div>
        <div class="review-rating">${stars}</div>
        <br>
        <p class="review-text">${review.text}</p>
      </div>
      `;
      
      reviewsContainer.appendChild(reviewElement);
    });
  }
  
  // Update fetchPlaceDetails to also fetch reviews
  const originalFetchPlaceDetails = fetchPlaceDetails;
  fetchPlaceDetails = async function(token, placeId) {
    await originalFetchPlaceDetails(token, placeId);
    fetchReviews(placeId);
  };