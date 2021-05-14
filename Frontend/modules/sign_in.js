let signinModule = new Module({
  template: './templates/sign_in.html',
  model: {
    email: '',
    password: ''
  },
  handlers: {
    loginButton: function(model) {
      VHrequest({
        method: 'POST',
        url: SERVER + '/sign/in',
        data: {
          email: model.email,
          password: model.password
        }
      }).then((response) => {
        try {
          data = JSON.parse(response)
          if (data.data == '') {
            return
          }
          document.localStorage.setItem('token', data.data)
          location.hash = '#/'
        } catch (e) {

        } finally {

        }

      })
    }
  }
})
