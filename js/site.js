// Pull all H2's into div.headings, or delete div.headings.
const makeTableOfContents = () => {
  const container = document.querySelector('div.headings')
  if (! container) {
    return
  }
  const headings = Array.from(document.querySelectorAll('h2'))
	.filter(h => (h.id !== null) && h.id.startsWith('s:'))
  if (headings.length === 0) {
    container.parentNode.removeChild(container)
  }
  const items = headings
        .map(h => '<li><a href="#' + h.id + '">' + h.innerHTML + '</a></li>')
        .join('\n')
  container.innerHTML = '<h2>Contents</h2><ul>\n' + items + '</ul>'
}

// Add Bootstrap striped table classes to all tables.
const stripeTables = () => {
  Array.from(document.querySelectorAll('table'))
    .forEach(t => t.classList.add('table', 'table-striped'))
}

// Perform transformations on load (which is why this script is included at the
// bottom of the page).
(function(){
  makeTableOfContents()
  stripeTables()
})()
