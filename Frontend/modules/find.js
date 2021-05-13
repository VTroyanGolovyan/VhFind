let finderModule = new Module({
  template: './templates/find_page.html',
  model: {
    queryString: ''
  },
  handlers: {
    queryInput: function (model) {
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

        }
      )
    },
    result: function(model) {
      window.localStorage.setItem('query', model.queryString)
      document.location.hash = '#/Result'
    }
  }
})
