const pdfUrl = './MathPQC-%20AC26%20affiliated%20event.pdf';
const loadButton = document.getElementById('loadPdfBtn');
const statusEl = document.getElementById('status');
const contentEl = document.getElementById('documentContent');

async function extractTextFromPdf(url) {
  if (typeof pdfjsLib === 'undefined') {
    throw new Error('PDF.js failed to load.');
  }

  const loadingTask = pdfjsLib.getDocument({ url });
  const pdf = await loadingTask.promise;
  const textChunks = [];

  for (let pageNum = 1; pageNum <= pdf.numPages; pageNum += 1) {
    const page = await pdf.getPage(pageNum);
    const textContent = await page.getTextContent();
    const pageText = textContent.items
      .map((item) => item.str)
      .join(' ');
    textChunks.push(pageText);
  }

  return textChunks;
}

async function loadPdf() {
  try {
    statusEl.textContent = 'Loading PDF…';
    contentEl.innerHTML = '<p class="muted">Reading PDF content…</p>';

    const pages = await extractTextFromPdf(pdfUrl);

    if (!pages.length) {
      contentEl.innerHTML = '<p class="muted">No readable text found in the PDF.</p>';
      statusEl.textContent = 'Finished';
      return;
    }

    const pageMarkup = pages
      .map((text, index) => {
        const safeText = text.trim() || '(no text detected on this page)';
        return `<div class="page"><h3>Page ${index + 1}</h3><p>${safeText}</p></div>`;
      })
      .join('');

    contentEl.innerHTML = pageMarkup;
    statusEl.textContent = `Loaded ${pages.length} page(s)`;
  } catch (error) {
    console.error(error);
    contentEl.innerHTML = '<p class="muted">Failed to read the PDF. Please make sure the file is available and the browser allows it.</p>';
    statusEl.textContent = 'Failed to load';
  }
}

loadButton.addEventListener('click', loadPdf);
loadPdf();
