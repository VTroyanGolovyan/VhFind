

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
          let result = document.getElementById('result')
          result.innerHTML = ''
          for (site of JSON.parse(data)['data']) {
            let a = document.createElement('a')
            result.appendChild(a)
            a.innerHTML = site[1]
            a.href = site[0]
            a.target = '_blank'
          }
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
        let result = document.getElementById('result')
        result.innerHTML = ''
        for (site of JSON.parse(data)['data']) {
          let a = document.createElement('a')
          result.appendChild(a)
          a.innerHTML = site[1]
          a.href = site[0]
          a.target = '_blank'
        }
      }
    )
  }
})
