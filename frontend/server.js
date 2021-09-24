const { createSSRApp } = require('vue')
const { renderToString } = require('@vue/server-renderer')
const server = require('express')()
const fs = require('fs');

server.get('*', async (req, res) => {
  const app = createSSRApp({
    data() {
      return {
        result: 'hello'
      }
    },
    template: `<div>Message from the server: "{{ result }}"</div>`
  })

  const appContent = await renderToString(app)
  const html = `
  <html>
    <body>
      <h1>GeoCoLab</h1>
      <div id="app">${appContent}</div>
    </body>
  </html>
  `

  res.end(html)
})

server.listen('/tmp/nginx.socket', function () {
    console.info(`server up`);
    fs.openSync('/tmp/app-initialized', 'w');
});
