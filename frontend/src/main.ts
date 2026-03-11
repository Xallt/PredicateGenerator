import './style.css'
import 'katex/dist/katex.min.css'
import katex from 'katex'

const app = document.querySelector<HTMLDivElement>('#app')!
app.innerHTML = `
  <div class="container">
    <button id="start" type="button">Start</button>
    <ol id="expressions"></ol>
  </div>
`

const startBtn = document.querySelector<HTMLButtonElement>('#start')!
const listEl = document.querySelector<HTMLOListElement>('#expressions')!

function renderTex(tex: string): string {
  const inner = tex.startsWith('$') && tex.endsWith('$') ? tex.slice(1, -1) : tex
  return katex.renderToString(inner, { displayMode: false, throwOnError: false })
}

startBtn.addEventListener('click', () => {
  startBtn.disabled = true
  listEl.innerHTML = ''

  const eventSource = new EventSource('/api/generate?size=25&lang=MathLexs')

  eventSource.onmessage = (e) => {
    if (e.data === '') return
    const { expression } = JSON.parse(e.data) as { expression: string; raw: string }
    const li = document.createElement('li')
    li.innerHTML = renderTex(expression)
    listEl.appendChild(li)
  }

  eventSource.addEventListener('done', () => {
    eventSource.close()
    startBtn.disabled = false
  })

  eventSource.onerror = () => {
    eventSource.close()
    startBtn.disabled = false
  }
})
