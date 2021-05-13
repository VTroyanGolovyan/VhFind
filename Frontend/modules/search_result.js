function renderResult(data) {
  let result = document.getElementById('result')
  result.innerHTML = ''
  for (site of JSON.parse(data)['data']) {
    let a = document.createElement('a')
    let title = document.createElement('div')
    title.innerHTML = site[1]
    let text = document.createElement('div')
    text.innerHTML = site[3]
    let lt = document.createElement('div')
    lt.innerHTML = site[0]
    result.appendChild(a)
    a.appendChild(lt)
    a.appendChild(title)
    a.appendChild(text)
    a.href = site[0]
    a.target = '_blank'
    a.classList.add('result-link')
    lt.classList.add('result-link-text')
    title.classList.add('result-title')
    text.classList.add('result-text')
  }
}

let resultModule = new Module({
  template: './templates/result.html',
  model: {
      queryString: ''
  },
  handlers: {
    result: function(model) {
      VHrequest(
        {
          method: 'POST',
          url: SERVER + 'find',
          data: {
            query: model.queryString
          }
        }
      ).then(
        (data) => {
          renderResult(data)
        }
      )
    }
  },
  onshow: (model) => {
    model.queryString = window.localStorage.getItem('query')
    VHrequest(
      {
        method: 'POST',
        url: SERVER + 'find',
        data: {
          query: model.queryString
        }
      }
    ).then(
      (data) => {
        renderResult(data)
      }
    )
  }
})
