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

// Fix glossary reference URLs.
const fixGlossRefs = () => {
  const pageIsRoot = document.currentScript.getAttribute('ROOT') != ''
  const bibStem = pageIsRoot ? './gloss/' : '../gloss/'
  Array.from(document.querySelectorAll('a'))
    .filter(e => e.getAttribute('href').startsWith('#g:'))
    .forEach(e => {
      e.setAttribute('href', bibStem + e.getAttribute('href'))
    })
}

// Convert bibliography citation links.
const fixBibRefs = () => {
  const pageIsRoot = document.currentScript.getAttribute('ROOT') != ''
  const bibStem = pageIsRoot ? './bib/#b:' : '../bib/#b:'
  Array.from(document.querySelectorAll('a'))
    .filter(e => e.getAttribute('href') == '#BIB')
    .forEach(e => {
      const cites = e.textContent
	    .split(',')
	    .filter(c => c.length > 0)
	    .map(c => '<a href="' + bibStem + c + '" class="citation">' + c + '</a>')
      const newNode = document.createElement('span')
      newNode.innerHTML = '[' + cites.join(',') + ']'
      e.parentNode.replaceChild(newNode, e)
    })
}

// Convert chapter references.
const fixCrossRefs = () => {
  const pageIsRoot = document.currentScript.getAttribute('ROOT') != ''
  const pathToRoot = pageIsRoot ? './' : '../'
  const pathToFile = pathToRoot + 'toc.json'
  fetch(pathToFile)
    .then(response => response.json())
    .then(crossref => {
      const main = document.querySelector('div.main')
      if (! main) {
        return
      }
      Array.from(main.querySelectorAll('a'))
        .filter(e => {
          return e.innerHTML === 'CHAPTER'
        })
        .forEach(e => {
          const slug = e.getAttribute('href').split('/')[1]
          const entry = crossref[slug]
          var text = 'Unknown Reference'
          if (entry.type === 'number') {
            text = `Chapter ${entry.index}`
          } else if (entry.type === 'letter') {
            const letters = '_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            text = `Appendix ${letters[entry.index]}`
          } else if (entry.type === 'bib') {
            text = 'Bibliography'
          }
          e.innerHTML = text
        })
    })
}

// Perform transformations on load (which is why this script is included at the
// bottom of the page).
(function(){
  makeTableOfContents()
  stripeTables()
  fixBibRefs()
  fixGlossRefs()
  fixCrossRefs()
})()
