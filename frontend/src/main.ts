import './style.css'
import 'katex/dist/katex.min.css'
import katex from 'katex'

const app = document.querySelector<HTMLDivElement>('#app')!
app.innerHTML = `
  <div class="container">
    <div class="controls">
      <button id="start" type="button">Start</button>
      <button id="stop" type="button" disabled>Stop</button>
    </div>
    <ol id="expressions"></ol>
  </div>
`

const startBtn = document.querySelector<HTMLButtonElement>('#start')!
const stopBtn = document.querySelector<HTMLButtonElement>('#stop')!
const listEl = document.querySelector<HTMLOListElement>('#expressions')!

let eventSource: EventSource | null = null

function renderTex(tex: string): string {
  const inner = tex.startsWith('$') && tex.endsWith('$') ? tex.slice(1, -1) : tex
  return katex.renderToString(inner, { displayMode: false, throwOnError: false })
}

function stopStream() {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
  startBtn.disabled = false
  stopBtn.disabled = true
}

startBtn.addEventListener('click', () => {
  startBtn.disabled = true
  stopBtn.disabled = false
  listEl.innerHTML = ''

  eventSource = new EventSource('/api/generate?lang=MathLexs')

  const maxLines = 10000
  eventSource.onmessage = (e) => {
    const { expression } = JSON.parse(e.data) as { expression: string; raw: string }
    const li = document.createElement('li')
    li.innerHTML = renderTex(expression)
    listEl.appendChild(li)
    if (listEl.children.length >= maxLines) {
      stopStream()
    }
  }

  eventSource.onerror = () => {
    stopStream()
  }
})

stopBtn.addEventListener('click', () => {
  stopStream()
})
