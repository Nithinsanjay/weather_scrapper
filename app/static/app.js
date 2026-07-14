const form = document.getElementById('city-form');
const cityInput = document.getElementById('city-input');
const statusMessage = document.getElementById('status-message');
const cityName = document.getElementById('city-name');
const cityRegion = document.getElementById('city-region');
const temperature = document.getElementById('temperature');
const humidity = document.getElementById('humidity');
const updatedAt = document.getElementById('updated-at');

function setLoading(message) {
  statusMessage.innerHTML = `<span>${message}</span>`;
}

function renderWeather(data) {
  cityName.textContent = data.city || 'Unknown city';
  cityRegion.textContent = 'Live weather snapshot';
  temperature.textContent = `${Number(data.temperature).toFixed(0)}°C`;
  humidity.textContent = `${Number(data.humidity).toFixed(0)}%`;
  updatedAt.textContent = new Date(data.updated_at).toLocaleString();
}

function renderError(message) {
  cityName.textContent = 'Weather unavailable';
  cityRegion.textContent = 'Try another city';
  temperature.textContent = '--°C';
  humidity.textContent = '--%';
  updatedAt.textContent = '--';
  statusMessage.innerHTML = `<strong>${message}</strong>`;
}

async function fetchWeather(city) {
  const response = await fetch(`/scrape/${encodeURIComponent(city)}`, { method: 'POST' });
  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || 'Unable to fetch weather details.');
  }

  return result.data;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const city = cityInput.value.trim();

  if (!city) {
    renderError('Please enter a city name.');
    return;
  }

  setLoading(`Fetching weather for ${city}...`);

  try {
    const data = await fetchWeather(city);
    renderWeather(data);
    statusMessage.innerHTML = `Showing live weather for <strong>${data.city}</strong>.`;
  } catch (error) {
    renderError(error.message);
  }
});

window.addEventListener('DOMContentLoaded', async () => {
  setLoading('Fetching weather for Chennai...');

  try {
    const data = await fetchWeather('Chennai');
    renderWeather(data);
    statusMessage.innerHTML = `Showing live weather for <strong>${data.city}</strong>.`;
  } catch (error) {
    renderError(error.message);
  }
});
