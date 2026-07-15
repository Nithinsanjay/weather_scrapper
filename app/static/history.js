const form = document.getElementById('history-form');
const input = document.getElementById('history-city');
const status = document.getElementById('history-status');
const results = document.getElementById('history-results');

function setLoading(message) {
  status.innerHTML = `<span>${message}</span>`;
}

function formatValue(value) {
  return Number(value).toFixed(1);
}

function renderHistory(data) {
  if (!data.history || data.history.length === 0) {
    results.innerHTML = '<div class="empty-state"><p>No stored readings found for this city.</p></div>';
    return;
  }

  const items = data.history.map((entry) => {
    const isUp = entry.change.temperature_change >= 0;
    const badgeText = isUp
      ? `↑ ${formatValue(entry.change.temperature_change)}°C`
      : `↓ ${formatValue(Math.abs(entry.change.temperature_change))}°C`;

    return `
      <div class="history-item">
        <div class="history-header">
          <div>
            <strong>${entry.city}</strong>
            <p class="history-time">${new Date(entry.updated_at).toLocaleString()}</p>
          </div>
          <span class="history-badge ${isUp ? 'up' : 'down'}">${badgeText}</span>
        </div>
        <div class="history-grid">
          <div class="metric">
            <span class="metric-label">Temperature</span>
            <span class="metric-value">${formatValue(entry.temperature)}°C</span>
          </div>
          <div class="metric">
            <span class="metric-label">Humidity</span>
            <span class="metric-value">${formatValue(entry.humidity)}%</span>
          </div>
          <div class="metric">
            <span class="metric-label">Temp change</span>
            <span class="metric-value">${formatValue(entry.change.temperature_change)}°C</span>
          </div>
          <div class="metric">
            <span class="metric-label">Humidity change</span>
            <span class="metric-value">${formatValue(entry.change.humidity_change)}%</span>
          </div>
        </div>
      </div>
    `;
  }).join('');

  results.innerHTML = `<div class="history-list">${items}</div>`;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const city = input.value.trim();

  if (!city) {
    status.innerHTML = '<strong>Please enter a city name.</strong>';
    return;
  }

  setLoading(`Loading history for ${city}...`);

  try {
    const response = await fetch(`/history-data/${encodeURIComponent(city)}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Unable to load history.');
    }

    renderHistory(data);
    status.innerHTML = `Showing ${data.history.length} stored reading(s) for <strong>${data.city}</strong>.`;
  } catch (error) {
    results.innerHTML = '<div class="empty-state"><p>Unable to load history for this city.</p></div>';
    status.innerHTML = `<strong>${error.message}</strong>`;
  }
});
