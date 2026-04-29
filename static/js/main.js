const queryInput = document.getElementById('queryInput');
const charCount = document.getElementById('charCount');
const searchBtn = document.getElementById('searchBtn');
const btnText = document.getElementById('btnText');
const resultSection = document.getElementById('resultSection');
const loading = document.getElementById('loading');
const resultCard = document.getElementById('resultCard');
const resultBody = document.getElementById('resultBody');
const resultMeta = document.getElementById('resultMeta');
const loadingMsg = document.getElementById('loadingMsg');

const loadingMessages = [
  'Searching product database...',
  'Analyzing requirements...',
  'Matching specifications...',
  'Generating recommendation...'
];

queryInput.addEventListener('input', () => {
  charCount.textContent = `${queryInput.value.length} characters`;
});

function fillExample(btn) {
  queryInput.value = btn.textContent.trim();
  charCount.textContent = `${queryInput.value.length} characters`;
  queryInput.focus();
  queryInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function makeLinksClickable(text) {
  return text.replace(
    /(https?:\/\/[^\s<]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer" class="result-link">$1 ↗</a>'
  );
}

function typeHTML(element, html, speed = 6) {
  // If contains links, just show instantly to avoid broken tags
  if (html.includes('<a ')) {
    element.innerHTML = html;
    return;
  }
  element.innerHTML = '';
  const chars = html.split('');
  let i = 0;
  const interval = setInterval(() => {
    element.innerHTML += chars[i];
    i++;
    if (i >= chars.length) clearInterval(interval);
  }, speed);
}

let loadingInterval;

function startLoadingMessages() {
  let i = 0;
  loadingMsg.textContent = loadingMessages[0];
  loadingMsg.style.transition = 'opacity 0.2s ease';
  loadingInterval = setInterval(() => {
    i = (i + 1) % loadingMessages.length;
    loadingMsg.style.opacity = '0';
    setTimeout(() => {
      loadingMsg.textContent = loadingMessages[i];
      loadingMsg.style.opacity = '1';
    }, 200);
  }, 2000);
}

function stopLoadingMessages() {
  clearInterval(loadingInterval);
}

async function search() {
  const query = queryInput.value.trim();
  if (!query) {
    queryInput.focus();
    queryInput.style.borderColor = '#EF4444';
    setTimeout(() => { queryInput.style.borderColor = ''; }, 1000);
    return;
  }

  searchBtn.disabled = true;
  btnText.textContent = 'Analyzing...';
  resultSection.style.display = 'block';
  loading.classList.add('active');
  resultCard.classList.remove('active');
  resultBody.innerHTML = '';
  startLoadingMessages();

  const start = Date.now();

  try {
    const response = await fetch('/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    const data = await response.json();
    const elapsed = ((Date.now() - start) / 1000).toFixed(1);

    stopLoadingMessages();
    loading.classList.remove('active');
    resultCard.classList.add('active');
    resultMeta.textContent = `Response in ${elapsed}s`;

    const formatted = makeLinksClickable(data.recommendation);
    typeHTML(resultBody, formatted, 6);

  } catch (error) {
    stopLoadingMessages();
    loading.classList.remove('active');
    resultCard.classList.add('active');
    resultBody.textContent = 'Something went wrong. Please try again.';
  } finally {
    searchBtn.disabled = false;
    btnText.textContent = 'Analyze & Recommend';
  }
}

queryInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    search();
  }
});